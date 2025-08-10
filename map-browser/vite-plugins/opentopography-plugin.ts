import type { Plugin } from 'vite';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs/promises';
import fetch from 'node-fetch';
import sharp from 'sharp';

interface DownloadRequest {
  bounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
  center: {
    lat: number;
    lng: number;
  };
  scale: number;
  gridSize: number;
  resolution: string;
}

interface SatelliteDownloadRequest {
  bounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
  center: {
    lat: number;
    lng: number;
  };
  scale: number;
  gridSize: number;
  resolution: number; // pixels per meter
  mapboxToken: string;
}

interface DTMMatchedSatelliteRequest {
  dtmFilePath: string;
  mapboxToken: string;
  targetResolution?: number; // pixels per meter, defaults to match DTM
}

export function openTopographyPlugin(): Plugin {
  return {
    name: 'opentopography-api',
    configureServer(server) {
      server.middlewares.use('/api/download-terrain', async (req, res) => {
        if (req.method !== 'POST') {
          res.writeHead(405, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Method not allowed' }));
          return;
        }

        let body = '';
        req.on('data', chunk => {
          body += chunk.toString();
        });

        req.on('end', async () => {
          try {
            const data: DownloadRequest = JSON.parse(body);
            
            // Validate the request data
            if (!data.bounds || !data.center || !data.scale || !data.gridSize || !data.resolution) {
              res.writeHead(400, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ error: 'Missing required parameters' }));
              return;
            }

            // Calculate bounds from center point and scale
            const { bounds, center, scale, gridSize, resolution } = data;
            
            console.log('📍 OpenTopography download request:', {
              center: `${center.lat.toFixed(6)}, ${center.lng.toFixed(6)}`,
              bounds: `N:${bounds.north.toFixed(6)}, S:${bounds.south.toFixed(6)}, E:${bounds.east.toFixed(6)}, W:${bounds.west.toFixed(6)}`,
              scale: `${scale}km`,
              gridSize: `${gridSize}x${gridSize}`,
              resolution: resolution
            });

            // Generate filename based on location
            const locationName = `${center.lat.toFixed(4)}_${center.lng.toFixed(4)}`;
            const filename = `terrain_${locationName}_${resolution}_${scale}km.tif`;
            
            // Create downloads directory if it doesn't exist
            const downloadsDir = path.join(process.cwd(), 'downloads');
            await fs.mkdir(downloadsDir, { recursive: true });

            // Call the download script
            const result = await downloadTerrain({
              bounds,
              filename,
              outputDir: downloadsDir,
              resolution
            });

            if (result.success) {
              const filePath = path.join(downloadsDir, filename);
              const stats = await fs.stat(filePath);
              
              res.writeHead(200, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({
                success: true,
                message: 'Terrain data downloaded successfully',
                filename,
                fileSize: Math.round(stats.size / 1024) + ' KB',
                location: `${center.lat.toFixed(6)}, ${center.lng.toFixed(6)}`,
                bounds: bounds
              }));
            } else {
              res.writeHead(500, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ 
                success: false, 
                error: result.error || 'Failed to download terrain data'
              }));
            }

          } catch (error) {
            console.error('Error processing terrain download:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
              success: false, 
              error: 'Internal server error: ' + (error as Error).message 
            }));
          }
        });
      });

      // Add endpoint to list downloaded files
      server.middlewares.use('/api/downloaded-files', async (req, res) => {
        if (req.method !== 'GET') {
          res.writeHead(405, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Method not allowed' }));
          return;
        }

        try {
          const downloadsDir = path.join(process.cwd(), 'downloads');
          const files = await fs.readdir(downloadsDir);
          const terrainFiles = files.filter(file => file.endsWith('.tif') || file.endsWith('.asc'));
          
          const fileDetails = await Promise.all(
            terrainFiles.map(async (file) => {
              const filePath = path.join(downloadsDir, file);
              const stats = await fs.stat(filePath);
              return {
                name: file,
                size: Math.round(stats.size / 1024) + ' KB',
                modified: stats.mtime.toISOString()
              };
            })
          );

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ files: fileDetails }));

        } catch (error) {
          console.error('Error listing files:', error);
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Failed to list files' }));
        }
      });

      // Elevation query endpoint
      server.middlewares.use('/api/query-elevation', async (req, res) => {
        if (req.method !== 'POST') {
          res.writeHead(405, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Method not allowed' }));
          return;
        }

        let body = '';
        req.on('data', chunk => {
          body += chunk.toString();
        });

        req.on('end', async () => {
          try {
            const data: { lat: number; lng: number } = JSON.parse(body);
            
            if (!data.lat || !data.lng) {
              res.writeHead(400, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ error: 'Missing lat/lng parameters' }));
              return;
            }

            const elevation = await queryElevation(data.lat, data.lng);
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ elevation }));

          } catch (error) {
            console.error('Error querying elevation:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Failed to query elevation' }));
          }
        });
      });

      // Satellite imagery download endpoint
      server.middlewares.use('/api/download-satellite', async (req, res) => {
        if (req.method !== 'POST') {
          res.writeHead(405, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Method not allowed' }));
          return;
        }

        let body = '';
        req.on('data', chunk => {
          body += chunk.toString();
        });

        req.on('end', async () => {
          try {
            const data: SatelliteDownloadRequest = JSON.parse(body);
            
            // Validate the request data
            if (!data.bounds || !data.center || !data.scale || !data.resolution || !data.mapboxToken) {
              res.writeHead(400, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ error: 'Missing required parameters' }));
              return;
            }

            const { bounds, center, scale, resolution, mapboxToken } = data;
            
            console.log('🛰️ Satellite imagery download request:', {
              center: `${center.lat.toFixed(6)}, ${center.lng.toFixed(6)}`,
              bounds: `N:${bounds.north.toFixed(6)}, S:${bounds.south.toFixed(6)}, E:${bounds.east.toFixed(6)}, W:${bounds.west.toFixed(6)}`,
              scale: `${scale}km`,
              resolution: `${resolution} pixels/meter`
            });

            // Generate filename based on location and resolution
            const locationName = `${center.lat.toFixed(4)}_${center.lng.toFixed(4)}`;
            const filename = `satellite_${locationName}_${resolution}ppm_${scale}km.jpg`;
            
            // Create downloads directory if it doesn't exist
            const downloadsDir = path.join(process.cwd(), 'downloads');
            await fs.mkdir(downloadsDir, { recursive: true });

            // Download satellite imagery
            const result = await downloadSatelliteImagery({
              bounds,
              center,
              scale,
              resolution,
              filename,
              outputDir: downloadsDir,
              mapboxToken
            });

            if (result.success) {
              const filePath = path.join(downloadsDir, filename);
              const stats = await fs.stat(filePath);
              
              res.writeHead(200, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({
                success: true,
                message: 'Satellite imagery downloaded successfully',
                filename,
                fileSize: Math.round(stats.size / 1024) + ' KB',
                location: `${center.lat.toFixed(6)}, ${center.lng.toFixed(6)}`,
                bounds: bounds,
                resolution: `${resolution} pixels/meter`
              }));
            } else {
              res.writeHead(500, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ 
                success: false, 
                error: result.error || 'Failed to download satellite imagery'
              }));
            }

          } catch (error) {
            console.error('Error processing satellite download:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
              success: false, 
              error: 'Internal server error: ' + (error as Error).message 
            }));
          }
        });
      });

      // DTM-matched satellite imagery download endpoint
      server.middlewares.use('/api/download-satellite-dtm-matched', async (req, res) => {
        if (req.method !== 'POST') {
          res.writeHead(405, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Method not allowed' }));
          return;
        }

        let body = '';
        req.on('data', chunk => {
          body += chunk.toString();
        });

        req.on('end', async () => {
          try {
            const data: DTMMatchedSatelliteRequest = JSON.parse(body);
            
            // Validate the request data
            if (!data.dtmFilePath || !data.mapboxToken) {
              res.writeHead(400, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ error: 'Missing required parameters: dtmFilePath and mapboxToken' }));
              return;
            }

            console.log('🗺️ DTM-matched satellite download request:', {
              dtmFilePath: data.dtmFilePath,
              targetResolution: data.targetResolution || 'match DTM'
            });

            // Create downloads directory if it doesn't exist
            const downloadsDir = path.join(process.cwd(), 'downloads');
            await fs.mkdir(downloadsDir, { recursive: true });

            // Download satellite imagery to match DTM
            const result = await downloadSatelliteToMatchDTM({
              dtmFilePath: data.dtmFilePath,
              mapboxToken: data.mapboxToken,
              targetResolution: data.targetResolution,
              outputDir: downloadsDir
            });

            if (result.success && result.filename) {
              const filePath = path.join(downloadsDir, result.filename);
              const stats = await fs.stat(filePath);
              
              res.writeHead(200, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({
                success: true,
                message: 'Complete DTM-matched satellite processing finished',
                filename: result.filename,
                fileSize: Math.round(stats.size / 1024) + ' KB',
                bounds: result.bounds,
                projection: result.projection,
                resolution: result.resolution,
                additionalFiles: result.additionalFiles,
                processingSteps: [
                  '✅ DTM analysis and coordinate transformation',
                  '✅ High-resolution satellite download with tiling',
                  '✅ Georeferencing and projection matching',
                  '✅ Exact DTM bounds alignment (10000x10000)',
                  '✅ JPEG conversion',
                  '✅ Center crop to 8K (8192x8192)',
                  '✅ Scale to 4K for BeamNG (4096x4096)'
                ]
              }));
            } else {
              res.writeHead(500, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ 
                success: false, 
                error: result.error || 'Failed to download DTM-matched satellite imagery'
              }));
            }

          } catch (error) {
            console.error('Error processing DTM-matched satellite download:', error);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
              success: false, 
              error: 'Internal server error: ' + (error as Error).message 
            }));
          }
        });
      });
    }
  };
}

