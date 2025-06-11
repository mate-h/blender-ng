#!/bin/bash
# Quick install script for BeamNG Blender Addon (Updated for EXR Terrain)
# This script installs the addon to Blender and provides testing instructions

echo "🔧 BeamNG Blender Addon - Quick Install (EXR Terrain Version)"
echo "============================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Blender is installed
if ! command -v blender &> /dev/null; then
    print_error "Blender not found in PATH"
    print_warning "Please install Blender 4.0+ or add it to your PATH"
    echo "Download from: https://www.blender.org/download/"
    exit 1
fi

# Get Blender version
BLENDER_VERSION=$(blender --version | head -n1 | grep -o '[0-9]\+\.[0-9]\+')
print_status "Found Blender version: $BLENDER_VERSION"

# Check if Blender 4.0+
if [[ $(echo "$BLENDER_VERSION < 4.0" | bc -l) -eq 1 ]]; then
    print_warning "Blender 4.0+ recommended for best compatibility"
fi

# Determine Blender addons directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    ADDON_DIR="$HOME/Library/Application Support/Blender/$BLENDER_VERSION/scripts/addons"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    ADDON_DIR="$HOME/.config/blender/$BLENDER_VERSION/scripts/addons"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    ADDON_DIR="$APPDATA/Blender Foundation/Blender/$BLENDER_VERSION/scripts/addons"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Addon directory: $ADDON_DIR"

# Create addon directory if it doesn't exist
if [ ! -d "$ADDON_DIR" ]; then
    print_status "Creating addon directory..."
    mkdir -p "$ADDON_DIR"
fi

# Copy addon to Blender addons directory
ADDON_NAME="beamng_blender_addon"
TARGET_DIR="$ADDON_DIR/$ADDON_NAME"

print_status "Installing addon to: $TARGET_DIR"

# Remove existing installation
if [ -d "$TARGET_DIR" ]; then
    print_warning "Removing existing installation..."
    rm -rf "$TARGET_DIR"
fi

# Copy addon files
cp -r "$ADDON_NAME" "$TARGET_DIR"

print_status "Addon files copied successfully!"

# Create test data symlink (if test data exists)
TEST_DATA_PATH="/Volumes/Goodboy/crossover/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/levels/small_island"

if [ -d "$TEST_DATA_PATH" ]; then
    print_status "Test data found - you can test with small_island level"
else
    print_warning "Test data not found at: $TEST_DATA_PATH"
    print_warning "You'll need BeamNG.drive installed to test terrain import"
fi

echo ""
echo "🎉 Installation Complete!"
echo "========================"

echo ""
echo "📋 Next Steps:"
echo "1. Start Blender"
echo "2. Go to Edit > Preferences > Add-ons"
echo "3. Search for 'BeamNG'"
echo "4. Enable the 'BeamNG Level Importer/Exporter' addon"
echo "5. Check the 3D Viewport sidebar (N key) for 'BeamNG' tab"

echo ""
echo "🧪 Testing EXR Terrain Import:"
echo "1. Go to File > Import > BeamNG Level"
echo "2. Navigate to a BeamNG level directory (with .ter and .terrain.json files)"
echo "3. Adjust terrain settings in the BeamNG panel:"
echo "   • Terrain Scale: Controls overall terrain size"
echo "   • Displacement Strength: Controls height variation (try 50-500)"
echo "   • Subdivision Levels: Controls terrain detail (6+ recommended)"
echo "4. Enable 'Import Terrain' and click 'Import BeamNG Level'"

echo ""
echo "🎯 Expected Results:"
echo "• Creates 'BeamNG_Terrain' object with subdivision surface"
echo "• Generates 16-bit EXR displacement texture"
echo "• Real-time viewport displacement preview"
echo "• Green terrain material with proper shading"

echo ""
echo "⚡ Performance Notes:"
echo "• High subdivision levels (8+) may be slow in viewport"
echo "• Switch to 'Material Preview' or 'Rendered' viewport shading"
echo "• Consider lower subdivision for initial testing"

echo ""
print_status "Happy terrain importing! 🏞️" 