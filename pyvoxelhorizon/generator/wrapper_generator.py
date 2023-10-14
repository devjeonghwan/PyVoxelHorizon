import os
from sctokenizer import Source, TokenType

HEADER_FILE_NAMES = ["header/IGameHookController.h", "header/typedef.h", "header/math.inl"]
GENERATE_TARGETS = [
    # Enum
    "VH_EDIT_MODE", 
    "SCENE_WORLD_SIZE",
    "AXIS_TYPE",
    "PLANE_AXIS_TYPE",
    "CHAR_CODE_TYPE",
    "RENDER_MODE",
    "DEBUG_DRAW_FLAG",
    "GET_COLLISION_TRI_TYPE",

    # Interface
    "IVHController", 
    "IVHNetworkLayer", 

    "IVoxelObjectLite",

    # Struct
    "VOXEL_OBJ_PROPERTY",

    "INDEX_POS",
    "WORD_POS",
    "BYTE_POS",

    "AABB",
    "INT_AABB",
    "PLANE",

    "CAMERA_DESC_COMMON",
    # "CAMERA_DESC",

    "BYTE2",

    "IVERTEX",

    "INT_VECTOR2",
    "VECTOR2",

    "INT_VECTOR3",
    "VECTOR3",

    "INT_VECTOR4",
    "VECTOR4",

    "TRIANGLE",

    "DWORD_RECT",
    "FLOAT_RECT",

    "MIDI_NOTE"
]

IGNORES = ["SetOnDeleteVoxelObjectFunc"]
HINTS = {
    "IVHController": {
        "name": "GameController"
    },
    "IVHNetworkLayer": {
        "name": "NetworkLayer"
    },
    "IVoxelObjectLite": {
        "name": "VoxelObjectLite"
    },
    

    "VOXEL_OBJ_PROPERTY": {
        "name": "VoxelObjectProperty"
    },

    "INDEX_POS": {
        "name": "IndexPosition"
    },
    "WORD_POS": {
        "name": "WordPosition"
    },
    "BYTE_POS": {
        "name": "BytePosition"
    },
    
    "AABB": {
        "name": "AABB"
    },
    "INT_AABB": {
        "name": "IntAABB"
    },
    "PLANE": {
        "name": "Plane"
    },
    
    "CAMERA_DESC_COMMON": {
        "name": "CameraDescriptionCommon"
    },
    
    "BYTE2": {
        "name": "Byte2"
    },
    
    "IVERTEX": {
        "name": "Vertex"
    },
    
    "INT_VECTOR2": {
        "name": "IntVector2"
    },
    "VECTOR2": {
        "name": "Vector2"
    },
    
    "INT_VECTOR3": {
        "name": "IntVector3"
    },
    "VECTOR3": {
        "name": "Vector3"
    },
    
    "INT_VECTOR4": {
        "name": "IntVector4"
    },
    "VECTOR4": {
        "name": "Vector4"
    },
    
    "TRIANGLE": {
        "name": "Triangle"
    },
    
    "DWORD_RECT": {
        "name": "DwordRectangle"
    },
    "FLOAT_RECT": {
        "name": "FloatRectangle"
    },
    
    "MIDI_NOTE": {
        "name": "MidiNote"
    },
}

OUTPUT_DIRECTORY = "generated/"

parsed_enums = []
parsed_interfaces = []
parsed_structs = []

def add_type_with_tokens(output_types, argument_tokens):
    argument_type_tokens = argument_tokens[:]
    argument_name = None
    
    argument_tokens.reverse()
    
    for argument_token in argument_tokens:
        if argument_token.token_type == TokenType.IDENTIFIER:
            argument_type_tokens.remove(argument_token)
            argument_name = argument_token.token_value
            break

    argument_type = ""

    for argument_type_token in argument_type_tokens:
        if argument_type_token.token_value == '//':
            continue

        argument_type += argument_type_token.token_value

    output_types.append({
        'type': argument_type,
        'name': argument_name
    })

