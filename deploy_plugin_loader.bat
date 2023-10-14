@echo off
mkdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon

xcopy pyvoxelhorizon %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\pyvoxelhorizon\ /Y
xcopy plugin_loader\plugin_loader.py %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\entrypoint.py /Y