#!/usr/bin/env tsx

/**
 * Example usage of the OpenTopography Data Downloader
 * 
 * Usage: tsx example-usage.ts
 */

import { OpenTopographyDownloader, DATASETS, OUTPUT_FORMATS } from './download-opentopography.js';

async function exampleUsage() {
  const API_KEY = 'f86a999f93f6c97a6d61c3812b1918bd';
  const downloader = new OpenTopographyDownloader(API_KEY);

  console.log('🌍 OpenTopography Example Usage');
  console.log('=' .repeat(40));

  try {
    // Example 1: Download terrain data for Yosemite Valley
    console.log('\n📍 Downloading Yosemite Valley terrain data...');
    await downloader.downloadData({
      demtype: 'SRTMGL1',
      south: 37.7,
      north: 37.8,
      west: -119.7,
      east: -119.6,
      outputFormat: 'GTiff',
      filename: 'yosemite_valley.tif'
    });

    // Example 2: Download Copernicus data for the Alps
    console.log('\n📍 Downloading Alps terrain data (Copernicus 30m)...');
    await downloader.downloadData({
      demtype: 'COP30',
      south: 45.8,
      north: 46.0,
      west: 7.6,
      east: 7.8,
      outputFormat: 'GTiff',
      filename: 'alps_matterhorn.tif'
    });

    // Example 3: Download in ASCII Grid format
    console.log('\n📍 Downloading Death Valley in ASCII Grid format...');
    await downloader.downloadData({
      demtype: 'SRTMGL1',
      south: 36.2,
      north: 36.4,
      west: -117.2,
      east: -117.0,
      outputFormat: 'AAIGrid',
      filename: 'death_valley.asc'
    });

    console.log('\n✅ All example downloads completed!');
    console.log('\n💡 Tips:');
    console.log('  - Use smaller areas (< 0.2 degrees) for faster downloads');
    console.log('  - SRTMGL1 has global coverage at 30m resolution');
    console.log('  - COP30/COP90 offer more recent data where available');
    console.log('  - GTiff format is recommended for GIS applications');

  } catch (error) {
    console.error('❌ Error:', error);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  exampleUsage();
}