async function downloadSatelliteImagery(params: {
  bounds: { north: number; south: number; east: number; west: number };
  center: { lat: number; lng: number };
  scale: number;
  resolution: number; // pixels per meter
  filename: string;
  outputDir: string;
  mapboxToken: string;
}): Promise<{ success: boolean; error?: string }> {
  try {
    const { bounds, resolution, filename, outputDir, mapboxToken } = params;
    
    // Calculate the area size in meters
    const areaSizeMeters = params.scale * 1024; // Total area size
    
    // Calculate required image dimensions for the desired resolution
    const totalPixelsNeeded = Math.ceil(areaSizeMeters * resolution);
    
    // Mapbox Static API maximum size per tile
    const maxTileSize = 1280;
    
    // Calculate how many tiles we need in each direction
    const tilesPerSide = Math.ceil(totalPixelsNeeded / maxTileSize);
    const totalTiles = tilesPerSide * tilesPerSide;
    
    // Calculate actual tile size and resolution
    const pixelsPerTile = Math.min(totalPixelsNeeded, maxTileSize);
    const actualTotalPixels = tilesPerSide * pixelsPerTile;
    const actualResolution = actualTotalPixels / areaSizeMeters;
    
    console.log(`📐 High-resolution tiling calculation:`, {
      requestedResolution: resolution,
      actualResolution: actualResolution.toFixed(3),
      totalPixelsNeeded,
      actualTotalPixels: `${actualTotalPixels}x${actualTotalPixels}`,
      tilesPerSide,
      totalTiles,
      pixelsPerTile: `${pixelsPerTile}x${pixelsPerTile}`,
      areaSizeMeters
    });
    
    // If we only need one tile, use the simple approach
    if (tilesPerSide === 1) {
      return await downloadSingleTile(params, pixelsPerTile);
    }
    
    // Download multiple tiles and stitch them together
    console.log(`🧩 Downloading ${totalTiles} tiles to achieve ${actualResolution.toFixed(3)} pixels/meter`);
    
    // Calculate bounds for each tile
    const latSpan = bounds.north - bounds.south;
    const lngSpan = bounds.east - bounds.west;
    const latStep = latSpan / tilesPerSide;
    const lngStep = lngSpan / tilesPerSide;
    
    // Download all tiles
    const tilePromises: Promise<{ buffer: Buffer; row: number; col: number }>[] = [];
    
    for (let row = 0; row < tilesPerSide; row++) {
      for (let col = 0; col < tilesPerSide; col++) {
        const tileBounds = {
          north: bounds.north - (row * latStep),
          south: bounds.north - ((row + 1) * latStep),
          west: bounds.west + (col * lngStep),
          east: bounds.west + ((col + 1) * lngStep)
        };
        
        tilePromises.push(downloadTile(tileBounds, pixelsPerTile, mapboxToken, row, col));
      }
    }
    
    console.log(`⬇️ Downloading ${totalTiles} tiles...`);
    const tiles = await Promise.all(tilePromises);
    
    console.log(`🔧 Stitching ${totalTiles} tiles together...`);
    
    // Create a large canvas and composite all tiles
    // Set a high pixel limit to allow large high-resolution images
    const maxPixels = actualTotalPixels * actualTotalPixels;
    const compositeImage = sharp({
      create: {
        width: actualTotalPixels,
        height: actualTotalPixels,
        channels: 3,
        background: { r: 0, g: 0, b: 0 }
      },
      limitInputPixels: maxPixels * 2 // Set limit to 2x the actual pixels needed for safety
    });
    
    // Prepare composite operations
    const compositeOperations = tiles.map(tile => ({
      input: tile.buffer,
      top: tile.row * pixelsPerTile,
      left: tile.col * pixelsPerTile
    }));
    
    // Composite all tiles into one image
    const finalImageBuffer = await compositeImage
      .composite(compositeOperations)
      .jpeg({ quality: 95 })
      .toBuffer();
    
    // Save the final image
    const filePath = path.join(outputDir, filename);
    await fs.writeFile(filePath, finalImageBuffer);
    
    console.log(`✅ High-resolution satellite imagery saved: ${filename}`);
    console.log(`📊 Final resolution: ${actualResolution.toFixed(3)} pixels/meter`);
    console.log(`📏 Image dimensions: ${actualTotalPixels}x${actualTotalPixels} pixels`);
    console.log(`💾 File size: ${(finalImageBuffer.length / 1024 / 1024).toFixed(2)} MB`);
    
    return { success: true };
    
  } catch (error) {
    console.error('❌ Error downloading high-resolution satellite imagery:', error);
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}

async function downloadSingleTile(params: {
  bounds: { north: number; south: number; east: number; west: number };
  center: { lat: number; lng: number };
  scale: number;
  resolution: number;
  filename: string;
  outputDir: string;
  mapboxToken: string;
}, imageSize: number): Promise<{ success: boolean; error?: string }> {
  const { bounds, filename, outputDir, mapboxToken } = params;
  
  // Build Mapbox Static API URL without watermarks
  const mapboxUrl = `https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/` +
    `[${bounds.west},${bounds.south},${bounds.east},${bounds.north}]/` +
    `${imageSize}x${imageSize}?` +
    `attribution=false&logo=false&` +
    `access_token=${mapboxToken}`;
  
  console.log('🌍 Downloading single high-resolution tile...');
  
  // Download the image
  const response = await fetch(mapboxUrl);
  
  if (!response.ok) {
    throw new Error(`Mapbox API error: ${response.status} ${response.statusText}`);
  }
  
  // Save the image
  const filePath = path.join(outputDir, filename);
  const buffer = await response.arrayBuffer();
  await fs.writeFile(filePath, Buffer.from(buffer));
  
  return { success: true };
}

async function downloadTile(
  bounds: { north: number; south: number; east: number; west: number },
  size: number,
  mapboxToken: string,
  row: number,
  col: number
): Promise<{ buffer: Buffer; row: number; col: number }> {
  
  const mapboxUrl = `https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/` +
    `[${bounds.west},${bounds.south},${bounds.east},${bounds.north}]/` +
    `${size}x${size}?` +
    `attribution=false&logo=false&` +
    `access_token=${mapboxToken}`;
  
  const response = await fetch(mapboxUrl);
  
  if (!response.ok) {
    throw new Error(`Mapbox API error for tile ${row},${col}: ${response.status} ${response.statusText}`);
  }
  
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  
  console.log(`✓ Downloaded tile ${row},${col} (${buffer.length} bytes)`);
  
  return { buffer, row, col };
}

async function downloadTerrain(params: {
  bounds: { north: number; south: number; east: number; west: number };
  filename: string;
  outputDir: string;
  resolution: string;
}): Promise<{ success: boolean; error?: string }> {
  return new Promise((resolve) => {
    const scriptPath = path.join(process.cwd(), 'scripts', 'download-server.ts');
    
    const args = [
      scriptPath,
      '--bounds', JSON.stringify(params.bounds),
      '--filename', params.filename,
      '--output-dir', params.outputDir,
      '--dataset', params.resolution
    ];

    console.log('🚀 Executing:', 'npx tsx', args.join(' '));

    const child = spawn('npx', ['tsx', ...args], {
      stdio: 'pipe',
      cwd: process.cwd()
    });

    let stdout = '';
    let stderr = '';

    child.stdout?.on('data', (data) => {
      stdout += data.toString();
      console.log('📥 Script output:', data.toString().trim());
    });

    child.stderr?.on('data', (data) => {
      stderr += data.toString();
      console.error('📥 Script error:', data.toString().trim());
    });

    child.on('close', (code) => {
      console.log(`📋 Script finished with code: ${code}`);
      if (code === 0) {
        console.log('✅ Terrain download completed successfully');
        resolve({ success: true });
      } else {
        console.error('❌ Terrain download failed');
        console.error('STDOUT:', stdout);
        console.error('STDERR:', stderr);
        
        // Extract meaningful error from stderr
        let errorMessage = 'Download failed';
        
        // Look for specific error patterns in stderr
        const stderrText = stderr.trim();
        const stdoutText = stdout.trim();
        
        // Try to extract the actual error message
        if (stderrText.includes('HTTP')) {
          const httpErrorMatch = stderrText.match(/HTTP \d+: [^\n]+/);
          if (httpErrorMatch) {
            errorMessage = httpErrorMatch[0];
          }
        } else if (stderrText.includes('Error:')) {
          const errorMatch = stderrText.match(/Error: ([^\n]+)/);
          if (errorMatch) {
            errorMessage = errorMatch[1];
          }
        } else if (stdoutText.includes('❌')) {
          // Look for error messages in stdout
          const lines = stdoutText.split('\n');
          const errorLine = lines.find(line => line.includes('❌'));
          if (errorLine) {
            errorMessage = errorLine.replace(/❌\s*/, '').trim();
          }
        }
        
        resolve({ success: false, error: errorMessage });
      }
    });

    child.on('error', (error) => {
      console.error('❌ Failed to start download script:', error);
      resolve({ success: false, error: `Failed to start download script: ${error.message}` });
    });
  });
}

async function downloadSatelliteToMatchDTM(params: {
  dtmFilePath: string;
  mapboxToken: string;
  targetResolution?: number;
  outputDir: string;
}): Promise<{ 
  success: boolean; 
  error?: string; 
  filename?: string;
  bounds?: { north: number; south: number; east: number; west: number };
  projection?: string;
  resolution?: string;
}> {
  try {
    const { dtmFilePath, mapboxToken, targetResolution, outputDir } = params;
    
    console.log('🗺️ Analyzing DTM file for satellite matching...');
    
    // Get DTM information using gdalinfo
    const dtmInfo = await getDTMInfo(dtmFilePath);
    if (!dtmInfo.success) {
      return { success: false, error: dtmInfo.error };
    }
    
    console.log('📊 DTM Analysis:', {
      projection: dtmInfo.projection,
      bounds: dtmInfo.bounds,
      size: `${dtmInfo.width}x${dtmInfo.height}`,
      pixelSize: dtmInfo.pixelSize
    });
    
    // Convert UTM bounds to WGS84 for Mapbox API
    if (!dtmInfo.bounds || !dtmInfo.projection) {
      return { success: false, error: 'Missing bounds or projection from DTM analysis' };
    }
    
    const wgs84Bounds = await transformBoundsToWGS84(dtmInfo.bounds, dtmInfo.projection);
    if (!wgs84Bounds.success) {
      return { success: false, error: wgs84Bounds.error };
    }
    
    console.log('🌍 WGS84 bounds for satellite download:', wgs84Bounds.bounds);
    
    // Calculate target resolution
    if (!dtmInfo.pixelSize) {
      return { success: false, error: 'Missing pixel size from DTM analysis' };
    }
    const resolution = targetResolution || (1 / Math.abs(dtmInfo.pixelSize.x)); // pixels per meter
    
    // Generate filename based on DTM
    const dtmBasename = path.basename(dtmFilePath, path.extname(dtmFilePath));
    const filename = `satellite_${dtmBasename}_${resolution}ppm.jpg`;
    
    // Calculate area size in meters
    const areaSizeMeters = Math.max(
      Math.abs(dtmInfo.bounds.east - dtmInfo.bounds.west),
      Math.abs(dtmInfo.bounds.north - dtmInfo.bounds.south)
    );
    
    console.log('📐 Satellite download parameters:', {
      resolution: `${resolution} pixels/meter`,
      areaSizeMeters: `${areaSizeMeters}m`,
      targetSize: `${Math.ceil(areaSizeMeters * resolution)}px`
    });
    
    // Download satellite imagery using high-resolution tiling
    if (!wgs84Bounds.bounds) {
      return { success: false, error: 'Missing WGS84 bounds from coordinate transformation' };
    }
    
    const satelliteResult = await downloadHighResSatelliteImagery({
      bounds: wgs84Bounds.bounds,
      resolution,
      filename,
      outputDir,
      mapboxToken
    });
    
    if (!satelliteResult.success) {
      return { success: false, error: satelliteResult.error };
    }
    
    const satelliteFilePath = path.join(outputDir, filename);
    
    // Georeference the satellite image in WGS84
    const wgs84Filename = `satellite_${dtmBasename}_wgs84.tif`;
    const wgs84FilePath = path.join(outputDir, wgs84Filename);
    
    console.log('🌐 Georeferencing satellite image in WGS84...');
    const georefResult = await georeferenceSatelliteImage(
      satelliteFilePath,
      wgs84FilePath,
      wgs84Bounds.bounds
    );
    
    if (!georefResult.success) {
      return { success: false, error: georefResult.error };
    }
    
    // Transform to match DTM projection
    const projectedFilename = `satellite_${dtmBasename}_projected.tif`;
    const projectedFilePath = path.join(outputDir, projectedFilename);
    
    console.log('🔄 Transforming to match DTM projection...');
    const transformResult = await transformSatelliteToMatchDTM(
      wgs84FilePath,
      projectedFilePath,
      dtmInfo.projection // Use the projection code instead of file path
    );
    
    if (!transformResult.success) {
      return { success: false, error: transformResult.error };
    }
    
    // Align exactly to DTM bounds and dimensions
    const alignedFilename = `satellite_${dtmBasename}_aligned.tif`;
    const alignedFilePath = path.join(outputDir, alignedFilename);
    
    console.log('📐 Aligning to exact DTM bounds and dimensions...');
    const alignResult = await alignSatelliteToDTM(
      projectedFilePath,
      alignedFilePath,
      dtmInfo.bounds
    );
    
    if (!alignResult.success) {
      return { success: false, error: alignResult.error };
    }
    
    // Convert aligned TIFF to JPEG
    const alignedJpegFilename = `satellite_${dtmBasename}_aligned.jpg`;
    const alignedJpegPath = path.join(outputDir, alignedJpegFilename);
    
    console.log('📷 Converting to JPEG...');
    const jpegResult = await convertToJpeg(alignedFilePath, alignedJpegPath);
    
    if (!jpegResult.success) {
      return { success: false, error: jpegResult.error };
    }
    
    // Process for BeamNG: Center crop to 8K
    const crop8kFilename = `satellite_${dtmBasename}_8k_center.jpg`;
    const crop8kPath = path.join(outputDir, crop8kFilename);
    
    console.log('✂️ Center cropping to 8K...');
    const crop8kResult = await centerCropTo8K(alignedJpegPath, crop8kPath);
    
    if (!crop8kResult.success) {
      return { success: false, error: crop8kResult.error };
    }
    
    // Scale 8K to 4K for BeamNG
    const scale4kFilename = `satellite_${dtmBasename}_4k_center.jpg`;
    const scale4kPath = path.join(outputDir, scale4kFilename);
    
    console.log('📏 Scaling to 4K for BeamNG...');
    const scale4kResult = await scaleTo4K(crop8kPath, scale4kPath);
    
    if (!scale4kResult.success) {
      return { success: false, error: scale4kResult.error };
    }
    
    // Clean up intermediate files
    await fs.unlink(satelliteFilePath).catch(() => {}); // Original JPEG
    await fs.unlink(wgs84FilePath).catch(() => {}); // WGS84 TIFF
    await fs.unlink(projectedFilePath).catch(() => {}); // Projected TIFF
    
    console.log('✅ Complete DTM-matched satellite processing finished');
    console.log('📦 Generated files:');
    console.log(`   - ${alignedFilename} (10000x10000 TIFF)`);
    console.log(`   - ${alignedJpegFilename} (10000x10000 JPEG)`);
    console.log(`   - ${crop8kFilename} (8192x8192 JPEG)`);
    console.log(`   - ${scale4kFilename} (4096x4096 JPEG - BeamNG ready)`);
    
    return {
      success: true,
      filename: scale4kFilename, // Return the BeamNG-ready file as primary
      bounds: dtmInfo.bounds,
      projection: dtmInfo.projection,
      resolution: `${resolution} pixels/meter`,
      additionalFiles: {
        aligned: alignedFilename,
        alignedJpeg: alignedJpegFilename,
        crop8k: crop8kFilename,
        beamngReady: scale4kFilename
      }
    };
    
  } catch (error) {
    console.error('❌ Error downloading DTM-matched satellite imagery:', error);
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}

async function getDTMInfo(filePath: string): Promise<{
  success: boolean;
  error?: string;
  projection?: string;
  bounds?: { north: number; south: number; east: number; west: number };
  width?: number;
  height?: number;
  pixelSize?: { x: number; y: number };
}> {
  return new Promise((resolve) => {
    // Handle both local files and URLs with GDAL virtual file system
    const gdalPath = filePath.startsWith('http') ? `/vsicurl/${filePath}` : filePath;
    const child = spawn('gdalinfo', [gdalPath], { stdio: 'pipe' });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    child.on('close', (code) => {
      if (code !== 0) {
        resolve({ success: false, error: `gdalinfo failed: ${stderr}` });
        return;
      }
      
      try {
        // Parse gdalinfo output
        const lines = stdout.split('\n');
        
        // Get size
        const sizeLine = lines.find(line => line.startsWith('Size is'));
        const sizeMatch = sizeLine?.match(/Size is (\d+), (\d+)/);
        const width = sizeMatch ? parseInt(sizeMatch[1]) : 0;
        const height = sizeMatch ? parseInt(sizeMatch[2]) : 0;
        
        // Get pixel size
        const pixelSizeLine = lines.find(line => line.startsWith('Pixel Size'));
        const pixelSizeMatch = pixelSizeLine?.match(/Pixel Size = \(([^,]+),([^)]+)\)/);
        const pixelSizeX = pixelSizeMatch ? parseFloat(pixelSizeMatch[1]) : 1;
        const pixelSizeY = pixelSizeMatch ? parseFloat(pixelSizeMatch[2]) : -1;
        
        // Get projection - look for the UTM projection, not the base geographic CRS
        let projection = 'Unknown';
        
        // First try to find UTM zone projection
        const utmMatch = stdout.match(/PROJCRS\["([^"]*UTM[^"]*)"[\s\S]*?ID\["EPSG",(\d+)\]/);
        if (utmMatch) {
          projection = `EPSG:${utmMatch[2]}`;
        } else {
          // Fallback to any EPSG code
          const projectionMatch = stdout.match(/ID\["EPSG",(\d+)\]/);
          if (projectionMatch) {
            projection = `EPSG:${projectionMatch[1]}`;
          }
        }
        
        // Special handling for NAD83(CSRS) / UTM zone 10N
        if (stdout.includes('NAD83(CSRS)') && stdout.includes('UTM zone 10N')) {
          projection = 'EPSG:3157'; // NAD83(CSRS) / UTM zone 10N
        }
        
        // Get corner coordinates - look for UTM coordinates in parentheses
        const upperLeftMatch = stdout.match(/Upper Left\s+\(\s*([0-9.-]+),\s*([0-9.-]+)\)/);
        const lowerRightMatch = stdout.match(/Lower Right\s+\(\s*([0-9.-]+),\s*([0-9.-]+)\)/);
        
        if (!upperLeftMatch || !lowerRightMatch) {
          console.log('Debug - stdout:', stdout.substring(0, 1000));
          resolve({ success: false, error: 'Could not parse corner coordinates' });
          return;
        }
        
        const west = parseFloat(upperLeftMatch[1]);
        const north = parseFloat(upperLeftMatch[2]);
        const east = parseFloat(lowerRightMatch[1]);
        const south = parseFloat(lowerRightMatch[2]);
        
        console.log('Parsed coordinates:', { west, north, east, south });
        
        resolve({
          success: true,
          projection,
          bounds: { north, south, east, west },
          width,
          height,
          pixelSize: { x: pixelSizeX, y: pixelSizeY }
        });
        
      } catch (error) {
        resolve({ success: false, error: `Failed to parse gdalinfo output: ${error}` });
      }
    });
    
    child.on('error', (error) => {
      resolve({ success: false, error: `Failed to run gdalinfo: ${error.message}` });
    });
  });
}

async function transformBoundsToWGS84(
  bounds: { north: number; south: number; east: number; west: number },
  sourceSRS: string
): Promise<{
  success: boolean;
  error?: string;
  bounds?: { north: number; south: number; east: number; west: number };
}> {
  return new Promise((resolve) => {
    // Transform all four corners to WGS84
    const corners = [
      `${bounds.west} ${bounds.north}`, // Upper left
      `${bounds.east} ${bounds.north}`, // Upper right
      `${bounds.east} ${bounds.south}`, // Lower right
      `${bounds.west} ${bounds.south}`  // Lower left
    ];
    
    const child = spawn('gdaltransform', ['-s_srs', sourceSRS, '-t_srs', 'EPSG:4326'], {
      stdio: 'pipe'
    });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    child.on('close', (code) => {
      if (code !== 0) {
        resolve({ success: false, error: `gdaltransform failed: ${stderr}` });
        return;
      }
      
      try {
        const lines = stdout.trim().split('\n');
        if (lines.length !== 4) {
          resolve({ success: false, error: 'Unexpected gdaltransform output' });
          return;
        }
        
        const transformedCorners = lines.map(line => {
          const parts = line.split(' ');
          return { lng: parseFloat(parts[0]), lat: parseFloat(parts[1]) };
        });
        
        // Find the bounding box
        const lngs = transformedCorners.map(c => c.lng);
        const lats = transformedCorners.map(c => c.lat);
        
        const wgs84Bounds = {
          west: Math.min(...lngs),
          east: Math.max(...lngs),
          south: Math.min(...lats),
          north: Math.max(...lats)
        };
        
        resolve({ success: true, bounds: wgs84Bounds });
        
      } catch (error) {
        resolve({ success: false, error: `Failed to parse gdaltransform output: ${error}` });
      }
    });
    
    child.on('error', (error) => {
      resolve({ success: false, error: `Failed to run gdaltransform: ${error.message}` });
    });
    
    // Send all corner coordinates to stdin
    child.stdin?.write(corners.join('\n') + '\n');
    child.stdin?.end();
  });
}

async function downloadHighResSatelliteImagery(params: {
  bounds: { north: number; south: number; east: number; west: number };
  resolution: number;
  filename: string;
  outputDir: string;
  mapboxToken: string;
}): Promise<{ success: boolean; error?: string }> {
  // Use the existing high-resolution satellite download logic
  return downloadSatelliteImagery({
    bounds: params.bounds,
    center: {
      lat: (params.bounds.north + params.bounds.south) / 2,
      lng: (params.bounds.east + params.bounds.west) / 2
    },
    scale: Math.max(
      Math.abs(params.bounds.east - params.bounds.west) * 111.32, // Approximate km per degree longitude
      Math.abs(params.bounds.north - params.bounds.south) * 110.54  // Approximate km per degree latitude
    ),
    resolution: params.resolution,
    filename: params.filename,
    outputDir: params.outputDir,
    mapboxToken: params.mapboxToken
  });
}

async function georeferenceSatelliteImage(
  inputPath: string,
  outputPath: string,
  bounds: { north: number; south: number; east: number; west: number }
): Promise<{ success: boolean; error?: string }> {
  return new Promise(async (resolve) => {
    // Delete existing file if it exists (gdal_translate doesn't support -overwrite)
    try {
      await fs.unlink(outputPath);
      console.log('🗑️ Removed existing file:', outputPath);
    } catch (error) {
      // File doesn't exist, which is fine
    }
    
    const args = [
      '-a_srs', 'EPSG:4326',
      '-a_ullr', bounds.west.toString(), bounds.north.toString(), 
                bounds.east.toString(), bounds.south.toString(),
      inputPath,
      outputPath
    ];
    
    console.log('🌐 Georeferencing:', 'gdal_translate', args.join(' '));
    
    const child = spawn('gdal_translate', args, { stdio: 'pipe' });
    
    let stderr = '';
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        resolve({ success: true });
      } else {
        resolve({ success: false, error: `gdal_translate failed: ${stderr}` });
      }
    });
    
    child.on('error', (error) => {
      resolve({ success: false, error: `Failed to run gdal_translate: ${error.message}` });
    });
  });
}