# Parse Header Files
for header_file_name in HEADER_FILE_NAMES:
    source = Source.from_file(header_file_name, lang='cpp')
    tokens = source.tokenize()

    cursor = 0

    while True:
        if cursor >= len(tokens):
            break

        token = tokens[cursor]
        token_type = token.token_type
        token_value = token.token_value

        # Enum Parse
        if token_value == 'enum':
            cursor += 1
            name = tokens[cursor].token_value

            parsed_enum = {
                'name': name,
                'types': []
            }

            brace_count = 0
            enum_count = 0
            last_enum_name = None
            last_enum_value = enum_count

            while True:
                if cursor >= len(tokens):
                    break

                token = tokens[cursor]
                token_type = token.token_type
                token_value = token.token_value

                if brace_count == 1:
                    if token_type == TokenType.IDENTIFIER:
                        last_enum_name = token_value

                    if token_type == TokenType.CONSTANT:
                        last_enum_value = token_value

                    if token_type == TokenType.OPERATOR and token_value == ',':
                        parsed_enum['types'].append({
                            'name': last_enum_name,
                            'value': last_enum_value
                        })

                        enum_count += 1
                        last_enum_name = None
                        last_enum_value = enum_count

                if token_type == TokenType.SPECIAL_SYMBOL and token_value == '{':
                    brace_count += 1
                if token_type == TokenType.SPECIAL_SYMBOL and token_value == '}':
                    brace_count -= 1

                    if brace_count == 0:
                        break

                cursor += 1
            
            if last_enum_name != None and last_enum_value != None:
                parsed_enum['types'].append({
                    'name': last_enum_name,
                    'value': last_enum_value
                })

            parsed_enums.append(parsed_enum)
            continue
        elif token_value == 'interface':
            cursor += 1
            name = tokens[cursor].token_value

            parsed_interface = {
                'name': name,
                'functions': []
            }

            brace_count = 0

            while True:
                if cursor >= len(tokens):
                    break

                token = tokens[cursor]
                token_type = token.token_type
                token_value = token.token_value

                if brace_count == 1:
                    if token_type == TokenType.KEYWORD and token_value == 'virtual':
                        output_function = {
                            'name': '',
                            'call_convention': '__cdecl',
                            'return_type': 'void',
                            'arguments': []
                        } 

                        target_token_index = 0

                        while True:
                            if cursor >= len(tokens):
                                break
                            
                            token = tokens[cursor]
                            token_type = token.token_type
                            token_value = token.token_value

                            if target_token_index == 0:
                                # Return Type Parse
                                target_value = None
                                
                                if (token_type == TokenType.KEYWORD and token_value != "virtual") or token_type == TokenType.IDENTIFIER:
                                    target_value = token_value
                                
                                if target_value:
                                    while True:
                                        cursor += 1

                                        token = tokens[cursor]
                                        token_type = token.token_type
                                        token_value = token.token_value

                                        if token_type != TokenType.OPERATOR:
                                            cursor -= 1
                                            break
                                        else:
                                            target_value += token_value

                                    output_function['return_type'] = target_value
                                    target_token_index += 1
                            elif target_token_index == 1:
                                # Call Convention or Name Parse
                                target_value = None

                                if token_type == TokenType.IDENTIFIER:
                                    conventions = {
                                        'cdecl': '__cdecl',
                                        'clrcall': '__clrcall',
                                        'stdcall': '__stdcall',
                                        'fastcall': '__fastcall',
                                        'thiscall': '__thiscall',
                                        'vectorcall': '__vectorcall',
                                    }

                                    for convention_name in conventions.keys():
                                        if convention_name in token_value:
                                            target_value = conventions[convention_name]

                                    if target_value:
                                        output_function['call_convention'] = target_value
                                        target_token_index += 1
                                    else:
                                        output_function['name'] = token_value
                                        target_token_index += 2
                            elif target_token_index == 2:
                                # Name Parse
                                if token_type == TokenType.IDENTIFIER:
                                    output_function['name'] = token_value
                                    target_token_index += 1
                            else:
                                # Arguments Parse
                                argument_brace_count = 0

                                argument_tokens = []

                                while True:
                                    if cursor >= len(tokens):
                                        break
                                    
                                    token = tokens[cursor]
                                    token_type = token.token_type
                                    token_value = token.token_value

                                    if token_type == TokenType.OPERATOR and token_value == ',':
                                        add_type_with_tokens(output_function['arguments'], argument_tokens)
                                        argument_tokens = []
                                    elif token_type == TokenType.SPECIAL_SYMBOL and token_value == '(':
                                        argument_brace_count += 1
                                    elif token_type == TokenType.SPECIAL_SYMBOL and token_value == ')':
                                        argument_brace_count -= 1

                                        if argument_brace_count == 0:
                                            break
                                    else:
                                        if token_value != 'const':
                                            argument_tokens.append(token)

                                    cursor += 1

                                if len(argument_tokens) >= 2:
                                    add_type_with_tokens(output_function['arguments'], argument_tokens)

                                break

                            cursor += 1

                        parsed_interface['functions'].append(output_function)

                if token_type == TokenType.SPECIAL_SYMBOL and token_value == '{':
                    brace_count += 1
                if token_type == TokenType.SPECIAL_SYMBOL and token_value == '}':
                    brace_count -= 1

                    if brace_count == 0:
                        break
                cursor += 1
            
            if len(parsed_interface['functions']) > 0:
                parsed_interfaces.append(parsed_interface)

            continue
        elif token_value == 'struct':
            cursor += 1

            token = tokens[cursor]
            token_type = token.token_type
            token_value = token.token_value

            if token_type == TokenType.IDENTIFIER:
                parsed_struct = {
                    'name': token_value,
                    'fields': []
                }

                brace_count = 0
                field_tokens = []

                while True:
                    if cursor >= len(tokens):
                        break

                    token = tokens[cursor]
                    token_type = token.token_type
                    token_value = token.token_value

                    if brace_count == 1:
                        if token_type == TokenType.SPECIAL_SYMBOL and token_value == ';':
                            is_accepted_field = True
    
                            for field_token in field_tokens:
                                if field_token.token_type == TokenType.KEYWORD and field_token.token_value == "static":
                                    is_accepted_field = False
                                    break
                                
                                if field_token.token_type == TokenType.KEYWORD and field_token.token_value == "const":
                                    is_accepted_field = False
                                    break
                                
                                if field_token.token_type == TokenType.KEYWORD and field_token.token_value == "inline":
                                    is_accepted_field = False
                                    break

                            if is_accepted_field:
                                add_type_with_tokens(parsed_struct['fields'], field_tokens)

                            field_tokens = []
                        else:
                            if not (token_type == TokenType.KEYWORD and token_value == 'private'):
                                field_tokens.append(token)
                    elif brace_count == 0:
                        if token_type == TokenType.SPECIAL_SYMBOL and token_value == ';':
                            break
                    
                    if token_type == TokenType.SPECIAL_SYMBOL and token_value == '{':
                        field_tokens = []
                        brace_count += 1
                    if token_type == TokenType.SPECIAL_SYMBOL and token_value == '}':
                        field_tokens = []
                        brace_count -= 1

                        if brace_count == 0:
                            break

                    cursor += 1

                parsed_structs.append(parsed_struct)
            continue
        cursor += 1


