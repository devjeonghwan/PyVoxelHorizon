# PyVoxelHorizon
Are you looking for PyVoxelHorizon DLL injection version? See this [branch](https://github.com/devjeonghwan/PyVoxelHorizon/tree/injection_version) 

## What is PyVoxelHorizon?
A framework that attaches CPython using the Voxel Horizon official SDK and provides Python Wrapper API.

# Structure
```mermaid
flowchart TD
    USER_PLUGIN["User Python Plugins"]
    PY_VOXEL_HORIZON_PLUGIN_LOADER["PyVoxelHorizon Plugin Loader\n(pyvoxelhorizon/plugin/plugin_loader.py)"]
    PY_VOXEL_HORIZON_PLUGIN["PyVoxelHorizon Plugin Interface\n(pyvoxelhorizon/plugin/)"]
    PY_VOXEL_HORIZON["PyVoxelHorizon Interface\n(pyvoxelhorizon/enum|interface|struct/)"]
    PY_VOXEL_HORIZON_WRAPPER["PyVoxelHorizon Wrapper Plugin\n(wrapper_plugin/)"]
    PY_VOXEL_HORIZON_WRAPPER_GENERATOR["PyVoxelHorizon Wrapper Generator\n(pyvoxelhorizon/generator/)"]
    VOXEL_HORIZON{{"VOXEL HORIZON Process"}}
    VOXEL_HORIZON_HEADER_FILE{{"Offical SDK Header Files"}}
    
    VOXEL_HORIZON -->|"Load\n(Official Function)"| PY_VOXEL_HORIZON_WRAPPER
    PY_VOXEL_HORIZON_WRAPPER_GENERATOR -->|"Parse"| VOXEL_HORIZON_HEADER_FILE

    subgraph C++ Side
    PY_VOXEL_HORIZON_WRAPPER -->|"DLL Load"| PYTHON["CPython"]
    end
    
    subgraph Python Side
    PY_VOXEL_HORIZON_WRAPPER_GENERATOR -->|"Generate"| PY_VOXEL_HORIZON

    PY_VOXEL_HORIZON_WRAPPER <==>|"C++/Python\nInteroperation"| PY_VOXEL_HORIZON
    PY_VOXEL_HORIZON -->|"Implementation"| PY_VOXEL_HORIZON_PLUGIN_LOADER
    PY_VOXEL_HORIZON -..->|"Implementation"| IMPL1("Another Python Apps?")
    end

    subgraph Plugin Side
    PY_VOXEL_HORIZON_PLUGIN -->|"Implementation"| USER_PLUGIN
    PY_VOXEL_HORIZON_PLUGIN_LOADER -->|"Loads\n(Hot Reloads, Plugin Load, Helpers, ...)"| USER_PLUGIN
    end
```

## How to development Plugin without C++ Build?
1. Install [Python 3.11](https://www.python.org/downloads/release/python-3110/) for all users
2. Download `PyVoxelHorizon_{Build Number}.zip` from [releases](https://github.com/devjeonghwan/PyVoxelHorizon/releases) and extract all files to `{VOXEL HORIZON Path}/Plugin/bin/`
3. Write plugin code and Save into `{VOXEL HORIZON Path}/Plugin/bin/PyVoxelHorizon/plugins`
    - [Basic Plugin](sample/basic_plugin.py)
    - [MIDI Player Plugin](sample/midi_example_plugin.py)
4. Run VOXEL HORIZON
5. Press the '`' key to open the console
6. Enter the `load_plugin PyVoxelHorizon_x64_Release.dll`
7. Or, You can also uses command arguments. See [official document](https://github.com/megayuchi/VH_SDK)

## How to development `PyVoxelHorizon Wrapper Plugin`?
1. Install [Python 3.11](https://www.python.org/downloads/release/python-3110/) with enabled `development/embedded` options for all users
2. Set environment variable `PYTHON_PATH` to the path where Python is installed.
3. Set environment variable `VOXEL_HORIZON_PATH` to the path where VOXEL HORIZON is installed.
4. Open `wrapper_plugin/PyVoxelHorizon.sln` using Visual Studio 2022
5. Build or Debug

## How to development `PyVoxelHorizon Interfaces`?
Sorry, Not ready yet.

## How to development `PyVoxelHorizon Wrapper Generator`?
Sorry, Not ready yet.

## Troubleshoot
### `ModuleNotFoundError` occurred when running the plugin.
![image](https://github.com/devjeonghwan/PyVoxelHorizon/assets/13144936/22c625b8-d322-4723-815c-ced231e2efab)

The Python moule that the plugin uses is not installed.

It can be resolved through `pip install {Module Name}`. (For photo examples, `pip install umidiparser`)
