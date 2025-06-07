#!/usr/bin/env python3
"""
BeamNG Blender Addon Installation Script

This script provides convenient ways to install and manage the addon
for development and testing purposes.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

def get_blender_addon_paths():
    """Get potential Blender addon installation paths for different OS"""
    system = platform.system()
    paths = []
    
    if system == "Darwin":  # macOS
        # Standard Blender installations
        paths.extend([
            os.path.expanduser("~/Library/Application Support/Blender/*/scripts/addons/"),
            "/Applications/Blender.app/Contents/Resources/*/scripts/addons/",
        ])
    elif system == "Windows":
        # Windows paths
        paths.extend([
            os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender\\*\\scripts\\addons\\"),
            "C:\\Program Files\\Blender Foundation\\Blender\\*\\scripts\\addons\\",
        ])
    elif system == "Linux":
        # Linux paths
        paths.extend([
            os.path.expanduser("~/.config/blender/*/scripts/addons/"),
            "/usr/share/blender/*/scripts/addons/",
        ])
    
    return paths

def find_blender_addon_directory():
    """Find the actual Blender addon directory, preferring newer versions"""
    import glob
    
    potential_paths = get_blender_addon_paths()
    found_paths = []
    
    for path_pattern in potential_paths:
        matches = glob.glob(path_pattern)
        for path in matches:
            if os.path.exists(path) and os.access(path, os.W_OK):
                found_paths.append(path)
    
    if not found_paths:
        return None
    
    # Sort paths to prefer newer Blender versions (4.x over 3.x, etc.)
    def version_key(path):
        import re
        version_match = re.search(r'(\d+)\.(\d+)', path)
        if version_match:
            major, minor = map(int, version_match.groups())
            return (major, minor)
        return (0, 0)
    
    found_paths.sort(key=version_key, reverse=True)
    return found_paths[0]

def install_addon(source_dir, target_dir, addon_name="beamng_blender_addon"):
    """Install the addon by copying files"""
    source_path = os.path.join(source_dir, addon_name)
    target_path = os.path.join(target_dir, addon_name)
    
    # Remove existing installation
    if os.path.exists(target_path):
        print(f"Removing existing addon at: {target_path}")
        shutil.rmtree(target_path)
    
    # Copy addon files
    print(f"Installing addon from: {source_path}")
    print(f"Installing addon to: {target_path}")
    shutil.copytree(source_path, target_path)
    
    print("✅ Addon installed successfully!")
    print("\nTo enable the addon in Blender:")
    print("1. Open Blender")
    print("2. Go to Edit > Preferences > Add-ons")
    print("3. Search for 'BeamNG'")
    print("4. Enable the 'BeamNG.drive Level Importer/Exporter' addon")

def create_symlink(source_dir, target_dir, addon_name="beamng_blender_addon"):
    """Create a symbolic link for development (allows live editing)"""
    source_path = os.path.join(source_dir, addon_name)
    target_path = os.path.join(target_dir, addon_name)
    
    # Remove existing installation/link
    if os.path.exists(target_path):
        if os.path.islink(target_path):
            os.unlink(target_path)
        else:
            shutil.rmtree(target_path)
    
    # Create symbolic link
    print(f"Creating symlink from: {source_path}")
    print(f"Creating symlink to: {target_path}")
    
    try:
        os.symlink(source_path, target_path)
        print("✅ Development symlink created successfully!")
        print("🔄 Changes to the addon will be reflected immediately in Blender")
    except OSError as e:
        print(f"❌ Failed to create symlink: {e}")
        print("Falling back to file copy installation...")
        install_addon(source_dir, target_dir, addon_name)

def package_addon(source_dir, output_dir, addon_name="beamng_blender_addon"):
    """Package the addon as a .zip file for distribution"""
    import zipfile
    
    source_path = os.path.join(source_dir, addon_name)
    zip_filename = f"{addon_name}.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    
    print(f"Packaging addon: {source_path}")
    print(f"Output package: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if not file.endswith('.pyc') and not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    print(f"✅ Addon packaged successfully: {zip_path}")
    return zip_path

def main():
    """Main installation function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Install BeamNG Blender Addon")
    parser.add_argument("--dev", action="store_true", help="Install as development symlink")
    parser.add_argument("--package", action="store_true", help="Package addon as .zip")
    parser.add_argument("--target", help="Specify target Blender addon directory")
    parser.add_argument("--source", default=".", help="Source directory (default: current)")
    
    args = parser.parse_args()
    
    # Get source and target directories
    source_dir = os.path.abspath(args.source)
    addon_source = os.path.join(source_dir, "beamng_blender_addon")
    
    # Check if addon source exists
    if not os.path.exists(addon_source):
        print(f"❌ Addon source not found: {addon_source}")
        print("Make sure you're running this script from the project root directory")
        sys.exit(1)
    
    if args.package:
        # Package addon
        output_dir = os.path.join(source_dir, "dist")
        os.makedirs(output_dir, exist_ok=True)
        package_addon(source_dir, output_dir)
        return
    
    # Find target directory
    if args.target:
        target_dir = args.target
    else:
        target_dir = find_blender_addon_directory()
        if not target_dir:
            print("❌ Could not find Blender addon directory automatically")
            print("Please specify target directory with --target option")
            print("\nBlender addon directories are typically located at:")
            for path in get_blender_addon_paths():
                print(f"  {path}")
            sys.exit(1)
    
    print(f"Using Blender addon directory: {target_dir}")
    
    # Install addon
    if args.dev:
        create_symlink(source_dir, target_dir)
    else:
        install_addon(source_dir, target_dir)
    
    print("\n📋 Next steps:")
    print("1. (Re)start Blender")
    print("2. Go to Edit > Preferences > Add-ons")
    print("3. Search for 'BeamNG' and enable the addon")
    print("4. Look for the 'BeamNG' tab in the 3D Viewport sidebar (N key)")

if __name__ == "__main__":
    main() 