async function transformSatelliteToMatchDTM(
  inputPath: string,
  outputPath: string,
  targetProjection: string
): Promise<{ success: boolean; error?: string }> {
  return new Promise((resolve) => {
    const args = [
      '-overwrite',               // Overwrite existing files
      '-t_srs', targetProjection, // Use explicit projection code
      '-tr', '1', '1',            // 1 meter pixel resolution to match DTM
      '-r', 'cubic',              // Use cubic resampling for better quality
      inputPath,
      outputPath
    ];
    
    console.log('🔄 Transforming projection:', 'gdalwarp', args.join(' '));
    
    const child = spawn('gdalwarp', args, { stdio: 'pipe' });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout?.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log('📥 gdalwarp progress:', output.trim());
    });
    
    child.stderr.on('data', (data) => {
      const output = data.toString();
      stderr += output;
      console.log('📥 gdalwarp stderr:', output.trim());
    });
    
    child.on('close', (code) => {
      console.log(`📋 gdalwarp finished with code: ${code}`);
      if (code === 0) {
        console.log('✅ Projection transformation completed');
        resolve({ success: true });
      } else {
        console.error('❌ Projection transformation failed');
        resolve({ success: false, error: `gdalwarp failed: ${stderr}` });
      }
    });
    
    child.on('error', (error) => {
      console.error('❌ Failed to start gdalwarp:', error);
      resolve({ success: false, error: `Failed to run gdalwarp: ${error.message}` });
    });
  });
}

