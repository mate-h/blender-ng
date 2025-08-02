#!/usr/bin/env python3
"""
BC Coast Map Mod - Setup Script
This script helps set up the installation system and prepare map files
"""

import os
import sys
import shutil
from pathlib import Path
import argparse


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class SetupManager:
    """Handles setup of the BC Coast map mod installation system"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.levels_dir = self.script_dir / "levels"
        self.bc_coast_dir = self.levels_dir / "bc_coast"
        
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
        
    def create_directory_structure(self):
        """Create the necessary directory structure"""
        self.print_status("Creating directory structure...")
        
        # Create levels directory
        self.levels_dir.mkdir(exist_ok=True)
        self.print_success(f"Created directory: {self.levels_dir}")
        
        # Create bc_coast directory
        self.bc_coast_dir.mkdir(exist_ok=True)
        self.print_success(f"Created directory: {self.bc_coast_dir}")
        
    def copy_map_files(self, source_path: Path):
        """Copy map files from source to the levels directory"""
        if not source_path.exists():
            self.print_error(f"Source path does not exist: {source_path}")
            return False
            
        self.print_status(f"Copying map files from: {source_path}")
        
        try:
            # If source is a file (zip), extract it
            if source_path.is_file() and source_path.suffix == '.zip':
                import zipfile
                with zipfile.ZipFile(source_path, 'r') as zip_ref:
                    zip_ref.extractall(self.bc_coast_dir)
                self.print_success("Extracted zip file successfully")
            else:
                # If source is a directory, copy it
                if self.bc_coast_dir.exists():
                    shutil.rmtree(self.bc_coast_dir)
                shutil.copytree(source_path, self.bc_coast_dir)
                self.print_success("Copied directory successfully")
                
            return True
            
        except Exception as e:
            self.print_error(f"Failed to copy files: {str(e)}")
            return False
            
    def validate_setup(self):
        """Validate that the setup is complete"""
        self.print_status("Validating setup...")
        
        required_files = ["info.json", "mainLevel.lua"]
        missing_files = []
        
        for file in required_files:
            if not (self.bc_coast_dir / file).exists():
                missing_files.append(file)
                
        if missing_files:
            self.print_error(f"Missing required files: {', '.join(missing_files)}")
            return False
            
        self.print_success("Setup validation passed!")
        return True
        
    def show_instructions(self):
        """Show next steps for the user"""
        print()
        print("=" * 50)
        print("SETUP COMPLETE!")
        print("=" * 50)
        print()
        print("Next steps:")
        print("1. Verify your map files are in: beamng_map_mod/levels/bc_coast/")
        print("2. Install the mod:")
        print("   python3 manage.py install")
        print("3. Check the status:")
        print("   python3 manage.py status")
        print("4. If you need to uninstall:")
        print("   python3 manage.py uninstall")
        print()
        print("For more information, see README.md")
        print()
        
    def run(self, source_path: str = None):
        """Run the setup process"""
        print("BC Coast Map Mod - Setup")
        print("========================")
        print()
        
        # Create directory structure
        self.create_directory_structure()
        
        # Copy map files if source provided
        if source_path:
            source = Path(source_path)
            if not self.copy_map_files(source):
                return False
        else:
            self.print_warning("No source path provided. You'll need to manually copy your map files to:")
            print(f"  {self.bc_coast_dir}")
            print()
            print("Required files:")
            print("  - info.json")
            print("  - mainLevel.lua")
            print("  - (and all other map files)")
            print()
            
        # Validate setup
        if self.validate_setup():
            self.show_instructions()
            return True
        else:
            self.print_error("Setup validation failed. Please check the missing files.")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Set up BC Coast map mod installation system")
    parser.add_argument("--source", "-s", 
                       help="Path to source map files (directory or zip file)")
    
    args = parser.parse_args()
    
    setup = SetupManager()
    success = setup.run(args.source)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 