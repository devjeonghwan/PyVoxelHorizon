@echo off

rmdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\pyvoxelhorizon\ /s /q
mkdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon
mkdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\pyvoxelhorizon\

xcopy pyvoxelhorizon %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\pyvoxelhorizon\ /E /H /Y

SET ENTRYPOINT_FILE_PATH="%VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\entrypoint.py"

del %ENTRYPOINT_FILE_PATH%
echo from pyvoxelhorizon.plugin.plugin_loader import PluginLoader>%ENTRYPOINT_FILE_PATH%
echo.>>%ENTRYPOINT_FILE_PATH%
echo.>>%ENTRYPOINT_FILE_PATH%
echo def create_game_hook(address):>>%ENTRYPOINT_FILE_PATH%
echo     return PluginLoader(address)>>%ENTRYPOINT_FILE_PATH%