// Align satellite to exact DTM bounds and dimensions
async function alignSatelliteToDTM(
  inputPath: string,
  outputPath: string,
  bounds: { north: number; south: number; east: number; west: number }
): Promise<{ success: boolean; error?: string }> {
  return new Promise((resolve) => {
    const args = [
      '-overwrite',               // Overwrite existing files
      '-te', bounds.west.toString(), bounds.south.toString(), bounds.east.toString(), bounds.north.toString(),
      '-ts', '10000', '10000',
      '-r', 'cubic',
      inputPath,
      outputPath
    ];
    
    console.log('📐 Aligning:', 'gdalwarp', args.join(' '));
    
    const child = spawn('gdalwarp', args, { stdio: 'pipe' });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout?.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log('📥 gdalwarp align progress:', output.trim());
    });
    
    child.stderr.on('data', (data) => {
      const output = data.toString();
      stderr += output;
      console.log('📥 gdalwarp align stderr:', output.trim());
    });
    
    child.on('close', (code) => {
      console.log(`📋 gdalwarp align finished with code: ${code}`);
      if (code === 0) {
        console.log('✅ DTM alignment completed');
        resolve({ success: true });
      } else {
        console.error('❌ DTM alignment failed');
        resolve({ success: false, error: `gdalwarp alignment failed: ${stderr}` });
      }
    });
    
    child.on('error', (error) => {
      console.error('❌ Failed to start gdalwarp align:', error);
      resolve({ success: false, error: `Failed to run gdalwarp: ${error.message}` });
    });
  });
}

