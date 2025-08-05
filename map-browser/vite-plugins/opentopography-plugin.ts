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