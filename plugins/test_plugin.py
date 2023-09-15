from pyvoxelhorizon.game.object import GameContext
from voxel_horizon_plugin import VoxelHorizonPlugin
from pyvoxelhorizon.game.object import *

PLUGIN_NAME     = "TestPlugin"

class TestPlugin(VoxelHorizonPlugin):
    def on_initialize(self, game_context: GameContext):
        print("Load!")

    def on_update(self, game_context: GameContext):
        print("Update!")

    def on_mouse_right_click(self, game_context: GameContext):
        game_context.write_text(0xff0000ff, "Blue Console Message!\n")

        battle_scene = game_context.get_battle_scene()

        if not battle_scene:
            return
        
        voxel_object_manager = battle_scene.get_voxel_object_manager()

        if not voxel_object_manager:
            return

        VOXEL_OBJECT_SIZE = 400
        
        
        v3Pos = Vector3()
        v3Pos.x = 200
        v3Pos.y = -2200
        v3Pos.z = 200


        result = voxel_object_manager.create_voxel_object(v3Pos, 8, 0xffffffff)
        voxel_object = result.voxel_object

        if not voxel_object:
            game_context.write_text(0xffffffff, "Failed to create object. " + str(result.get_meesage()) + "\n")
            return
        
        voxel_object.set_palette_with_indexed_color(15)
        voxel_object.update_geometry(False)
        voxel_object.update_lighting()
        voxel_object.set_destroyable(True)
        v3Pos.x += VOXEL_OBJECT_SIZE


        result = voxel_object_manager.create_voxel_object(v3Pos, 8, 0xffffffff)
        voxel_object = result.voxel_object

        if not voxel_object:
            game_context.write_text(0xffffffff, "Failed to create object. " + str(result.get_meesage()) + "\n")
            return
        
        voxel_object.set_palette_with_indexed_color(3)
        voxel_object.update_geometry(False)
        voxel_object.update_lighting()
        voxel_object.set_destroyable(True)
        v3Pos.x += VOXEL_OBJECT_SIZE


        result = voxel_object_manager.create_voxel_object(v3Pos, 4, 0xffffffff)
        voxel_object = result.voxel_object

        if not voxel_object:
            game_context.write_text(0xffffffff, "Failed to create object. " + str(result.get_meesage()) + "\n")
            return
        
        voxel_object.set_palette_with_indexed_color(5)
        voxel_object.update_geometry(False)
        voxel_object.update_lighting()
        voxel_object.set_destroyable(True)
        v3Pos.x += VOXEL_OBJECT_SIZE


        result = voxel_object_manager.create_voxel_object(v3Pos, 2, 0xffffffff)
        voxel_object = result.voxel_object

        if not voxel_object:
            game_context.write_text(0xffffffff, "Failed to create object. " + str(result.get_meesage()) + "\n")
            return
        
        voxel_object.set_palette_with_indexed_color(7)
        voxel_object.update_geometry(False)
        voxel_object.update_lighting()
        voxel_object.set_destroyable(True)
        v3Pos.x += VOXEL_OBJECT_SIZE


        result = voxel_object_manager.create_voxel_object(v3Pos, 1, 0xffffffff)
        voxel_object = result.voxel_object

        if not voxel_object:
            game_context.write_text(0xffffffff, "Failed to create object. " + str(result.get_meesage()) + "\n")
            return
        
        voxel_object.set_palette_with_indexed_color(9)
        voxel_object.update_geometry(False)
        voxel_object.update_lighting()
        voxel_object.set_destroyable(True)
        v3Pos.x += VOXEL_OBJECT_SIZE


        result = voxel_object_manager.create_voxel_object(v3Pos, 8, 0xffffffff)
        voxel_object = result.voxel_object

        if not voxel_object:
            game_context.write_text(0xffffffff, "Failed to create object. " + str(result.get_meesage()) + "\n")
            return
        
        voxel_object.set_palette_with_indexed_color(11)
        voxel_object.update_geometry(False)
        voxel_object.update_lighting()
        voxel_object.set_destroyable(True)
        v3Pos.x += VOXEL_OBJECT_SIZE

        voxel_object_manager.update_visibility()
        
        game_context.write_text(0xffffffff, "Is Destoryable " + str(voxel_object.is_destroyable()) + "\n")



        # VECTOR3
        # vector_test = Vector3()
        # vector_test.x = 1000
        # vector_test.y = -2200
        # vector_test.z = 600

        # # voxel_object = voxel_object_manager.ge_voxel_object(vector_test)
        # # game_context.write_text(0xffffffff, ">>> " + str(voxel_object) + "\n")
        # # result = voxel_object_manager.create_voxel_object(vector_test, width_height_depth, 0xffffffff)
        # # game_context.write_text(0xffffffff, "RET: " + result.get_meesage() + "\n")
        # # voxel_object = voxel_object_manager.get_voxel_object(vector_test)
        
        # result = voxel_object_manager.create_voxel_object(vector_test, 8, 0xffffffff)
        # voxel_object = result.voxel_object

        # # Voxel 생성 실패 검사
        # if not voxel_object:
        #     game_context.write_text(0xffffffff, "Failed to create object. " + str(result.get_meesage()) + "\n")
        #     return
        
        # voxel_object.set_palette_with_indexed_color(4)
        # voxel_object.set_destroyable(True)

        # game_context.write_text(0xffffffff, "is_destroyable: " + str(voxel_object.is_destroyable()) + "\n")
        
        # # 업데이트 해주고
        # voxel_object.update_geometry(False)
        # voxel_object.update_lighting()
        
        # voxel_object.add_voxel_with_auto_resize(8, 1, 1, 1, 32)

        # voxel_object_property = voxel_object.get_voxel_object_property()
        # game_context.write_text(0xffffffff, "<<< " + str(voxel_object_property) + "\n")

        # voxel_object_property = voxel_object.get_voxel_object_property()
        # game_context.write_text(0xffffffff, "<<< " + str(voxel_object_property) + "\n")

        # str_buffer = ""

        # for z in range(voxel_object_property.width_depth_height):
        #     for y in range(voxel_object_property.width_depth_height):
        #         for x in range(voxel_object_property.width_depth_height):
        #             if voxel_object.get_voxel(x, y, z):
        #                 str_buffer += "■"
        #             else:
        #                 str_buffer += "□"
                
        #         str_buffer += "\n"
            
        #     str_buffer += "\n"
        
        # self.show_message(str_buffer)
        # 0 = OK
        # 2 = POSITION ERROR
        # 3 = ALLOC ERROR
        # 1 = EXISTS ERROR


    def on_stop(self):
        return None