// Convert TIFF to JPEG using oiiotool
async function convertToJpeg(
  inputPath: string,
  outputPath: string
): Promise<{ success: boolean; error?: string }> {
  return new Promise(async (resolve) => {
    // Delete existing file if it exists
    try {
      await fs.unlink(outputPath);
      console.log('🗑️ Removed existing file:', outputPath);
    } catch (error) {
      // File doesn't exist, which is fine
    }
    
    const args = [inputPath, '-o', outputPath];
    
    console.log('📷 Converting:', 'oiiotool', args.join(' '));
    
    const child = spawn('oiiotool', args, { stdio: 'pipe' });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout?.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log('📥 oiiotool convert:', output.trim());
    });
    
    child.stderr.on('data', (data) => {
      const output = data.toString();
      stderr += output;
      console.log('📥 oiiotool convert stderr:', output.trim());
    });
    
    child.on('close', (code) => {
      console.log(`📋 oiiotool convert finished with code: ${code}`);
      if (code === 0) {
        console.log('✅ JPEG conversion completed');
        resolve({ success: true });
      } else {
        console.error('❌ JPEG conversion failed');
        resolve({ success: false, error: `oiiotool conversion failed: ${stderr}` });
      }
    });
    
    child.on('error', (error) => {
      console.error('❌ Failed to start oiiotool convert:', error);
      resolve({ success: false, error: `Failed to run oiiotool: ${error.message}` });
    });
  });
}

