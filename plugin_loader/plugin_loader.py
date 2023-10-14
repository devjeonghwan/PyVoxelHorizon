from pyvoxelhorizon import GameHook

def create_game_hook(address):
    return PyVoxelHorizonPluginLoader(address)

class PyVoxelHorizonPluginLoader(GameHook):
    def __init__(self, address):
        return