# BC Coast Map Mod - Python Installation System

A robust Python-based installation system for the BC Coast map mod for BeamNG.drive.

## Overview

This system provides a complete solution for installing, managing, and uninstalling the BC Coast map mod. It follows the proper BeamNG.drive mod structure and provides a user-friendly interface for mod management.

## Features

- **Automatic BeamNG.drive Detection**: Automatically finds your BeamNG.drive installation
- **Proper Mod Structure**: Installs the mod following BeamNG's official mod format
- **Backup System**: Creates backups before uninstalling
- **Status Checking**: Check if the mod is installed and get detailed information
- **Force Installation**: Overwrite existing installations when needed
- **Configuration Files**: Separate JSON configuration files for easy customization

## Prerequisites

- Python 3.6 or higher
- BeamNG.drive installed
- The BC Coast map files in the `levels/bc_coast/` directory

## Installation

### Using the Management Script (Recommended)

```bash
# Install the mod
python3 manage.py install

# Check status
python3 manage.py status

# Uninstall the mod
python3 manage.py uninstall

# Package the mod (create zip file for distribution)
python3 manage.py package
```

### Command Line Options

#### Management Script (`manage.py`)

```bash
# Basic usage
python3 manage.py <action>

# Available actions
python3 manage.py install     # Install the mod
python3 manage.py uninstall   # Uninstall the mod
python3 manage.py status      # Check mod status
python3 manage.py package     # Package mod (create zip file)

# Options
python3 manage.py install --force          # Force installation (no confirmation)
python3 manage.py uninstall --no-backup    # Skip backup creation
python3 manage.py install --mod-name mymap --version 2.0.0  # Custom mod name/version
```

## Features

- **Automatic BeamNG.drive Detection**: Automatically finds your BeamNG.drive installation
- **Proper Mod Structure**: Installs the mod following BeamNG's official mod format
- **Backup System**: Creates backups before uninstalling
- **Status Checking**: Verify installation status and details
- **Force Installation**: Overwrite existing installations when needed
- **Configuration Files**: Separate JSON configuration files for easy customization
- **Zip Creation**: Automatically creates zip files for distribution

## Configuration

### Mod Information (`config/mod_info.json`)

This file contains the metadata for the mod that appears in BeamNG.drive:

```json
{
    "title": "BC Coast",
    "tag_line": "BC Coast - A coastal driving map for BeamNG.drive",
    "message": "BC Coast is a coastal driving map for BeamNG.drive...",
    "version_string": "1.0.0",
    "resource_category_id": 9
}
```

### Installer Configuration (`config/installer_config.json`)

This file contains settings for the installer:

```json
{
    "mod_name": "bc_coast",
    "mod_version": "1.0.0",
    "mod_id": "BCCOAST",
    "required_files": ["info.json", "mainLevel.lua"],
    "optional_files": ["bc_coast_preview.jpg", "bc_coast_minimap.png"]
}
```

## BeamNG.drive Mod Structure

The installer creates the following structure in your BeamNG.drive installation:

```
[BeamNG User Folder]/
├── mods/
│   └── repo/
│       └── bc_coast/
│           ├── levels/
│           │   └── bc_coast/          # The actual map files
│           ├── mod_info/
│           │   └── BCCOAST/
│           │       ├── info.json      # Mod metadata
│           │       └── icon.jpg       # Mod icon
│           ├── bc_coast.zip           # Mod zip file
│           └── install.log            # Installation log
```

## Zip and Database Management

The system automatically:

1. **Creates Zip Files**: Generates a zip file containing the complete mod structure
2. **Updates db.json**: Automatically updates BeamNG's mod database with:
   - File hashes for integrity checking
   - Mod metadata and version information
   - Installation timestamps
   - Mod status and configuration

### Package Command

The `package` command creates a zip file and updates db.json without installing:

```bash
python3 manage.py package
```

This is useful for:
- Creating distribution packages
- Testing mod packaging
- Updating the database without installation
- Preparing mods for sharing

## Troubleshooting

### Common Issues

1. **"Source directory not found"**
   - Make sure the `levels/bc_coast/` directory exists in the same folder as the scripts
   - Ensure the directory contains the required files (`info.json`, `mainLevel.lua`)

2. **"Could not find BeamNG.drive user folder"**
   - The installer will prompt you to enter the path manually
   - Common locations:
     - Windows: `%APPDATA%/BeamNG.drive`
     - macOS: `~/Library/Application Support/BeamNG.drive`
     - Linux: `~/Documents/BeamNG.drive`

3. **"Mod directory already exists"**
   - Use the `--force` flag to overwrite: `python3 manage.py install --force`
   - Or manually remove the existing mod first

### Verification

After installation, you can verify the mod is working:

1. Check the status: `python3 manage.py status`
2. Look for the mod in BeamNG.drive's level selection menu
3. Check the installation log in the mod directory

## Development

### Adding New Features

1. **New Configuration Options**: Add them to `config/installer_config.json`
2. **Custom Mod Types**: Modify the `BeamNGModManager` class in `manage.py`
3. **Additional Validation**: Add validation methods to the manager classes

### Testing

```bash
# Test installation
python3 manage.py install --force

# Test status
python3 manage.py status

# Test uninstallation
python3 manage.py uninstall --force
```

## License

This installation system is provided as-is for personal use. Please respect BeamNG GmbH's intellectual property rights.

## Credits

- Based on the original small_island map by BeamNG GmbH
- Modified and renamed for BC Coast theme
- Python installation system created for robust mod management 