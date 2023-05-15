import os
from .native import dll_injector

def patch_with_python_script(script_file):
    bridge_file = os.path.dirname(os.path.realpath(__file__)) + "/PyVoxelHorizonBridge.dll"
    
    # print("Patching 'PyVoxelHorizon' bridge into 'VoxelHorizon'..")
    
    injector = dll_injector.DLLInjector()

    # print("Try attach to 'Client_x64_release.exe'..")
    injector.bind_by_name("Client_x64_release.exe")
    # print("Attached!")

    # print("Try inject bridge dll..")
    module_address = injector.load_module(bridge_file)
    # print("Injected!")

    # print("Try initialize bridge..")
    function_address = dll_injector.get_function_address_with_module_path(bridge_file, "InitializeBridge")

    script_file = os.path.abspath(script_file)
    script_file_address = injector.allocate((len(script_file) + 1) * 2)

    try:
        injector.write_wide_characters(script_file_address, script_file)
    
        injector.call(module_address, function_address, script_file_address)

        # print("Initialized!")
    finally:
        injector.deallocate(script_file_address)