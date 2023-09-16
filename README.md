# PyVoxelHorizon
## What is PyVoxelHorizon?
A framework that injects Python code into the Voxel Horizon process and provides the Python Wrapper API for CALL, READ, WRITE using native pointers.

## How to development Plugin/MOD?
First, You have to write own plugin code. Please see below codes.
1. [Template Plugin](samples/template_plugin/template_plugin.py)
2. [Example Plugin](samples/example_plugin/example_plugin.py)
3. [Doom Plugin](samples/doom_plugin/doom_plugin.py)
4. [NES Plugin](samples/nes_plugin/nes_plugin.py)

And put your plugin code in `plugins/` directory and Download or Build `PyVoxelHorizonBridge.dll` and copy dll to `pyvoxelhorizon/` directory.  

Then run `AA.attach_to_vh`. Done!

## How to build `PyVoxelHorizonBridge.dll`?
1. Install `python==3.11.X` with enabled `development/embedded` options
2. Open `pyvoxelhorizonbridge/windows/PyVoxelHorizonBridge.sln` using Visual Studio
3. Build

## How to development `PyVoxelHorizon`?
Sorry, Not ready yet..