parsed_enum_names = [parsed_enum['name'] for parsed_enum in parsed_enums]
parsed_interface_names = [parsed_interface['name'] for parsed_interface in parsed_interfaces]
parsed_struct_names = [parsed_struct['name'] for parsed_struct in parsed_structs]

def convert_name_with_hint(name):
    if name in HINTS:
        if "name" in HINTS[name]:
            return HINTS[name]['name']
        
    return name

def underbarlize(name, lower=False):
    new_name = ""

    letter_cursor = 0
    while True:
        if letter_cursor >= len(name):
            break

        word = name[letter_cursor]

        if word.isupper():
            start_cursor = letter_cursor

            letter_cursor += 1
            singleUpper = True

            while True:
                if letter_cursor >= len(name):
                    break

                if name[letter_cursor].isupper():
                    singleUpper = False
                    word += name[letter_cursor]
                    letter_cursor += 1
                else:
                    if singleUpper:
                        letter_cursor -= 1
                    else:
                        letter_cursor -= 2
                        word = word[0:len(word) - 1]
                    break
                
            if start_cursor != 0:
                new_name += "_"

        new_name += word

        letter_cursor += 1
    
    if lower:
        return new_name.lower()
    
    return new_name.upper()

def ignore_multiply_one(value, multiplier):
    if multiplier == 1:
        return value
    
    return value + " * " + str(multiplier)

