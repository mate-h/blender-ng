import type { Plugin } from 'vite';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs/promises';

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
    }
  };
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