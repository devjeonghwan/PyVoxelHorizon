import os
from sctokenizer import Source, TokenType

HEADER_FILE_NAMES = ["header/IGameHookController.h", "header/typedef.h", "header/math.inl", "header/patch.h"]
GENERATE_TARGETS = [
    # Type Define
    "WEB_CLIENT_HANDLE",

    # Enum
    "VH_EDIT_MODE",
    "PLANE_AXIS_TYPE",
    "RENDER_MODE",
    "CREATE_VOXEL_OBJECT_ERROR",
    "MIDI_SIGNAL_TYPE",

    # Interface
    "IVHController",
    "IVHNetworkLayer",
    "IVoxelObjectLite",

    # Struct
    "VOXEL_OBJ_PROPERTY",
    "VOXEL_DESC_LITE",

    "AABB",

    "BOUNDING_SPHERE",
    "TRIANGLE",
    "RECT",

    "PLANE",

    "VECTOR3",
    "INT_VECTOR3",

    "VECTOR4",
    "INT_VECTOR4",

    "IVERTEX",
    "IVERTEX_QUAD",

    "MIDI_NOTE",
    "MIDI_DEVICE_INFO",
]

IGNORES = ["SetOnDeleteVoxelObjectFunc"]
HINTS = {
    "IVHController": {
        "name": "GameController",
        "functions": {
            "CreateVoxelObject": {
                "overloads": [
                    {"name": "CreateVoxelObject", "order": 1},
                    {"name": "CreateVoxelObjectAdvanced", "order": 0},
                ]
            },
            "IsValidVoxelObjectPosition": {
                "overloads": [
                    {"name": "IsValidVoxelObjectPosition", "order": 1},
                    {"name": "IsValidVoxelObjectIntPosition", "order": 0},
                ]
            },
        }
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
    "VOXEL_DESC_LITE": {
        "name": "VoxelDescriptionLite"
    },

    "BOUNDING_SPHERE": {
        "name": "BoundingSphere"
    },
    "TRIANGLE": {
        "name": "Triangle"
    },
    "RECT": {
        "name": "Rect"
    },

    "PLANE": {
        "name": "Plane"
    },

    "VECTOR3": {
        "name": "Vector3"
    },
    "INT_VECTOR3": {
        "name": "IntVector3"
    },

    "VECTOR4": {
        "name": "Vector4"
    },
    "INT_VECTOR4": {
        "name": "IntVector4"
    },

    "IVERTEX": {
        "name": "Vertex"
    },
    "IVERTEX_QUAD": {
        "name": "VertexQuad"
    },

    "MIDI_NOTE": {
        "name": "MidiNote"
    },
}

UTIL_MODULE_PATH = "pyvoxelhorizon.util"

ENUM_OUTPUT_DIRECTORY = "generated/enum"
ENUM_MODULE_PATH = "pyvoxelhorizon.enum"

INTERFACE_OUTPUT_DIRECTORY = "generated/interface"
INTERFACE_MODULE_PATH = "pyvoxelhorizon.interface"

STRUCT_OUTPUT_DIRECTORY = "generated/struct"
STRUCT_MODULE_PATH = "pyvoxelhorizon.struct"

ENUM_SOURCE_PREFIX = ""
ENUM_SOURCE_PREFIX += "import ctypes" + "\n"
ENUM_SOURCE_PREFIX += "import ctypes.wintypes as wintypes" + "\n"
ENUM_SOURCE_PREFIX += "\n"
ENUM_SOURCE_PREFIX += "from " + UTIL_MODULE_PATH + " import *" + "\n"
ENUM_SOURCE_PREFIX += "\n"

INTERFACE_SOURCE_PREFIX = ""
INTERFACE_SOURCE_PREFIX += "import ctypes" + "\n"
INTERFACE_SOURCE_PREFIX += "import ctypes.wintypes as wintypes" + "\n"
INTERFACE_SOURCE_PREFIX += "\n"
INTERFACE_SOURCE_PREFIX += "from " + UTIL_MODULE_PATH + " import *" + "\n"
INTERFACE_SOURCE_PREFIX += "from " + ENUM_MODULE_PATH + " import *" + "\n"

STRUCT_SOURCE_PREFIX = ""
STRUCT_SOURCE_PREFIX += "import ctypes" + "\n"
STRUCT_SOURCE_PREFIX += "import ctypes.wintypes as wintypes" + "\n"
STRUCT_SOURCE_PREFIX += "\n"
STRUCT_SOURCE_PREFIX += "from " + UTIL_MODULE_PATH + " import *" + "\n"
STRUCT_SOURCE_PREFIX += "from " + ENUM_MODULE_PATH + " import *" + "\n"

parsed_typedefs = []
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

    for index in range(1, len(tokens)):
        first_token = tokens[index - 1]
        second_token = tokens[index]

        if first_token.token_type == TokenType.OPERATOR:
            if first_token.token_value == 'and' or first_token.token_value == 'or' or first_token.token_value == 'xor' or first_token.token_value == 'not':

                if second_token.token_type == TokenType.IDENTIFIER:
                    # Merge
                    second_token.token_value = first_token.token_value + second_token.token_value

                    first_token.token_type = TokenType.IDENTIFIER
                    first_token.token_value = ""

    cursor = 0

    while True:
        if cursor >= len(tokens):
            break

        token = tokens[cursor]
        token_type = token.token_type
        token_value = token.token_value

        # Enum Parse
        if token_value == 'typedef':
            typedef_tokens = []

            while True:
                cursor += 1

                if cursor >= len(tokens):
                    break

                token = tokens[cursor]
                token_type = token.token_type
                token_value = token.token_value

                if token_type == TokenType.SPECIAL_SYMBOL and token_value == ';':
                    add_type_with_tokens(parsed_typedefs, typedef_tokens)
                    break
                else:
                    typedef_tokens.append(token)

            continue
        elif token_value == 'enum':
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
                elif brace_count == 0:
                    if token_type == TokenType.SPECIAL_SYMBOL and token_value == ';':
                        break

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

                                if (
                                        token_type == TokenType.KEYWORD and token_value != "virtual") or token_type == TokenType.IDENTIFIER:
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
                elif brace_count == 0:
                    if token_type == TokenType.SPECIAL_SYMBOL and token_value == ';':
                        break
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

target_typedefs = []
target_enums = []
target_interfaces = []
target_structs = []

target_typedef_names = []
target_enum_names = []
target_interface_names = []
target_struct_names = []

for target_name in GENERATE_TARGETS:
    for parsed_typedef in parsed_typedefs:
        if parsed_typedef['name'] == target_name:
            target_typedefs.append(parsed_typedef)
            target_typedef_names.append(parsed_typedef['name'])
            break

for target_name in GENERATE_TARGETS:
    for parsed_enum in parsed_enums:
        if parsed_enum['name'] == target_name:
            target_enums.append(parsed_enum)
            target_enum_names.append(parsed_enum['name'])
            break

for target_name in GENERATE_TARGETS:
    for parsed_interface in parsed_interfaces:
        if parsed_interface['name'] == target_name:
            target_interfaces.append(parsed_interface)
            target_interface_names.append(parsed_interface['name'])
            break

for target_name in GENERATE_TARGETS:
    for parsed_struct in parsed_structs:
        if parsed_struct['name'] == target_name:
            target_structs.append(parsed_struct)
            target_struct_names.append(parsed_struct['name'])
            break


def convert_name_with_hint(name):
    if name in HINTS:
        if "name" in HINTS[name]:
            return HINTS[name]['name']

    return name


def convert_typedefs(type_name):
    for target_typedef in target_typedefs:
        if type_name in target_typedef['name']:
            return type_name.replace(target_typedef['name'], target_typedef['type'])

    return type_name


def is_hint_name(name):
    for hint_name in HINTS:
        hint = HINTS[hint_name]

        if "name" in hint and hint['name'] == name:
            return True

    return False


def underbarlize(name, lower=False):
    new_name = ""

    if not "_" in name:
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
    else:
        new_name = name

    if lower:
        return new_name.lower()

    return new_name.upper()


def remove_array_part(raw_type):
    if "[" in raw_type:
        raw_split = raw_type.split("[")

        return raw_split[0]

    return raw_type


def ignore_multiply_one(value, multiplier):
    if multiplier == 1:
        return value

    return value + " * " + str(multiplier)


def convert_raw_type_to_python_ctype(raw_type):
    raw_type = convert_typedefs(raw_type)
    multiplier = 1

    if "[" in raw_type:
        raw_split = raw_type.split("[")

        type_part = raw_split[0]
        index_part = raw_split[1]
        index_part = index_part[0:len(index_part) - 1]

        raw_type = type_part
        multiplier = int(index_part)

    if raw_type == "void":
        return "None"

    elif raw_type == "unsignedchar":
        return ignore_multiply_one("ctypes.c_ubyte", multiplier)

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
    elif raw_type == "LONG":
        return ignore_multiply_one("wintypes.LONG", multiplier)
    elif raw_type == "FLOAT":
        return ignore_multiply_one("wintypes.FLOAT", multiplier)

    elif raw_type == "int":
        return ignore_multiply_one("ctypes.c_int", multiplier)
    elif raw_type == "long":
        return ignore_multiply_one("ctypes.c_long", multiplier)
    elif raw_type == "float":
        return ignore_multiply_one("ctypes.c_float", multiplier)

    elif raw_type == "...":
        return "..."

    elif raw_type in target_enum_names:
        return ignore_multiply_one("ctypes.c_int", multiplier)

    elif raw_type in target_struct_names:
        return ignore_multiply_one(convert_name_with_hint(raw_type), multiplier)

    else:
        raise Exception("Unknown argument type `{0}`".format(raw_type))


def convert_raw_arguments_to_python_ctypes(raw_arguments):
    python_ctypes = []

    for raw_argument in raw_arguments:
        python_ctype = convert_raw_type_to_python_ctype(raw_argument['type'])

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


def convert_raw_type_to_python_type_info(raw_type, is_return_type: bool = False):
    raw_type = convert_typedefs(raw_type)

    if raw_type == "void":
        return {"type": "None", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "void*":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "void**":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "unsignedchar":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "CHAR":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "CHAR*":
        return {"type": "str", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "WCHAR":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "WCHAR*":
        return {"type": "str", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "char":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "char*":
        return {"type": "str", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "wchar":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "wchar*":
        return {"type": "str", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "WORD":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "DWORD":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "WORD*":
        return {"type": "wintypes.WORD", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, wintypes.WORD)"}
    elif raw_type == "DWORD*":
        return {"type": "wintypes.DWORD", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, wintypes.DWORD)"}

    elif raw_type == "BOOL":
        return {"type": "bool", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "BYTE":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "UINT":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "INT":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "BOOL*":
        return {"type": "wintypes.BOOL", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, wintypes.BOOL)"}
    elif raw_type == "BYTE*":
        return {"type": "wintypes.BYTE", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, wintypes.BYTE)"}
    elif raw_type == "UINT*":
        return {"type": "wintypes.UINT", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, wintypes.UINT)"}
    elif raw_type == "INT*":
        return {"type": "wintypes.INT", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, wintypes.INT)"}

    elif raw_type == "int":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "unsignedlong":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "long":
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}
    elif raw_type == "float":
        return {"type": "float", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type == "int*":
        return {"type": "ctypes.c_int", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, ctypes.c_int)"}
    elif raw_type == "unsignedlong*":
        return {"type": "ctypes.c_uint", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, ctypes.c_uint)"}
    elif raw_type == "long*":
        return {"type": "ctypes.c_int", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, ctypes.c_int)"}
    elif raw_type == "float*":
        return {"type": "ctypes.c_float", "from_statement": "get_address({0})",
                "to_statement": "cast_address({0}, ctypes.c_float)"}

    elif raw_type == "...":
        return {"type": "...", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type in target_enum_names:
        return {"type": "int", "from_statement": "{0}", "to_statement": "{0}"}

    elif raw_type in target_struct_names:
        return {"type": convert_name_with_hint(raw_type), "from_statement": "{0}", "to_statement": "{0}"}

    else:
        if raw_type.endswith('*'):
            pointer_depth = 0

            while True:
                position = len(raw_type) - pointer_depth

                if raw_type[position - 1: position] == '*':
                    pointer_depth += 1
                else:
                    break

            new_type = raw_type.rstrip('*')

            if pointer_depth == 1:
                if new_type in target_enum_names:
                    new_type = convert_name_with_hint(new_type)

                    return {"type": "wintypes.INT", "from_statement": "get_address({0})",
                            "to_statement": "cast_address({0}, wintypes.INT)"}
                elif new_type in target_struct_names or new_type in target_interface_names:
                    new_type = convert_name_with_hint(new_type)

                    return {"type": new_type, "from_statement": "get_address({0})",
                            "to_statement": "cast_address({0}, " + new_type + ")"}
            elif pointer_depth == 2:
                if not is_return_type:
                    if new_type in target_enum_names:
                        new_type = convert_name_with_hint(new_type)

                        return {"type": "list[wintypes.INT]", "from_statement": "get_addresses_pointer({0})",
                                "to_statement": None}
                    elif new_type in target_struct_names or new_type in target_interface_names:
                        new_type = convert_name_with_hint(new_type)

                        return {"type": "list[" + new_type + "]", "from_statement": "get_addresses_pointer({0})",
                                "to_statement": None}

        raise Exception("Unknown argument type `{0}`".format(raw_type))


def convert_raw_arguments_to_python_argument_type_infos_and_names(raw_arguments):
    python_type_infos = []
    python_type_names = []

    for raw_argument in raw_arguments:
        python_type_info = convert_raw_type_to_python_type_info(raw_argument['type'])
        python_type = python_type_info['type']

        if python_type == "...":
            previous_type_info = python_type_infos.pop()
            python_type_names.pop()

            if previous_type_info['type'] == "str":
                python_type_infos.append({"type": "", "from_statement": "{0}", "to_statement": "{0}"})
                python_type_names.append("*args")
            else:
                raise Exception("Unknown variable length argument type info `{0}`".format(previous_type_info))
        else:
            python_type_infos.append(python_type_info)
            python_type_names.append(underbarlize(raw_argument['name'], lower=True))

    return (python_type_infos, python_type_names)


def write_init_file(init_modules, path):
    output_source = ""

    for init_module in init_modules:
        output_source += "from ." + init_module['module_name'] + " import " + (', '.join(init_module['names'])) + "\n"

    output_source += "\n"
    output_source += "__all__ = [" + "\n"
    for init_module in init_modules:
        for name in init_module['names']:
            output_source += "    '" + name + "'," + "\n"

        if len(init_module['names']) > 1:
            output_source += "\n"

    output_source = output_source.rstrip('\n')
    output_source += "\n"
    output_source += "]"

    with open(path, 'w') as file:
        file.write(output_source)


def resolve_import(raw_type_name):
    name_for_check_import = remove_array_part(raw_type_name.replace('*', '').strip())

    if name_for_check_import in target_struct_names:
        name_for_check_import = convert_name_with_hint(name_for_check_import)
        return (STRUCT_MODULE_PATH + "." + underbarlize(name_for_check_import, lower=True), name_for_check_import)
    elif name_for_check_import in target_interface_names:
        name_for_check_import = convert_name_with_hint(name_for_check_import)
        return (INTERFACE_MODULE_PATH + "." + underbarlize(name_for_check_import, lower=True), name_for_check_import)

    return (None, None)


if not os.path.exists(ENUM_OUTPUT_DIRECTORY):
    os.makedirs(ENUM_OUTPUT_DIRECTORY)
if not os.path.exists(INTERFACE_OUTPUT_DIRECTORY):
    os.makedirs(INTERFACE_OUTPUT_DIRECTORY)
if not os.path.exists(STRUCT_OUTPUT_DIRECTORY):
    os.makedirs(STRUCT_OUTPUT_DIRECTORY)

# Enum Generate
enum_init_modules = []

for target_enum in target_enums:
    enum_name = target_enum['name']
    enum_types = target_enum['types']

    output_source = ENUM_SOURCE_PREFIX
    python_enum_name = convert_name_with_hint(enum_name)

    enum_init_module = {
        'module_name': underbarlize(python_enum_name, lower=True),
        'names': []
    }

    python_enums = []

    for enum_type in enum_types:
        enum_type_name = convert_name_with_hint(enum_type['name'])
        enum_type_value = enum_type['value']

        if not enum_type_name.startswith(enum_name):
            enum_type_name = enum_name + "_" + enum_type_name

        python_enum = {
            "name": enum_type_name,
            "value": enum_type_value
        }

        enum_init_module['names'].append(enum_type_name)
        python_enums.append(python_enum)

    for python_enum in python_enums:
        output_source += python_enum["name"] + " = " + str(python_enum["value"]) + "\n"

    output_source += "\n"
    output_source += "\n"

    python_get_string_function_name = "get_" + underbarlize(python_enum_name, lower=True) + "_string"
    enum_init_module['names'].append(python_get_string_function_name)

    output_source += "def " + python_get_string_function_name + "(value: int):" + "\n"

    first_enum = True
    for python_enum in python_enums:
        if first_enum:
            output_source += "    if value == " + str(python_enum["value"]) + ":" + "\n"
        else:
            output_source += "    elif value == " + str(python_enum["value"]) + ":" + "\n"

        output_source += "        return '" + python_enum["name"] + "'" + "\n"

    output_source += "    " + "\n"
    output_source += "    return '" + python_enum_name + "_UNKNOWN'" + "\n"

    enum_init_modules.append(enum_init_module)

    with open(ENUM_OUTPUT_DIRECTORY + "/" + enum_init_module['module_name'] + ".py", 'w') as file:
        file.write(output_source)

write_init_file(enum_init_modules, ENUM_OUTPUT_DIRECTORY + "/__init__.py")

# Interface Generate
interface_init_modules = []

for target_interface in target_interfaces:
    interface_name = target_interface['name']
    interface_functions = target_interface['functions']

    interface_hint = HINTS[interface_name] if interface_name in HINTS else {}
    interface_functions_hint = interface_hint['functions'] if 'functions' in interface_hint else {}

    output_source = INTERFACE_SOURCE_PREFIX
    python_interface_name = convert_name_with_hint(interface_name)

    interface_init_module = {
        'module_name': underbarlize(python_interface_name, lower=True),
        'names': [python_interface_name],
        "imports": []
    }

    python_global_load_functions_name = "load_functions_of_" + underbarlize(python_interface_name, lower=True)
    python_interface_functions = []

    function_index = 0

    for function in interface_functions:
        function_name = function['name']
        function_call_convention = function['call_convention']
        function_return_type = function['return_type']
        function_arguments = function['arguments']

        if not function_name in IGNORES:
            function_offset = function_index * 8

            overload_index = 0
            overload_targets = []

            function_index_for_check = 0

            for function_for_check in interface_functions:
                if function_for_check['name'] == function_name:
                    if function_for_check == function:
                        overload_index = len(overload_targets)

                    overload_targets.append(function_index_for_check)
                function_index_for_check += 1

            is_overloaded = len(overload_targets) > 1

            if is_overloaded:
                # MSVC uses reversed offset for overload functions
                function_offset = overload_targets[(len(overload_targets) - 1) - overload_index] * 8
                python_function_name = function_name + "Offset" + str(function_offset)

                if function_name in interface_functions_hint:
                    function_hint = interface_functions_hint[function_name]

                    if ('overloads' in function_hint):
                        overload_hint = function_hint['overloads']

                        if len(overload_hint) <= overload_index:
                            raise Exception(
                                "Not enough overload hints for `{0}::{1}`".format(interface_name, function_name))

                        overload_function_hint = overload_hint[overload_index]

                        function_offset = overload_targets[overload_function_hint['order']] * 8
                        python_function_name = overload_function_hint['name']
            else:
                python_function_name = function_name

                if function_name in interface_functions_hint:
                    function_hint = interface_functions_hint[function_name]

                    if 'name' in function_hint:
                        python_function_name = function_hint['name']

            python_function_name = underbarlize(python_function_name, lower=True)
            python_global_function_name = "FUNCTION_" + underbarlize(python_interface_name,
                                                                     lower=False) + "_" + python_function_name.upper()

            if function_call_convention == "__stdcall":
                python_function_type = "ctypes.WINFUNCTYPE"
            elif function_call_convention == "__cdecl":
                python_function_type = "ctypes.CFUNCTYPE"
            else:
                raise Exception("Unknown call convention `{0}`".format(function_call_convention))

            python_function_return_ctype = convert_raw_type_to_python_ctype(function_return_type)
            python_function_argument_ctypes = convert_raw_arguments_to_python_ctypes(function_arguments)

            python_function_python_return_type_info = convert_raw_type_to_python_type_info(function_return_type,
                                                                                           is_return_type=True)
            python_function_python_argument_type_infos, python_function_argument_names = convert_raw_arguments_to_python_argument_type_infos_and_names(
                function_arguments)

            python_interface_functions.append({
                "name": python_function_name,

                "type": python_function_type,

                "global_name": python_global_function_name,
                "offset": function_offset,

                "return_ctype": python_function_return_ctype,
                "argument_ctypes": python_function_argument_ctypes,

                "python_return_type_info": python_function_python_return_type_info,
                "python_argument_type_infos": python_function_python_argument_type_infos,

                "python_argument_names": python_function_argument_names
            })

            import_module, import_name = resolve_import(function_return_type)
            if import_module and import_name and (not (import_module, import_name) in interface_init_module['imports']):
                output_source += "from " + import_module + " import " + import_name + "\n"
                interface_init_module['imports'].append((import_module, import_name))

            for function_argument in function_arguments:
                import_module, import_name = resolve_import(function_argument['type'])
                if import_module and import_name and (
                not (import_module, import_name) in interface_init_module['imports']):
                    output_source += "from " + import_module + " import " + import_name + "\n"
                    interface_init_module['imports'].append((import_module, import_name))

        function_index += 1

    output_source += "\n"
    output_source += "IS_FUNCTIONS_LOADED = False" + "\n"
    output_source += "\n"

    for python_interface_function in python_interface_functions:
        output_source += python_interface_function['global_name'] + " = None" + "\n"

    output_source += "\n"
    output_source += "def " + python_global_load_functions_name + "(function_table_address: int):" + "\n"
    output_source += "    global IS_FUNCTIONS_LOADED\n"
    output_source += "    \n"
    output_source += "    if IS_FUNCTIONS_LOADED:" + "\n"
    output_source += "        return" + "\n"

    for python_interface_function in python_interface_functions:
        python_function_type = python_interface_function['type']

        output_source += "    " + "\n"
        output_source += "    function_address = read_memory(function_table_address + " + str(
            python_interface_function['offset']) + ", ctypes.c_void_p)\n"
        output_source += "    global " + python_interface_function['global_name'] + "\n"
        output_source += "    " + python_interface_function['global_name'] + " = "
        output_source += "" + python_interface_function['type'] + "("

        output_source += python_interface_function['return_ctype']
        output_source += ", wintypes.LPVOID"  # This

        for argument_ctype in python_interface_function['argument_ctypes']:
            output_source += ", " + argument_ctype

        output_source += ")"
        output_source += "(function_address)" + "\n"

    output_source += "        " + "\n"
    output_source += "    IS_FUNCTIONS_LOADED = True" + "\n"

    output_source += "\n"

    output_source += "class " + python_interface_name + "(AddressObject):\n"
    output_source += "    def __init__(self, address: int):" + "\n"
    output_source += "        super().__init__(address)" + "\n"
    output_source += "        " + "\n"
    output_source += "        function_table_address = read_memory(address, ctypes.c_void_p)" + "\n"
    output_source += "        " + python_global_load_functions_name + "(function_table_address)" + "\n"
    output_source += "    " + "\n"

    for python_interface_function in python_interface_functions:
        python_return_type_info = python_interface_function['python_return_type_info']
        python_argument_type_infos = python_interface_function['python_argument_type_infos']
        python_argument_names = python_interface_function['python_argument_names']

        output_source += "    def " + python_interface_function['name'] + "(self"

        for argument_index in range(len(python_argument_names)):
            python_argument_type = python_argument_type_infos[argument_index]['type']
            python_argument_name = python_argument_names[argument_index]

            if python_argument_type:
                output_source += ", "
                output_source += python_argument_name
                output_source += ": "
                output_source += python_argument_type
            else:
                output_source += ", "
                output_source += python_argument_name

        output_source += ")"

        output_source += " -> "
        output_source += python_return_type_info['type']

        output_source += ":" + "\n"

        for argument_index in range(len(python_argument_names)):
            python_argument_type_info = python_argument_type_infos[argument_index]
            python_argument_name = python_argument_names[argument_index]

            python_from_statement = python_argument_type_info['from_statement'].format(python_argument_name)

            if python_from_statement != python_argument_name:
                output_source += "        " + python_argument_name + " = " + python_from_statement + "\n"

        output_source += "        " + "\n"

        calling_function = python_interface_function['global_name'] + "(" + (
            ", ".join(["self.address"] + python_argument_names)) + ")"
        output_source += "        return " + python_return_type_info['to_statement'].format(calling_function) + "\n"

        output_source += "    " + "\n"

    interface_init_modules.append(interface_init_module)

    with open(INTERFACE_OUTPUT_DIRECTORY + "/" + interface_init_module['module_name'] + ".py", 'w') as file:
        file.write(output_source)

write_init_file(interface_init_modules, INTERFACE_OUTPUT_DIRECTORY + "/__init__.py")

# Struct Generate
struct_init_modules = []

for target_struct in target_structs:
    struct_name = target_struct['name']
    struct_fields = target_struct['fields']

    output_source = STRUCT_SOURCE_PREFIX
    python_struct_name = convert_name_with_hint(struct_name)

    struct_init_module = {
        'module_name': underbarlize(python_struct_name, lower=True),
        'names': [python_struct_name],
        'imports': []
    }

    python_struct_fields = []

    for field in struct_fields:
        python_struct_field = {
            "name": underbarlize(field['name'], lower=True),
            "ctype": convert_raw_type_to_python_ctype(field['type']),
        }

        python_struct_fields.append(python_struct_field)

        import_module, import_name = resolve_import(field['type'])
        if import_module and import_name and (not (import_module, import_name) in struct_init_module['imports']):
            output_source += "from " + import_module + " import " + import_name + "\n"
            struct_init_module['imports'].append((import_module, import_name))

    output_source += "\n"
    output_source += "class " + python_struct_name + "(ctypes.Structure):" + "\n"
    output_source += "    _fields_ = (" + "\n"

    for python_struct_field in python_struct_fields:
        output_source += "        ('" + python_struct_field['name'] + "', " + python_struct_field['ctype'] + ")," + "\n"

    output_source += "    )" + "\n"
    output_source += "\n"
    output_source += "    def __repr__(self):" + "\n"
    output_source += "        return f'" + python_struct_name
    output_source += "("

    presentations = []
    for python_struct_field in python_struct_fields:
        presentations.append(python_struct_field['name'] + "={self." + python_struct_field['name'] + "}")
    output_source += ", ".join(presentations)

    output_source += ")'" + "\n"

    struct_init_modules.append(struct_init_module)

    with open(STRUCT_OUTPUT_DIRECTORY + "/" + struct_init_module['module_name'] + ".py", 'w') as file:
        file.write(output_source)

write_init_file(struct_init_modules, STRUCT_OUTPUT_DIRECTORY + "/__init__.py")
