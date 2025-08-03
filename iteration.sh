./quick_install.sh
# blender --background --python-console ""

blender

# manual steps
# import beamng level from 

cp ./terrain_analysis/beamng_export/custom_level/custom_level.ter ./beamng_map_mod/levels/bc_coast/
cd beamng_map_mod
python manage.py package && python manage.py install

"/Volumes/Goodboy/apps/CrossOver.app/Contents/SharedSupport/CrossOver/CrossOver-Hosted Application/wine" "C:\Program Files (x86)\Steam\steamapps\common\BeamNG.drive\Bin64\BeamNG.drive.x64.exe"

# manual steps