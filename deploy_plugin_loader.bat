@echo off

rmdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\ /s /q
mkdir %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon

xcopy pyvoxelhorizon %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\pyvoxelhorizon\ /E /H /Y
xcopy plugin_loader\plugin_loader.py %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\* /E /H /Y /F
ren %VOXEL_HORIZON_PATH%\Plugin\bin\PyVoxelHorizon\plugin_loader.py entrypoint.py