// Center crop 10K image to 8K using oiiotool
async function centerCropTo8K(
  inputPath: string,
  outputPath: string
): Promise<{ success: boolean; error?: string }> {
  return new Promise(async (resolve) => {
    // Delete existing file if it exists
    try {
      await fs.unlink(outputPath);
      console.log('🗑️ Removed existing file:', outputPath);
    } catch (error) {
      // File doesn't exist, which is fine
    }
    
    // Offset calculation: (10000 - 8192) / 2 = 904
    const args = [inputPath, '--cut', '8192x8192+904+904', '-o', outputPath];
    
    console.log('✂️ Center cropping:', 'oiiotool', args.join(' '));
    
    const child = spawn('oiiotool', args, { stdio: 'pipe' });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout?.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log('📥 oiiotool crop:', output.trim());
    });
    
    child.stderr.on('data', (data) => {
      const output = data.toString();
      stderr += output;
      console.log('📥 oiiotool crop stderr:', output.trim());
    });
    
    child.on('close', (code) => {
      console.log(`📋 oiiotool crop finished with code: ${code}`);
      if (code === 0) {
        console.log('✅ Center crop to 8K completed');
        resolve({ success: true });
      } else {
        console.error('❌ Center crop failed');
        resolve({ success: false, error: `oiiotool center crop failed: ${stderr}` });
      }
    });
    
    child.on('error', (error) => {
      console.error('❌ Failed to start oiiotool crop:', error);
      resolve({ success: false, error: `Failed to run oiiotool: ${error.message}` });
    });
  });
}