def convert_raw_argument_to_python_ctype(raw_type):
    multiplier = 1

    if "[" in raw_type:
        raw_split = raw_type.split("[")
        raw_type = raw_split[0]
        multiplier = int(raw_split[1].replace("]", ""))

    if raw_type == "void":
        return "None"
    
    elif raw_type == "CHAR":
        return ignore_multiply_one("wintypes.CHAR", multiplier)
    elif raw_type == "CHAR*":
        return ignore_multiply_one("ctypes.c_char_p", multiplier)
    
    elif raw_type == "WCHAR":
        return ignore_multiply_one("wintypes.WCHAR", multiplier)
    elif raw_type == "WCHAR*":
        return ignore_multiply_one("ctypes.c_wchar_p", multiplier)
    
    elif raw_type == "char":
        return ignore_multiply_one("ctypes.c_char", multiplier)
    elif raw_type == "char*":
        return ignore_multiply_one("ctypes.c_char_p", multiplier)
    
    elif raw_type == "wchar":
        return ignore_multiply_one("ctypes.c_wchar", multiplier)
    elif raw_type == "wchar*":
        return ignore_multiply_one("ctypes.c_wchar_p", multiplier)
    
    elif raw_type.endswith("*"):
        return ignore_multiply_one("wintypes.LPVOID", multiplier)
    
    elif raw_type == "WORD":
        return ignore_multiply_one("wintypes.WORD", multiplier)
    elif raw_type == "DWORD":
        return ignore_multiply_one("wintypes.DWORD", multiplier)
    elif raw_type == "BOOL":
        return ignore_multiply_one("wintypes.BOOL", multiplier)
    elif raw_type == "BYTE":
        return ignore_multiply_one("wintypes.BYTE", multiplier)
    elif raw_type == "UINT":
        return ignore_multiply_one("wintypes.UINT", multiplier)
    elif raw_type == "INT":
        return ignore_multiply_one("wintypes.INT", multiplier)
    
    elif raw_type == "int":
        return ignore_multiply_one("ctypes.c_int", multiplier)
    elif raw_type == "long":
        return ignore_multiply_one("ctypes.c_long", multiplier)
    elif raw_type == "float":
        return ignore_multiply_one("ctypes.c_float", multiplier)
    
    elif raw_type == "...":
        return "..."
    
    elif raw_type in parsed_enum_names:
        return ignore_multiply_one("ctypes.c_int", multiplier)
    
    elif raw_type in parsed_struct_names:
        return ignore_multiply_one(convert_name_with_hint(raw_type), multiplier)
    
    else:
        raise Exception("Unknown argument type `{0}`".format(raw_type))

def convert_raw_arguments_to_python_ctypes(raw_arguments):
    python_ctypes = []

    for raw_argument in raw_arguments:
        python_ctype = convert_raw_argument_to_python_ctype(raw_argument['type'])
        
        if python_ctype == "...":
            previous_ctype = python_ctypes.pop()
            
            if previous_ctype == "ctypes.c_char" or previous_ctype == "wintypes.CHAR":
                python_ctypes.append("ctypes.c_char_p")

            elif previous_ctype == "ctypes.c_wchar" or previous_ctype == "wintypes.WCHAR":
                python_ctypes.append("ctypes.c_wchar_p")

            elif previous_ctype == "ctypes.c_char_p" or previous_ctype == "ctypes.c_wchar_p":
                python_ctypes.append(previous_ctype)

            else:
                raise Exception("Unknown variable length argument type `{0}`".format(previous_ctype))
        else:
            python_ctypes.append(python_ctype)
    
    return python_ctypes

def convert_raw_argument_to_python_type(raw_type):
    if raw_type == "void":
        return "None"
    
    elif raw_type == "CHAR":
        return "int"
    elif raw_type == "CHAR*":
        return "str"
    
    elif raw_type == "WCHAR":
        return "int"
    elif raw_type == "WCHAR*":
        return "str"
    
    elif raw_type == "char":
        return "int"
    elif raw_type == "char*":
        return "str"
    
    elif raw_type == "wchar":
        return "int"
    elif raw_type == "wchar*":
        return "str"
    
    elif raw_type.endswith("*"):
        return "int"
    
    elif raw_type == "WORD":
        return "int"
    elif raw_type == "DWORD":
        return "int"
    elif raw_type == "BOOL":
        return "bool"
    elif raw_type == "BYTE":
        return "int"
    elif raw_type == "UINT":
        return "int"
    elif raw_type == "INT":
        return "int"
    
    elif raw_type == "int":
        return "int"
    elif raw_type == "long":
        return "int"
    elif raw_type == "float":
        return "float"
    
    elif raw_type == "...":
        return "..."
    
    elif raw_type in parsed_enum_names:
        return "int"
    
    elif raw_type in parsed_struct_names:
        return convert_name_with_hint(raw_type)
    
    else:
        raise Exception("Unknown argument type `{0}`".format(raw_type))

