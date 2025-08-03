#!/usr/bin/env tsx

/**
 * OpenTopography Data Downloader
 * Downloads topographic data from OpenTopography's Global API
 * 
 * Usage: tsx download-opentopography.ts
 */

import { promises as fs } from 'fs';
import path from 'path';

// OpenTopography API configuration
const API_KEY = 'f86a999f93f6c97a6d61c3812b1918bd';
const BASE_URL = 'https://portal.opentopography.org/API/globaldem';

// Available datasets
const DATASETS = {
  SRTMGL1: 'SRTM GL1 (30m)',
  SRTMGL3: 'SRTM GL3 (90m)', 
  ALOS: 'ALOS World 3D (30m)',
  NASADEM: 'NASADEM (30m)',
  COP30: 'Copernicus DEM 30m',
  COP90: 'Copernicus DEM 90m'
} as const;

// Output formats
const OUTPUT_FORMATS = {
  GTiff: 'GeoTIFF',
  AAIGrid: 'Arc ASCII Grid',
  HFA: 'Erdas Imagine'
} as const;

interface DownloadParams {
  demtype: keyof typeof DATASETS;
  south: number;
  north: number;
  west: number;
  east: number;
  outputFormat: keyof typeof OUTPUT_FORMATS;
  filename?: string;
  outputDir?: string;
}

class OpenTopographyDownloader {
  private apiKey: string;
  private baseUrl: string;

  constructor(apiKey: string, baseUrl: string = BASE_URL) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  /**
   * Build the API URL with parameters
   */
  private buildApiUrl(params: DownloadParams): string {
    const urlParams = new URLSearchParams({
      demtype: params.demtype,
      south: params.south.toString(),
      north: params.north.toString(),
      west: params.west.toString(),
      east: params.east.toString(),
      outputFormat: params.outputFormat,
      API_Key: this.apiKey
    });

    return `${this.baseUrl}?${urlParams.toString()}`;
  }

  /**
   * Download data from OpenTopography
   */
  async downloadData(params: DownloadParams): Promise<void> {
    const url = this.buildApiUrl(params);
    
    console.log(`Downloading ${DATASETS[params.demtype]} data...`);
    console.log(`Bounds: N:${params.north}, S:${params.south}, E:${params.east}, W:${params.west}`);
    console.log(`Format: ${OUTPUT_FORMATS[params.outputFormat]}`);
    console.log(`URL: ${url}`);
    
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'User-Agent': 'OpenTopography-TypeScript-Downloader/1.0'
        }
      });

      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        
        // Try to get more detailed error information from the response
        try {
          const contentType = response.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            const errorData = await response.json();
            if (errorData.error) {
              errorMessage += ` - ${errorData.error}`;
            }
          } else {
            const errorText = await response.text();
            if (errorText && errorText.length < 500) { // Avoid very long error messages
              errorMessage += ` - ${errorText}`;
            }
          }
        } catch (parseError) {
          // If we can't parse the error response, just use the status
          console.warn('Could not parse error response:', parseError);
        }
        
        throw new Error(errorMessage);
      }

      // Check content type
      const contentType = response.headers.get('content-type');
      console.log(`Content-Type: ${contentType}`);

      // Generate filename if not provided
      const extension = params.outputFormat === 'GTiff' ? 'tif' : 
                       params.outputFormat === 'AAIGrid' ? 'asc' : 'img';
      const filename = params.filename || 
        `opentopo_${params.demtype}_${params.south}_${params.north}_${params.west}_${params.east}.${extension}`;
      
      // Create output directory if specified
      const outputDir = params.outputDir || './downloads';
      await fs.mkdir(outputDir, { recursive: true });
      
      const filePath = path.join(outputDir, filename);

      // Download the file
      const buffer = Buffer.from(await response.arrayBuffer());
      await fs.writeFile(filePath, buffer);

      console.log(`✅ Successfully downloaded: ${filePath}`);
      console.log(`📏 File size: ${(buffer.length / 1024 / 1024).toFixed(2)} MB`);

    } catch (error) {
      console.error('❌ Download failed:', error);
      throw error;
    }
  }

  /**
   * Get elevation data for specific points (simplified point query)
   */
  async getElevation(lat: number, lon: number, dataset: keyof typeof DATASETS = 'SRTMGL1'): Promise<any> {
    // For point queries, we'll use a small bounding box around the point
    const buffer = 0.001; // ~100 meters
    const params: DownloadParams = {
      demtype: dataset,
      south: lat - buffer,
      north: lat + buffer,
      west: lon - buffer,
      east: lon + buffer,
      outputFormat: 'GTiff'
    };

    console.log(`Getting elevation for point: ${lat}, ${lon}`);
    
    try {
      await this.downloadData({
        ...params,
        filename: `elevation_${lat}_${lon}.tif`,
        outputDir: './point_queries'
      });
    } catch (error) {
      console.error('Failed to get elevation data:', error);
      throw error;
    }
  }

  /**
   * List available datasets
   */
  listDatasets(): void {
    console.log('\n📊 Available Datasets:');
    Object.entries(DATASETS).forEach(([key, value]) => {
      console.log(`  ${key}: ${value}`);
    });
  }

  /**
   * List available output formats
   */
  listFormats(): void {
    console.log('\n📋 Available Output Formats:');
    Object.entries(OUTPUT_FORMATS).forEach(([key, value]) => {
      console.log(`  ${key}: ${value}`);
    });
  }
}

// Example usage and testing
async function main() {
  const downloader = new OpenTopographyDownloader(API_KEY);
  
  console.log('🌍 OpenTopography Data Downloader');
  console.log('=' .repeat(50));
  
  // List available datasets and formats
  downloader.listDatasets();
  downloader.listFormats();
  
  console.log('\n🎯 Running test downloads...\n');
  
  try {
    // Example 1: Download SRTM data for a small area around Mount Rainier, WA
    console.log('📍 Test 1: Mount Rainier, WA area (SRTM 30m)');
    await downloader.downloadData({
      demtype: 'SRTMGL1',
      south: 46.8,
      north: 46.9,
      west: -121.8,
      east: -121.7,
      outputFormat: 'GTiff',
      filename: 'mount_rainier_srtm30m.tif'
    });

    console.log('\n📍 Test 2: Small area near San Francisco (Copernicus 30m)');
    await downloader.downloadData({
      demtype: 'COP30',
      south: 37.7,
      north: 37.8,
      west: -122.5,
      east: -122.4,
      outputFormat: 'GTiff',
      filename: 'san_francisco_cop30m.tif'
    });

    console.log('\n📍 Test 3: Point elevation query for Seattle Space Needle');
    await downloader.getElevation(47.6205, -122.3493, 'SRTMGL1');

    console.log('\n✅ All downloads completed successfully!');
    
  } catch (error) {
    console.error('❌ Error during download:', error);
    process.exit(1);
  }
}

// Run the main function if this script is executed directly
// Check if this is the main module using import.meta.url
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error('Unhandled error:', error);
    process.exit(1);
  });
}

export { OpenTopographyDownloader, DATASETS, OUTPUT_FORMATS };
export type { DownloadParams };