# OpenTopography Data Downloader

This TypeScript script downloads elevation data from [OpenTopography](https://opentopography.org/)'s Global API service.

## Files

- `download-opentopography.ts` - Main downloader class and functionality
- `example-usage.ts` - Example usage scenarios
- `downloads/` - Directory where downloaded files are saved
- `point_queries/` - Directory for point elevation queries

## Prerequisites

- Node.js with TypeScript support
- `tsx` package for running TypeScript directly
- Valid OpenTopography API key

## Installation

```bash
# Install tsx globally if you haven't already
npm install -g tsx

# Or run with npx
npx tsx download-opentopography.ts
```

## Usage

### Basic Usage

```bash
# Run the main script with test downloads
tsx download-opentopography.ts

# Run the example usage scenarios
tsx example-usage.ts
```

### Programmatic Usage

```typescript
import { OpenTopographyDownloader } from './download-opentopography.js';

const downloader = new OpenTopographyDownloader('your-api-key-here');

// Download terrain data for a specific area
await downloader.downloadData({
  demtype: 'SRTMGL1',        // Dataset type
  south: 37.7,               // Southern boundary (degrees)
  north: 37.8,               // Northern boundary (degrees)  
  west: -122.5,              // Western boundary (degrees)
  east: -122.4,              // Eastern boundary (degrees)
  outputFormat: 'GTiff',     // Output format
  filename: 'my_terrain.tif' // Optional filename
});
```

## Available Datasets

| Dataset | Description | Resolution |
|---------|-------------|------------|
| `SRTMGL1` | SRTM GL1 | 30m |
| `SRTMGL3` | SRTM GL3 | 90m |
| `ALOS` | ALOS World 3D | 30m |
| `NASADEM` | NASADEM | 30m |
| `COP30` | Copernicus DEM | 30m |
| `COP90` | Copernicus DEM | 90m |

## Output Formats

| Format | Description | Extension |
|--------|-------------|-----------|
| `GTiff` | GeoTIFF | `.tif` |
| `AAIGrid` | Arc ASCII Grid | `.asc` |
| `HFA` | Erdas Imagine | `.img` |

## API Key

The script uses the API key: `f86a999f93f6c97a6d61c3812b1918bd`

For production use, you should:
1. Get your own API key from [OpenTopography](https://portal.opentopography.org/)
2. Set it as an environment variable
3. Use it responsibly according to OpenTopography's terms of service

## Examples

### Example 1: Mount Rainier Area
```typescript
await downloader.downloadData({
  demtype: 'SRTMGL1',
  south: 46.8,
  north: 46.9,
  west: -121.8,
  east: -121.7,
  outputFormat: 'GTiff',
  filename: 'mount_rainier.tif'
});
```

### Example 2: European Alps
```typescript
await downloader.downloadData({
  demtype: 'COP30',
  south: 45.8,
  north: 46.0,
  west: 7.6,
  east: 7.8,
  outputFormat: 'GTiff',
  filename: 'alps.tif'
});
```

## Tips

- Use smaller areas (< 0.2 degrees) for faster downloads
- SRTMGL1 has global coverage and is reliable
- GeoTIFF format is recommended for GIS applications
- Check file sizes - larger areas take longer to process

## Error Handling

The script includes comprehensive error handling:
- HTTP errors are caught and reported
- File system errors are handled gracefully
- Invalid parameters are validated

## License

This script is provided as-is for educational and research purposes. Please follow OpenTopography's terms of service when using their API.