def convert_raw_arguments_to_python_types_with_name(raw_arguments):
    python_names = []
    python_types = []

    for raw_argument in raw_arguments:
        python_type = convert_raw_argument_to_python_type(raw_argument['type'])
        
        if python_type == "...":
            previous_name = python_names.pop()
            previous_type = python_types.pop()

            if previous_type == "str":
                python_names.append("*args")
                python_types.append(None)
            else:
                raise Exception("Unknown variable length argument type `{0}`".format(previous_type))
        else:
            python_names.append(underbarlize(raw_argument['name'], lower=True))
            python_types.append(python_type)
    
    return ({
        "names": python_names,
        "types" : python_types
    })

def convert_raw_arguments_to_names(raw_arguments):
    return convert_raw_arguments_to_python_types_with_name(raw_arguments)['names']

def convert_raw_arguments_to_python_types(raw_arguments):
    return convert_raw_arguments_to_python_types_with_name(raw_arguments)['types']

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

# Enum Generate
output_code = ""
for parsed_enum in parsed_enums:
    enum_name = parsed_enum['name']

    if enum_name in GENERATE_TARGETS:
        enum_types = parsed_enum['types']

        for enum_type in enum_types:
            enum_type_name = convert_name_with_hint(enum_type['name'])
            enum_type_value = enum_type['value']

            if not enum_type_name.startswith(enum_name):
                enum_type_name = enum_name + "_" + enum_type_name

            output_code += enum_type_name + " = " + str(enum_type_value) + "\n"

        output_code += "\n"
        output_code += "\n"

with open(OUTPUT_DIRECTORY + "/enums.py", 'w') as file:
    file.write(output_code)

