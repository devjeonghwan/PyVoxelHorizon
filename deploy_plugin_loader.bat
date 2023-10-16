@echo off

rmdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\ /s /q
mkdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon

xcopy pyvoxelhorizon %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\pyvoxelhorizon\ /E /H /Y

(
echo from pyvoxelhorizon.plugin.plugin_loader import PluginLoader
echo ""
echo ""
echo def create_game_hook(address):
echo     return PluginLoader(address)
)>"%VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\entrypoint.py"