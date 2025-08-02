# BC Coast Map Mod - Changelog

## Version 2.0.0 - Enhanced Mod Manager

### New Features

#### 🎯 **Unified Mod Manager**
- **Consolidated Scripts**: Removed separate `install.py` and `uninstall.py` scripts
- **Single Management Interface**: All operations now handled through `manage.py`
- **Improved Error Handling**: Better error messages and recovery

#### 📦 **Zip Creation & Distribution**
- **Automatic Zip Generation**: Creates zip files during installation and packaging
- **Proper Mod Structure**: Zip files contain the complete mod structure
- **Distribution Ready**: Zip files can be shared or distributed

#### 🗄️ **Database Management**
- **Automatic db.json Updates**: Updates BeamNG's mod database automatically
- **File Hash Generation**: Creates MD5 hashes for all mod files
- **Mod Metadata**: Stores complete mod information in the database
- **Integrity Checking**: File hashes enable integrity verification

#### 🔧 **New Commands**
- **`package`**: Create zip file and update db.json without installing
- **Enhanced `status`**: More detailed status information
- **Improved `install`**: Now includes zip creation and db.json updates

### Technical Improvements

#### **File Hash System**
- MD5 hash generation for all mod files
- Windows-style path conversion for BeamNG compatibility
- Hash storage in db.json for integrity checking

#### **Database Integration**
- Automatic db.json loading and saving
- Mod entry creation with complete metadata
- Timestamp management and version tracking

#### **Zip File Management**
- Proper directory structure preservation
- Compression optimization
- Temporary directory cleanup

### Updated File Structure

```
beamng_map_mod/
├── manage.py               # Unified management script
├── setup.py                # Setup helper script
├── config/
│   ├── mod_info.json       # Mod metadata configuration
│   └── installer_config.json # Installer settings
├── levels/
│   └── bc_coast/           # The actual map files
├── 0.36/mods/db.json       # BeamNG mod database (auto-updated)
├── bc_coast.zip            # Generated mod zip file
└── README.md               # Documentation
```

### Usage Examples

```bash
# Install mod (includes zip creation and db.json update)
python3 manage.py install

# Package mod without installing
python3 manage.py package

# Check detailed status
python3 manage.py status

# Uninstall with backup
python3 manage.py uninstall
```

### Database Schema

The system now automatically updates `db.json` with:

```json
{
  "mods": {
    "bc_coast": {
      "active": true,
      "dateAdded": 1754118333,
      "dirname": "/mods/repo/",
      "filename": "bc_coast.zip",
      "fullpath": "/mods/repo/bc_coast.zip",
      "modData": {
        "attachments": [],
        "category_title": "Maps",
        "current_version_id": 1,
        "download_count": 0,
        "filename": "bc_coast.zip",
        "hashes": [
          ["file1.json", "hash1"],
          ["file2.lua", "hash2"]
        ],
        "last_update": 1754118333,
        "message": "BC Coast map description...",
        "path": "BCCOAST/1/",
        "rating_avg": 0,
        "rating_count": 0,
        "rating_sum": 0,
        "resource_category_id": 9,
        "resource_date": 1754118333,
        "resource_id": 999999,
        "review_count": 0,
        "tag_line": "BC Coast - A coastal driving map",
        "title": "BC Coast",
        "update_count": 0,
        "user_id": 0,
        "username": "local_mod",
        "version_string": "1.0.0"
      }
    }
  }
}
```

### Benefits

1. **Professional Distribution**: Zip files ready for sharing
2. **Database Integration**: Proper BeamNG mod database management
3. **Integrity Checking**: File hashes for verification
4. **Simplified Workflow**: Single command for all operations
5. **Better Documentation**: Comprehensive status reporting

### Migration Notes

- Old separate scripts (`install.py`, `uninstall.py`) are no longer needed
- All functionality now available through `manage.py`
- Database updates are automatic and transparent
- Zip files are created automatically during installation

### Future Enhancements

- Mod versioning and update system
- Automatic mod validation
- Network distribution capabilities
- Mod dependency management 