# Interface Generate
for parsed_interface in parsed_interfaces:
    interface_name = parsed_interface['name']
    interface_functions = parsed_interface['functions']

    if interface_name in GENERATE_TARGETS:
        output_code = ""
        
        python_interface_name = convert_name_with_hint(interface_name)

        python_global_load_functions_name = "load_functions_of_" + underbarlize(python_interface_name, lower=True)
        python_interface_functions = []
        
        output_code += "import ctypes" + "\n"
        output_code += "import ctypes.wintypes as wintypes" + "\n"
        output_code += "\n"
        
        output_code += "IS_FUNCTIONS_LOADED = False" + "\n"
        output_code += "\n"
        
        function_offset = 0
        
        for function in interface_functions:
            function_name = function['name']
            function_call_convention = function['call_convention']
            function_return_type = function['return_type']
            function_arguments = function['arguments']

            if not function_name in IGNORES:
                python_function_name = underbarlize(function_name, lower=True)

                while True:
                    is_overloaded = False

                    for python_interface_function in python_interface_functions:
                        if python_interface_function['name'] == python_function_name:
                            python_function_name = python_function_name + "_overloaded"
                            is_overloaded = True

                            break
                    
                    if not is_overloaded:
                        break
                
                python_global_function_name = "FUNCTION_" + underbarlize(python_interface_name, lower=False) + "_" + python_function_name.upper()

                if function_call_convention == "__stdcall":
                    python_function_type = "ctypes.WINFUNCTYPE"
                elif function_call_convention == "__cdecl":
                    python_function_type = "ctypes.CFUNCTYPE"
                else:
                    raise Exception("Unknown call convention `{0}`".format(function_call_convention))
                
                python_function_return_ctype = convert_raw_argument_to_python_ctype(function_return_type)
                python_function_argument_ctypes = convert_raw_arguments_to_python_ctypes(function_arguments)
                
                python_function_return_python_type = convert_raw_argument_to_python_type(function_return_type)
                python_function_argument_python_types = convert_raw_arguments_to_python_types(function_arguments)
                
                python_function_argument_names = convert_raw_arguments_to_names(function_arguments)

                python_interface_functions.append({
                    "name": python_function_name,
                    
                    "type": python_function_type,

                    "global_name": python_global_function_name,
                    "offset": function_offset,
                    
                    "return_ctype": python_function_return_ctype,
                    "argument_ctypes": python_function_argument_ctypes,

                    "return_python_type": python_function_return_python_type,
                    "argument_python_types": python_function_argument_python_types,

                    "argument_names": python_function_argument_names,
                })

                output_code += python_global_function_name + " = None" + "\n"

            function_offset += 8
        
        output_code += "\n"
        output_code += "def " + python_global_load_functions_name + "(function_table_address: int):" + "\n"
        output_code += "    global IS_FUNCTIONS_LOADED\n"
        output_code += "    \n"
        output_code += "    if IS_FUNCTIONS_LOADED:" + "\n"
        output_code += "        return" + "\n"

        for python_interface_function in python_interface_functions:
            python_function_type = python_interface_function['type']
        
            output_code += "    " + "\n"
            output_code += "    function_address = ctypes.cast(function_table_address + " + str(python_interface_function['offset']) + ", ctypes.POINTER(ctypes.c_void_p))[0]\n"
            output_code += "    global " + python_interface_function['global_name'] + "\n"
            output_code += "    " + python_interface_function['global_name'] + " = "
            output_code += "" + python_interface_function['type'] + "("

            output_code += python_interface_function['return_ctype']
            output_code += ", wintypes.LPVOID" # This

            for argument_ctype in python_interface_function['argument_ctypes']:
                output_code += ", " + argument_ctype

            output_code += ")"
            output_code += "(function_address)" + "\n"

        output_code += "        " + "\n"
        output_code += "    IS_FUNCTIONS_LOADED = True" + "\n"

        output_code += "\n"

        output_code += "class " + python_interface_name + ":\n"
        output_code += "    address: int = None" + "\n"
        output_code += "    " + "\n"
        output_code += "    def __init__(self, address: int):" + "\n"
        output_code += "        self.address = address" + "\n"
        output_code += "        " + "\n"
        output_code += "        function_table_address = ctypes.cast(address, ctypes.POINTER(ctypes.c_void_p))[0]" + "\n"
        output_code += "        " + python_global_load_functions_name + "(function_table_address)" + "\n"
        output_code += "    " + "\n"

        for python_interface_function in python_interface_functions:
            output_code += "    def " + python_interface_function['name'] + "(self"

            for argument_index in range(len(python_interface_function['argument_names'])):
                argument_name = python_interface_function['argument_names'][argument_index]
                argument_python_type = python_interface_function['argument_python_types'][argument_index]

                if argument_python_type:
                    output_code += ", "
                    output_code += argument_name
                    output_code += ": "
                    output_code += argument_python_type
                else:
                    output_code += ", "
                    output_code += argument_name

            output_code += ")"

            output_code += " -> "
            output_code += python_interface_function['return_python_type']

            output_code += ":" + "\n"
            
            if python_interface_function['return_python_type'] != "None":
                output_code += "        return " + python_interface_function['global_name'] + "(" + (", ".join(["self.address"] + python_interface_function['argument_names'])) + ")\n"
            else:
                output_code += "        " + python_interface_function['global_name'] + "(" + (", ".join(["self.address"] + python_interface_function['argument_names'])) + ")\n"
            output_code += "    " + "\n"
                
        with open(OUTPUT_DIRECTORY + "/" + underbarlize(python_interface_name, lower=True) + ".py", 'w') as file:
            file.write(output_code)
            
# Struct Generate
for parsed_struct in parsed_structs:
    struct_name = parsed_struct['name']
    struct_fields = parsed_struct['fields']

    if struct_name in GENERATE_TARGETS:
        output_code = ""

        python_struct_name = convert_name_with_hint(struct_name)
        
        output_code += "import ctypes" + "\n"
        output_code += "import ctypes.wintypes as wintypes" + "\n"
        output_code += "\n"
        
        output_code += "class " + python_struct_name + "(ctypes.Structure):" + "\n"
        output_code += "    _fields_ = (" + "\n"
        
        python_struct_fields = []

        for field in struct_fields:
            python_struct_field = {
                "name": underbarlize(field['name'], lower=True),
                "ctype": convert_raw_argument_to_python_ctype(field['type']),
            }

            python_struct_fields.append(python_struct_field)

            output_code += "        ('" + python_struct_field['name'] + "', " + python_struct_field['ctype'] + ")," + "\n"
        
        output_code += "    )" + "\n"
        output_code += "\n"
        output_code += "    def __repr__(self):" + "\n"
        output_code += "        return f'" + python_struct_name
        output_code += "("

        presentations = []
        for python_struct_field in python_struct_fields:
            presentations.append(python_struct_field['name'] + "={self." + python_struct_field['name'] + "}")
        output_code += ", ".join(presentations)

        output_code += ")'" + "\n"
        
        with open(OUTPUT_DIRECTORY + "/" + underbarlize(python_struct_name, lower=True) + ".py", 'w') as file:
            file.write(output_code)
