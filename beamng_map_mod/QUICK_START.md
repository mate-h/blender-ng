# BC Coast Map Mod - Quick Start Guide

Get your BC Coast map mod installed in BeamNG.drive quickly!

## Prerequisites

- Python 3.6 or higher
- BeamNG.drive installed
- Your BC Coast map files ready

## Quick Installation

### Step 1: Set up the installation system

```bash
# Navigate to the beamng_map_mod directory
cd beamng_map_mod

# If you have your map files in a directory or zip file:
python3 setup.py --source /path/to/your/bc_coast/files

# Or if you want to copy files manually later:
python3 setup.py
```

### Step 2: Install the mod

```bash
# Install the mod (recommended)
python3 manage.py install

# Or force install if you want to overwrite existing installation
python3 manage.py install --force
```

### Step 3: Verify installation

```bash
# Check if the mod is installed correctly
python3 manage.py status
```

### Step 4: Launch BeamNG.drive

- Start BeamNG.drive
- Go to the level selection menu
- Look for "BC Coast" in the list
- Select and enjoy!

## Quick Commands Reference

```bash
# Install mod
python3 manage.py install

# Check status
python3 manage.py status

# Uninstall mod
python3 manage.py uninstall

# Package mod (create zip and update db.json)
python3 manage.py package

# Force install (overwrite existing)
python3 manage.py install --force

# Uninstall without backup
python3 manage.py uninstall --no-backup
```

## Troubleshooting

### "Source directory not found"
- Make sure your map files are in `beamng_map_mod/levels/bc_coast/`
- Required files: `info.json`, `mainLevel.lua`

### "Could not find BeamNG.drive user folder"
- The script will prompt you to enter the path manually
- Common locations:
  - macOS: `~/Library/Application Support/BeamNG.drive`
  - Windows: `%APPDATA%/BeamNG.drive`
  - Linux: `~/Documents/BeamNG.drive`

### Mod not appearing in BeamNG.drive
- Restart BeamNG.drive
- Check the status: `python3 manage.py status`
- Verify the mod is in the correct location

## File Structure After Installation

```
[BeamNG User Folder]/
├── mods/
│   └── repo/
│       └── bc_coast/
│           ├── levels/
│           │   └── bc_coast/          # Your map files
│           ├── mod_info/
│           │   └── BCCOAST/
│           │       ├── info.json      # Mod metadata
│           │       └── icon.jpg       # Mod icon
│           └── install.log            # Installation log
```

## Need Help?

- Check the full README.md for detailed documentation
- Run `python3 manage.py status` to diagnose issues
- Look at the installation log in the mod directory

## Next Steps

After installation, you can:
- Customize the mod by editing `config/mod_info.json`
- Create backups before making changes
- Use the management system for future updates