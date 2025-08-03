#!/usr/bin/env tsx

/**
 * Server-side OpenTopography downloader
 * Called by the Vite plugin to download terrain data
 * 
 * Usage: tsx download-server.ts --bounds '{"north":46.9,"south":46.8,"east":-121.7,"west":-121.8}' --filename 'terrain.tif' --output-dir './downloads'
 */

import { OpenTopographyDownloader } from './download-opentopography';
import { promises as fs } from 'fs';
import path from 'path';

// OpenTopography API key
const API_KEY = 'f86a999f93f6c97a6d61c3812b1918bd';

interface Bounds {
  north: number;
  south: number;
  east: number;
  west: number;
}

interface ServerDownloadParams {
  bounds: Bounds;
  filename: string;
  outputDir: string;
  dataset?: 'SRTMGL1' | 'SRTMGL3' | 'COP30' | 'COP90' | 'NASADEM' | 'ALOS';
  format?: 'GTiff' | 'AAIGrid' | 'HFA';
}

class ServerDownloader {
  private downloader: OpenTopographyDownloader;

  constructor(apiKey: string) {
    this.downloader = new OpenTopographyDownloader(apiKey);
  }

  async downloadTerrain(params: ServerDownloadParams): Promise<void> {
    const {
      bounds,
      filename,
      outputDir,
      dataset = 'SRTMGL1', // Default to SRTM 30m
      format = 'GTiff'     // Default to GeoTIFF
    } = params;

    console.log('🌍 Server-side terrain download starting...');
    console.log(`📍 Bounds: N:${bounds.north}, S:${bounds.south}, E:${bounds.east}, W:${bounds.west}`);
    console.log(`📁 Output: ${path.join(outputDir, filename)}`);
    console.log(`📊 Dataset: ${dataset} (30m SRTM)`);
    console.log(`📋 Format: ${format}`);

    try {
      // Ensure output directory exists
      await fs.mkdir(outputDir, { recursive: true });

      // Validate bounds
      if (bounds.north <= bounds.south || bounds.east <= bounds.west) {
        throw new Error('Invalid bounds: north must be > south, east must be > west');
      }

      // Check bounds are reasonable (not too large)
      const latDiff = bounds.north - bounds.south;
      const lngDiff = bounds.east - bounds.west;
      
      if (latDiff > 1.0 || lngDiff > 1.0) {
        console.warn('⚠️  Large area detected - this may take a while...');
      }

      if (latDiff > 5.0 || lngDiff > 5.0) {
        throw new Error('Area too large - please select a smaller region (max 5° x 5°)');
      }

      // Download the data
      await this.downloader.downloadData({
        demtype: dataset,
        south: bounds.south,
        north: bounds.north,
        west: bounds.west,
        east: bounds.east,
        outputFormat: format,
        filename: filename,
        outputDir: outputDir
      });

      // Verify the file was created
      const filePath = path.join(outputDir, filename);
      const stats = await fs.stat(filePath);
      
      console.log('✅ Download completed successfully!');
      console.log(`📏 File size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
      console.log(`📂 Location: ${filePath}`);

    } catch (error) {
      console.error('❌ Download failed:', error);
      throw error;
    }
  }
}

// Parse command line arguments
function parseArgs(): ServerDownloadParams {
  const args = process.argv.slice(2);
  const params: Partial<ServerDownloadParams> = {};

  for (let i = 0; i < args.length; i += 2) {
    const key = args[i];
    const value = args[i + 1];

    switch (key) {
      case '--bounds':
        try {
          params.bounds = JSON.parse(value);
        } catch (error) {
          throw new Error(`Invalid bounds JSON: ${value}`);
        }
        break;
      case '--filename':
        params.filename = value;
        break;
      case '--output-dir':
        params.outputDir = value;
        break;
      case '--dataset':
        params.dataset = value as any;
        break;
      case '--format':
        params.format = value as any;
        break;
      default:
        console.warn(`Unknown argument: ${key}`);
    }
  }

  // Validate required parameters
  if (!params.bounds) {
    throw new Error('Missing required parameter: --bounds');
  }
  if (!params.filename) {
    throw new Error('Missing required parameter: --filename');
  }
  if (!params.outputDir) {
    throw new Error('Missing required parameter: --output-dir');
  }

  return params as ServerDownloadParams;
}

// Main execution
async function main() {
  try {
    console.log('🚀 OpenTopography Server Downloader');
    console.log('=' .repeat(50));

    const params = parseArgs();
    const downloader = new ServerDownloader(API_KEY);
    
    await downloader.downloadTerrain(params);
    
    console.log('🎉 Server download completed successfully!');
    process.exit(0);

  } catch (error) {
    console.error('💥 Server download failed:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { ServerDownloader };