# PyVoxelHorizon

# Structure
```mermaid
flowchart TB
    USER_PLUGIN["User Python Plugins"]
    PY_VOXEL_HORIZON_PLUGIN_LOADER["PyVoxelHorizon Plugin Loader\n(plugin_loader/)"]
    PY_VOXEL_HORIZON["PyVoxelHorizon Interface\n(pyvoxelhorizon/)"]
    PY_VOXEL_HORIZON_WRAPPER["PyVoxelHorizon Wrapper Plugin\n(wrapper_plugin/)"]
    PY_VOXEL_HORIZON_WRAPPER_GENERATOR["PyVoxelHorizon Wrapper Generator\n(pyvoxelhorizon/generator/)"]
    VOXEL_HORIZON{{"VOXEL HORIZON Process"}}
    VOXEL_HORIZON_HEADER_FILE{{"VOXEL HORIZON Offical SDK\nHeader Files"}}
    
    VOXEL_HORIZON -->|"Load\n(Official Function)"| PY_VOXEL_HORIZON_WRAPPER
    VOXEL_HORIZON_HEADER_FILE -->|"Parse"| PY_VOXEL_HORIZON_WRAPPER_GENERATOR
    PY_VOXEL_HORIZON_WRAPPER_GENERATOR -->|"Generate"| PY_VOXEL_HORIZON

    subgraph C++ Side
    PY_VOXEL_HORIZON_WRAPPER -->|"DLL Load"| PYTHON["CPython"]
    end
    
    subgraph Python Side
    PY_VOXEL_HORIZON_WRAPPER <==>|"C++/Python\nInteroperation"| PY_VOXEL_HORIZON
    PY_VOXEL_HORIZON -->|"Implementation"| PY_VOXEL_HORIZON_PLUGIN_LOADER
    PY_VOXEL_HORIZON -..->|"Implementation"| IMPL1("Another Python Apps?")
    end
    
    subgraph Plugin Side
    PY_VOXEL_HORIZON_PLUGIN_LOADER -->|"Loads\n(Hot Reloads, Multiple Plugins, Helpers, ...)"| USER_PLUGIN
    end
```