// Scale 8K image to 4K using oiiotool
async function scaleTo4K(
  inputPath: string,
  outputPath: string
): Promise<{ success: boolean; error?: string }> {
  return new Promise(async (resolve) => {
    // Delete existing file if it exists
    try {
      await fs.unlink(outputPath);
      console.log('🗑️ Removed existing file:', outputPath);
    } catch (error) {
      // File doesn't exist, which is fine
    }
    
    const args = [inputPath, '--resize', '4096x4096', '-o', outputPath];
    
    console.log('📏 Scaling:', 'oiiotool', args.join(' '));
    
    const child = spawn('oiiotool', args, { stdio: 'pipe' });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout?.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log('📥 oiiotool scale:', output.trim());
    });
    
    child.stderr.on('data', (data) => {
      const output = data.toString();
      stderr += output;
      console.log('📥 oiiotool scale stderr:', output.trim());
    });
    
    child.on('close', (code) => {
      console.log(`📋 oiiotool scale finished with code: ${code}`);
      if (code === 0) {
        console.log('✅ Scale to 4K completed');
        resolve({ success: true });
      } else {
        console.error('❌ Scale to 4K failed');
        resolve({ success: false, error: `oiiotool scaling failed: ${stderr}` });
      }
    });
    
    child.on('error', (error) => {
      console.error('❌ Failed to start oiiotool scale:', error);
      resolve({ success: false, error: `Failed to run oiiotool: ${error.message}` });
    });
  });
}

