#!/usr/bin/env python3
"""
BC Coast Map Mod - Management Script
This script provides a unified interface for managing the BC Coast map mod
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from typing import Optional, Dict, Any
import argparse
import time


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class BeamNGModManager:
    """Unified manager for BeamNG map mods"""
    
    def __init__(self, mod_name: str = "bc_coast", mod_version: str = "1.0.0"):
        self.mod_name = mod_name
        self.mod_version = mod_version
        self.script_dir = Path(__file__).parent
        self.mod_id = "BCCOAST"
        
    def print_status(self, message: str):
        """Print a status message"""
        print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")
        
    def print_success(self, message: str):
        """Print a success message"""
        print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")
        
    def print_warning(self, message: str):
        """Print a warning message"""
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")
        
    def print_error(self, message: str):
        """Print an error message"""
        print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")
        
    def find_beamng_folder(self) -> Optional[Path]:
        """Find the BeamNG.drive user folder"""
        possible_paths = [
            Path.home() / "Documents" / "BeamNG.drive",
            Path.home() / "Library" / "Application Support" / "BeamNG.drive",
            Path(os.environ.get('APPDATA', '')) / "BeamNG.drive",
            Path("/Volumes/Goodboy/crossover/Steam/drive_c/users/crossover/AppData/Local/BeamNG.drive/0.36")
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
        
    def get_mod_status(self, beamng_folder: Path) -> Dict[str, Any]:
        """Get the current status of the mod"""
        mod_zip = beamng_folder / "mods" / "repo" / f"{self.mod_name}.zip"
        install_log = beamng_folder / "mods" / "repo" / f"{self.mod_name}_install.log"
        
        status = {
            "installed": False,
            "mod_zip": None,
            "version": None,
            "install_date": None,
            "file_size": None
        }
        
        # Check if installed as zip file
        if mod_zip.exists():
            status["installed"] = True
            status["mod_zip"] = str(mod_zip)
            status["file_size"] = mod_zip.stat().st_size
            
            # Check install log for version and date
            if install_log.exists():
                try:
                    with open(install_log, 'r') as f:
                        log_content = f.read()
                        for line in log_content.split('\n'):
                            if line.startswith("Mod Version:"):
                                status["version"] = line.split(":", 1)[1].strip()
                            elif line.startswith("Installation Date:"):
                                date_str = line.split(":", 1)[1].strip()
                                try:
                                    status["install_date"] = int(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S")))
                                except:
                                    pass
                except:
                    pass
            
        return status
        
    def create_mod_zip(self, source_dir: Path, output_path: Path) -> bool:
        """Create a zip file of the mod"""
        try:
            self.print_status(f"Creating mod zip file: {output_path}")
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in source_dir.rglob("*"):
                    if file_path.is_file():
                        # Get relative path from source directory
                        relative_path = file_path.relative_to(source_dir)
                        zipf.write(file_path, relative_path)
                        
            self.print_success(f"Mod zip created successfully: {output_path}")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to create zip file: {str(e)}")
            return False
        
    def validate_source_directory(self) -> bool:
        """Validate that the source directory contains the required files"""
        levels_dir = self.script_dir / "levels" / self.mod_name
        if not levels_dir.exists():
            self.print_error(f"Source directory not found: {levels_dir}")
            return False
            
        required_files = ["info.json", "mainLevel.lua"]
        for file in required_files:
            if not (levels_dir / file).exists():
                self.print_error(f"Required file not found: {levels_dir / file}")
                return False
                
        return True
        
    def install_mod(self, beamng_folder: Path, force: bool = False) -> bool:
        """Install the mod to the BeamNG folder"""
        try:
            # Check if zip file exists
            zip_source = self.script_dir / f"{self.mod_name}.zip"
            if not zip_source.exists():
                self.print_error(f"Zip file not found: {zip_source}")
                self.print_status("Run 'python3 manage.py package' first to create the zip file")
                return False
            
            # Create mod repository directory
            mods_repo_dir = beamng_folder / "mods" / "repo"
            mods_repo_dir.mkdir(parents=True, exist_ok=True)
            
            # Target zip file location
            target_zip = mods_repo_dir / f"{self.mod_name}.zip"
            
            # Check if mod already exists
            if target_zip.exists() and not force:
                self.print_warning(f"Mod zip file already exists: {target_zip}")
                response = input("Do you want to overwrite it? (y/N): ")
                if response.lower() != 'y':
                    self.print_status("Installation cancelled")
                    return False
                    
            # Copy zip file to target location
            self.print_status(f"Installing mod zip file: {self.mod_name}.zip")
            shutil.copy2(zip_source, target_zip)
            
            # Create installation log
            install_log = mods_repo_dir / f"{self.mod_name}_install.log"
            with open(install_log, 'w') as f:
                f.write("BC Coast Map Mod Installation Log\n")
                f.write("=================================\n")
                f.write(f"Installation Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Mod Version: {self.mod_version}\n")
                f.write(f"BeamNG Folder: {beamng_folder}\n")
                f.write(f"Source Zip: {zip_source}\n")
                f.write(f"Target Zip: {target_zip}\n")
                
            # Verify installation
            self.print_status("Verifying installation...")
            if target_zip.exists():
                self.print_success("BC Coast map installed successfully!")
                print()
                print("Installation Details:")
                print(f"  - Mod Location: {target_zip}")
                print(f"  - Level Name: {self.mod_name}")
                print(f"  - Version: {self.mod_version}")
                print(f"  - File Size: {target_zip.stat().st_size / (1024*1024):.1f} MB")
                print()
                print("The map should now appear in your BeamNG.drive level selection menu.")
                print("Restart BeamNG.drive if it's currently running.")
                print()
                print(f"Installation log saved to: {install_log}")
                
                return True
            else:
                self.print_error("Installation verification failed!")
                return False
                
        except Exception as e:
            self.print_error(f"Installation failed: {str(e)}")
            return False
            
    def uninstall_mod(self, beamng_folder: Path, force: bool = False, backup: bool = True) -> bool:
        """Uninstall the mod from the BeamNG folder"""
        try:
            mod_zip = beamng_folder / "mods" / "repo" / f"{self.mod_name}.zip"
            install_log = beamng_folder / "mods" / "repo" / f"{self.mod_name}_install.log"
            
            # Check if mod exists
            if not mod_zip.exists():
                self.print_warning(f"Mod '{self.mod_name}.zip' not found in BeamNG installation")
                return True  # Not an error if mod doesn't exist
                
            # Create backup if requested
            if backup and mod_zip.exists():
                backup_dir = self.script_dir / f"backup_{self.mod_name}_{int(time.time())}"
                backup_dir.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(mod_zip, backup_dir / f"{self.mod_name}.zip")
                    if install_log.exists():
                        shutil.copy2(install_log, backup_dir / f"{self.mod_name}_install.log")
                    self.print_success(f"Backup created at: {backup_dir}")
                except Exception as e:
                    self.print_warning(f"Failed to create backup: {str(e)}")
                    
            # Confirm uninstallation
            if not force:
                response = input(f"Are you sure you want to uninstall '{self.mod_name}'? (y/N): ")
                if response.lower() != 'y':
                    self.print_status("Uninstallation cancelled")
                    return True
                    
            # Remove mod zip file
            if mod_zip.exists():
                self.print_status("Removing mod zip file...")
                mod_zip.unlink()
                
            # Remove install log if it exists
            if install_log.exists():
                self.print_status("Removing install log...")
                install_log.unlink()
                
            self.print_success(f"Mod '{self.mod_name}' uninstalled successfully!")
            return True
            
        except Exception as e:
            self.print_error(f"Uninstallation failed: {str(e)}")
            return False
            
    def show_status(self, beamng_folder: Path):
        """Show the current status of the mod"""
        status = self.get_mod_status(beamng_folder)
        
        print("BC Coast Map Mod - Status")
        print("=========================")
        print()
        
        if status["installed"]:
            self.print_success("Mod is installed")
            print(f"  - Version: {status['version'] or 'Unknown'}")
            if status["mod_zip"]:
                print(f"  - Mod Zip: {status['mod_zip']}")
            if status["file_size"]:
                file_size_mb = status["file_size"] / (1024 * 1024)
                print(f"  - File Size: {file_size_mb:.1f} MB")
            if status["install_date"]:
                install_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status["install_date"]))
                print(f"  - Install Date: {install_date}")
        else:
            self.print_warning("Mod is not installed")
            
        print()
        
    def run(self, action: str, force: bool = False, backup: bool = True):
        """Run the specified action"""
        print("BC Coast Map Mod - Manager")
        print("==========================")
        
        # Execute action
        if action == "install":
            # Find BeamNG folder
            self.print_status("Looking for BeamNG.drive installation...")
            beamng_folder = self.find_beamng_folder()
            
            if not beamng_folder:
                self.print_error("Could not find BeamNG.drive user folder automatically.")
                user_path = input("Please enter the path to your BeamNG.drive user folder: ")
                beamng_folder = Path(user_path)
                
                if not beamng_folder.exists():
                    self.print_error(f"Invalid path: {beamng_folder}")
                    return False
                    
            self.print_success(f"Found BeamNG folder: {beamng_folder}")
            
            if not self.validate_source_directory():
                return False
            return self.install_mod(beamng_folder, force)
            
        elif action == "uninstall":
            # Find BeamNG folder
            self.print_status("Looking for BeamNG.drive installation...")
            beamng_folder = self.find_beamng_folder()
            
            if not beamng_folder:
                self.print_error("Could not find BeamNG.drive user folder automatically.")
                user_path = input("Please enter the path to your BeamNG.drive user folder: ")
                beamng_folder = Path(user_path)
                
                if not beamng_folder.exists():
                    self.print_error(f"Invalid path: {beamng_folder}")
                    return False
                    
            self.print_success(f"Found BeamNG folder: {beamng_folder}")
            
            return self.uninstall_mod(beamng_folder, force, backup)
            
        elif action == "status":
            # Find BeamNG folder
            self.print_status("Looking for BeamNG.drive installation...")
            beamng_folder = self.find_beamng_folder()
            
            if not beamng_folder:
                self.print_error("Could not find BeamNG.drive user folder automatically.")
                user_path = input("Please enter the path to your BeamNG.drive user folder: ")
                beamng_folder = Path(user_path)
                
                if not beamng_folder.exists():
                    self.print_error(f"Invalid path: {beamng_folder}")
                    return False
                    
            self.print_success(f"Found BeamNG folder: {beamng_folder}")
            
            self.show_status(beamng_folder)
            return True
            
        elif action == "package":
            # Package the mod without installing
            if not self.validate_source_directory():
                return False
                
            self.print_status("Packaging mod...")
            
            # Create temporary mod directory
            temp_mod_dir = self.script_dir / f"temp_{self.mod_name}"
            if temp_mod_dir.exists():
                shutil.rmtree(temp_mod_dir)
                
            # Create mod structure
            temp_mod_dir.mkdir()
            (temp_mod_dir / "levels").mkdir()
            (temp_mod_dir / "mod_info").mkdir()
            
            # Copy level files
            source_level_dir = self.script_dir / "levels" / self.mod_name
            target_level_dir = temp_mod_dir / "levels" / self.mod_name
            shutil.copytree(source_level_dir, target_level_dir)
            
            # Create mod info
            mod_info_dir = temp_mod_dir / "mod_info" / self.mod_id
            mod_info_dir.mkdir(parents=True, exist_ok=True)
            
            # Load and update mod info JSON
            config_file = self.script_dir / "config" / "mod_info.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    mod_info = json.load(f)
            else:
                mod_info = {}
                
            # Update timestamps
            mod_info["last_update"] = int(time.time())
            mod_info["resource_date"] = int(time.time())
            mod_info["version_string"] = self.mod_version
            mod_info["via"] = f"packed by local installer on {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            with open(mod_info_dir / "info.json", 'w') as f:
                json.dump(mod_info, f, indent=4)
                
            # Copy preview image as icon if available
            preview_source = source_level_dir / f"{self.mod_name}_preview.jpg"
            if preview_source.exists():
                shutil.copy2(preview_source, mod_info_dir / "icon.jpg")
                self.print_status("Copied preview image as mod icon")
            else:
                self.print_warning("No preview image found for mod icon")
                
            # Create zip file
            zip_path = self.script_dir / f"{self.mod_name}.zip"
            if self.create_mod_zip(temp_mod_dir, zip_path):
                self.print_success(f"Mod packaged successfully: {zip_path}")
                    
                # Clean up temp directory
                shutil.rmtree(temp_mod_dir)
                return True
            else:
                self.print_error("Failed to package mod")
                if temp_mod_dir.exists():
                    shutil.rmtree(temp_mod_dir)
                return False
                
        else:
            self.print_error(f"Unknown action: {action}")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Manage BC Coast map mod for BeamNG.drive")
    parser.add_argument("action", choices=["install", "uninstall", "status", "package"],
                       help="Action to perform")
    parser.add_argument("--force", "-f", action="store_true", 
                       help="Force operation without confirmation")
    parser.add_argument("--no-backup", action="store_true",
                       help="Skip creating backup before uninstallation")
    parser.add_argument("--mod-name", default="bc_coast",
                       help="Name of the mod (default: bc_coast)")
    parser.add_argument("--version", default="1.0.0",
                       help="Mod version (default: 1.0.0)")
    
    args = parser.parse_args()
    
    manager = BeamNGModManager(args.mod_name, args.version)
    success = manager.run(args.action, args.force, not args.no_backup)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 