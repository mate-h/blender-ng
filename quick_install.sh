#!/bin/bash
# Quick installation script for BeamNG Blender Addon development

echo "🚀 BeamNG Blender Addon - Quick Install"
echo "======================================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9 or higher."
    exit 1
fi

# Install for development (symlink)
echo "📦 Installing addon for development..."
python install_addon.py --dev

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Open Blender"
echo "2. Go to Edit > Preferences > Add-ons"  
echo "3. Search for 'BeamNG' and enable the addon"
echo "4. Look for the 'BeamNG' tab in the 3D Viewport sidebar (N key)"
echo ""
echo "🔧 Development tip: Changes to the code will be reflected immediately!"
echo "   Just disable/enable the addon in Blender preferences to reload." 