async function queryElevation(lat: number, lng: number): Promise<number | null> {
  return new Promise((resolve) => {
    // Use gdallocationinfo to query elevation at the given coordinates
    // We'll look for SRTM files in the downloads directory
    const downloadsDir = path.join(process.cwd(), 'public', 'downloads');
    
    // First, try to find a SRTM file that covers this coordinate
    // Look for files with SRTMGL1 in the name and check if they cover the point
    fs.readdir(downloadsDir).then(files => {
      const srtmFile = files.find(file => 
        file.includes('SRTMGL1') && file.endsWith('.tif')
      );
      
      if (!srtmFile) {
        console.log('No SRTM file found for elevation query');
        resolve(null);
        return;
      }

      const filePath = path.join(downloadsDir, srtmFile);
      const args = [
        '-valonly',
        '-wgs84',
        filePath,
        lng.toString(),
        lat.toString()
      ];

      console.log('🔍 Querying elevation:', 'gdallocationinfo', args.join(' '));

      const child = spawn('gdallocationinfo', args, {
        stdio: 'pipe'
      });

      let stdout = '';
      let stderr = '';

      child.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        if (code === 0) {
          const elevation = parseFloat(stdout.trim());
          if (!Number.isNaN(elevation) && elevation !== -32768) { // -32768 is typical NoData value
            resolve(elevation);
          } else {
            resolve(null);
          }
        } else {
          console.error('❌ gdallocationinfo failed:', stderr);
          resolve(null);
        }
      });

      child.on('error', (error) => {
        console.error('❌ Failed to run gdallocationinfo:', error);
        resolve(null);
      });
    }).catch(error => {
      console.error('❌ Error reading downloads directory:', error);
      resolve(null);
    });
  });
}