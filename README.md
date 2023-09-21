# PyVoxelHorizon
## What is PyVoxelHorizon?
A framework that injects Python code into the Voxel Horizon process and provides the Python Wrapper API for CALL, READ, WRITE using native pointers.

## How to development Plugin/MOD?
1. Download or Build `PyVoxelHorizonBridge.dll` and copy dll to `pyvoxelhorizon/` directory
2. Write plugin code
    - [Template Plugin](samples/template_plugin/template_plugin.py)
    - [Example Plugin](samples/example_plugin/example_plugin.py)
    - [Doom Plugin](samples/doom_plugin/doom_plugin.py)
    - [NES Plugin](samples/nes_plugin/nes_plugin.py)
3. Put plugin code in `plugins/` directory
4. Run `attach_to_vh.bat` after run Voxel Horizon

## How to build `PyVoxelHorizonBridge.dll`?
1. Install `python==3.11.X` with enabled `development/embedded` options
2. Open `pyvoxelhorizonbridge/windows/PyVoxelHorizonBridge.sln` using Visual Studio
3. Build

## How to development `PyVoxelHorizon`?
Sorry, Not ready yet..

## Demo Video
### NES Plugin Demo (Mario)
https://github.com/devjeonghwan/PyVoxelHorizon/assets/13144936/1086ecdf-439c-4afc-bf60-8ac00af043b5

### Doom Plugin
https://github.com/devjeonghwan/PyVoxelHorizon/assets/13144936/8e03dd6f-0eb6-47f0-8dcd-06b965163fa3
