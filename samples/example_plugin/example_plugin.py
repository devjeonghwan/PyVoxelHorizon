from voxel_horizon_plugin import VoxelHorizonPlugin
from pyvoxelhorizon.game.object import *
from pyvoxelhorizon.game.helper import VoxelEditor

PLUGIN_NAME = "ExamplePlugin"

class ExamplePlugin(VoxelHorizonPlugin):
    def on_update(self, game_context: GameContext):
        ############################
        #  Get Window/Device Size  #
        ############################
        window_width = game_context.get_window_width()
        window_height = game_context.get_window_height()
        device_width = game_context.get_device_width()
        device_height = game_context.get_device_height()

        game_context.write_text_line(0xFFFFFFFF, "Window Width: " + str(window_width))
        game_context.write_text_line(0xFFFFFFFF, "Window Height: " + str(window_height))
        game_context.write_text_line(0xFFFFFFFF, "Device Width: " + str(device_width))
        game_context.write_text_line(0xFFFFFFFF, "Device Height: " + str(device_height))
        ############################
        

        ######################
        #  Get Map Contains  #
        ######################
        is_in_private_map = game_context.is_in_private_map()
        is_in_pvp_mode = game_context.is_in_pvp_mode()

        game_context.write_text_line(0xFFFFFFFF, "Is In Private Map: " + str(is_in_private_map))
        game_context.write_text_line(0xFFFFFFFF, "Is In PVP Map: " + str(is_in_pvp_mode))
        #####################


        #####################
        #  Key Press Check  #
        #####################
        if game_context.is_key_press(KEY_UP):
            game_context.write_text_line(0xFFFFFFFF, "Press Key `UP`.")

        if game_context.is_key_press(KEY_DOWN):
            game_context.write_text_line(0xFFFFFFFF, "Press Key `DOWN`.")

    def on_mouse_left_click(self, game_context: GameContext):
        battle_scene = game_context.get_battle_scene()

        if not battle_scene:
            game_context.write_text_line(0xFFFFFFFF, "Failed to access battle scene.")
            return
        
        #####################
        #  Load Voxel File  #
        #####################
        # .../plugins/{plugin_file_name|example_plugin}/file.vxl
        battle_scene.load_voxels(self.get_path("file.vxl"))
        # or
        battle_scene.load_voxels("C:/file.vxl")
        ####################
        

        voxel_object_manager = battle_scene.get_voxel_object_manager()

        if not voxel_object_manager:
            game_context.write_text_line(0xFFFFFFFF, "Failed to access voxel object manager.")
            return
        

        #########################
        #  Create Voxel Object  #
        #########################
        vector3 = Vector3()
        vector3.x = 100
        vector3.y = 200
        vector3.z = 400

        result = voxel_object_manager.create_voxel_object_with_float_coord(vector3, 8, 0xFFFFFFFF)
        # or
        result = voxel_object_manager.create_voxel_object(100, 200, 400, 8, 0xFFFFFFFF)
        
        if not result.is_success():
            game_context.write_text_line(0xFFFFFFFF, "Failed to create voxel object. " + result.get_meesage())
            return
        
        voxel_object = result.voxel_object
        #########################
        

        ######################
        #  Get Voxel Object  #
        ######################
        vector3 = Vector3()
        vector3.x = 100
        vector3.y = 200
        vector3.z = 400

        voxel_object = voxel_object_manager.get_voxel_object_with_float_coord(vector3, 8, 0xFFFFFFFF)
        # or
        voxel_object = voxel_object_manager.get_voxel_object(100, 200, 400, 8, 0xFFFFFFFF)
        
        if not voxel_object:
            game_context.write_text_line(0xFFFFFFFF, "Not exists voxel object in " + str(vector3) + ".")
            return
        
        voxel_object = result.voxel_object
        ######################
        
        
        ###############################
        #  Get Voxel Object Property  #
        ###############################
        voxel_object_property = voxel_object.get_voxel_object_property()

        game_context.write_text_line(0xFFFFFFFF, "Width Depth Height: " + str(voxel_object_property.width_depth_height))
        game_context.write_text_line(0xFFFFFFFF, "Voxel Size: " + str(voxel_object_property.voxel_size))
        ###############################
        
        
        #########################
        #  Voxel Object Access  #
        #########################
        # Get Voxels
        for z in range(voxel_object_property.width_depth_height):
            for y in range(voxel_object_property.width_depth_height):
                for x in range(voxel_object_property.width_depth_height):
                    exists = voxel_object.get_voxel(x, y, z)

                    if exists:
                        print("Voxel Exists")
                    else:
                        print("Voxel Not Exists")

        # Get voxel color by index
        voxel_color = get_voxel_color(0)
        # Find similar voxel color with red(255, 0, 0)
        voxel_color = find_similar_voxel_color(255, 0, 0)

        # Voxel positioning between 0 ~ 7 assuming voxel `width_height_depth` is 8
        voxel_x = 3
        voxel_y = 2
        voxel_z = 1

        # Clear all voxels and Add voxel
        if voxel_object.clear_and_add_voxel(voxel_x, voxel_y, voxel_z, True):
            game_context.write_text_line(0xFFFFFFFF, "Failed to clear and add voxel.")
        
        # Add voxel with given position and `width_height_depth|8` and color
        if voxel_object.add_voxel_with_auto_resize(8, voxel_x, voxel_y, voxel_z, voxel_color):
            game_context.write_text_line(0xFFFFFFFF, "Failed to add voxel.")
        
        # Set voxel color with given position and `width_height_depth|8`
        if voxel_object.set_voxel_color_with_auto_resize(8, voxel_x, voxel_y, voxel_z, voxel_color):
            game_context.write_text_line(0xFFFFFFFF, "Failed to remove voxel.")
        
        # Set all voxels color of voxel object
        if voxel_object.set_palette_with_indexed_color(voxel_color):
            game_context.write_text_line(0xFFFFFFFF, "Failed to remove voxel.")
        
        # Remove voxel with given position and `width_height_depth|8`
        if voxel_object.remove_voxel_with_auto_resize(8, voxel_x, voxel_y, voxel_z):
            game_context.write_text_line(0xFFFFFFFF, "Failed to remove voxel.")
        
        # Get voxel object is destroyable or not
        if voxel_object.is_destroyable():
            game_context.write_text_line(0xFFFFFFFF, "Is Destroyable")
        else:
            game_context.write_text_line(0xFFFFFFFF, "Is Not Destroyable")

        # Set voxel object destroyable
        voxel_object.set_destroyable(True)
        
        # Update voxel object's geometry(immediately|True)
        voxel_object.update_geometry(True)
        
        # Update voxel object's light
        voxel_object.update_lighting()
        #########################

        # ...

        # or If you want easy way (little bit slow..)

        # ...
        
        #########################
        #  Voxel Editor Helper  #
        #########################
        # Open editor
        voxel_editor = VoxelEditor()

        if voxel_editor.get_voxel(100, 200, 300):
            print("Voxel Exists")
        else:
            print("Voxel Not Exists")
        
        # Add voxel without voxel object and any local position
        # You can use global position coordinate system
        if not voxel_editor.add_voxel(100, 200, 300, voxel_color):
            game_context.write_text_line(0xFFFFFFFF, "Failed to add voxel.")

        # Set voxel color without voxel object and any local position
        # You can use global position coordinate system
        if not voxel_editor.set_voxel_color(100, 200, 300, voxel_color):
            game_context.write_text_line(0xFFFFFFFF, "Failed to set voxel color.")

        # Remove voxel without voxel object and any local position
        # You can use global position coordinate system
        if not voxel_editor.remove_voxel(100, 200, 300):
            game_context.write_text_line(0xFFFFFFFF, "Failed to remove voxel.")

        # Commit editor
        voxel_editor.finish()
        #########################
                

    def on_mouse_right_click(self, game_context: GameContext):
        #####################
        #  Game Write Text  #
        #####################
        game_context.write_text_line(0xFF0000FF, "Blue Text Message!")
        game_context.write_text(0xFFFF0000, "Red Text Message!\n")
        #####################


    def on_stop(self):
        # Do Somthing or You can remove this function
        return None
