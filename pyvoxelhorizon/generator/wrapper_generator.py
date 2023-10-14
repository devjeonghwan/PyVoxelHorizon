import os
from sctokenizer import Source, TokenType

HEADER_FILE_NAMES = ["header/IGameHookController.h", "header/typedef.h"]
GENERATE_TARGETS = [
    "VH_EDIT_MODE", 
    "IVHController", 
    "IVHNetworkLayer", 
    "IVoxelObjectLite",
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
    }
}

OUTPUT_DIRECTORY = "generated/"

parsed_enums = []
parsed_interfaces = []

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

                                def check_token_append(output_enum_types, argument_tokens):
                                    argument_type_tokens = argument_tokens[0:len(argument_tokens) - 1]
                                    argument_name = argument_tokens[len(argument_tokens) - 1].token_value

                                    argument_type = ""

                                    for argument_type_token in argument_type_tokens:
                                        argument_type += argument_type_token.token_value

                                    output_enum_types.append({
                                        'type': argument_type,
                                        'name': argument_name
                                    })

                                while True:
                                    if cursor >= len(tokens):
                                        break
                                    
                                    token = tokens[cursor]
                                    token_type = token.token_type
                                    token_value = token.token_value

                                    if token_type == TokenType.OPERATOR and token_value == ',':
                                        check_token_append(output_function['arguments'], argument_tokens)
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
                                    check_token_append(output_function['arguments'], argument_tokens)

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
        cursor += 1

output_enum_names = [parsed_enum['name'] for parsed_enum in parsed_enums]
output_interface_names = [parsed_interface['name'] for parsed_interface in parsed_interfaces]

def underbarlize(name, lower=False):
    new_name = ""

    letter_cursor = 0
    while True:
        if letter_cursor >= len(name):
            break

        word = name[letter_cursor]

        if word.isupper():
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
                
            if letter_cursor != 0:
                new_name += "_"

        new_name += word

        letter_cursor += 1
    
    if lower:
        return new_name.lower()
    
    return new_name.upper()

def convert_raw_argument_to_python_ctype(raw_type):
    if raw_type == "CHAR":
        return "wintypes.CHAR"
    elif raw_type == "CHAR*":
        return "ctypes.c_char_p"
    
    elif raw_type == "WCHAR":
        return "wintypes.WCHAR"
    elif raw_type == "WCHAR*":
        return "ctypes.c_wchar_p"
    
    elif raw_type == "char":
        return "ctypes.c_char"
    elif raw_type == "char*":
        return "ctypes.c_char_p"
    
    elif raw_type == "wchar":
        return "ctypes.c_wchar"
    elif raw_type == "wchar*":
        return "ctypes.c_wchar_p"
    
    elif raw_type.endswith("*"):
        return "wintypes.LPVOID"
    
    elif raw_type == "WORD":
        return "wintypes.WORD"
    elif raw_type == "DWORD":
        return "wintypes.DWORD"
    elif raw_type == "BOOL":
        return "wintypes.BOOL"
    elif raw_type == "BYTE":
        return "wintypes.BYTE"
    elif raw_type == "UINT":
        return "wintypes.UINT"
    elif raw_type == "INT":
        return "wintypes.INT"
    
    elif raw_type == "int":
        return "ctypes.c_int"
    elif raw_type == "long":
        return "ctypes.c_long"
    elif raw_type == "float":
        return "ctypes.c_float"
    
    elif raw_type == "..":
        return "..."
    
    elif raw_type in output_enum_names:
        return "ctypes.c_int"
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
    if raw_type == "CHAR":
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
    
    elif raw_type == "..":
        return "..."
    
    elif raw_type in output_enum_names:
        return "int"
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
    
    return python_names, python_types

os.makedirs(OUTPUT_DIRECTORY)

# Enum Generate
for parsed_enum in parsed_enums:
    enum_name = parsed_enum['name']

    if enum_name in GENERATE_TARGETS:
        output_code = ""
        enum_types = parsed_enum['types']

        for enum_type in enum_types:
            enum_type_name = enum_type['name']
            enum_type_value = enum_type['value']

            if enum_type_name in HINTS:
                if "name" in HINTS[enum_type_name]:
                    enum_type_name = HINTS[enum_type_name]['name']

            if not enum_type_name.startswith(enum_name):
                enum_type_name = enum_name + "_" + enum_type_name

            output_code += enum_type_name + "\t = " + str(enum_type_value) + "\n"

        with open(OUTPUT_DIRECTORY + "/" + enum_name + ".py", 'w') as file:
            file.write(output_code)

# Interface Generate
for parsed_interface in parsed_interfaces:
    interface_name = parsed_interface['name']
    interface_functions = parsed_interface['functions']

    if interface_name in GENERATE_TARGETS:
        output_code = ""
        
        python_interface_name = interface_name  

        if python_interface_name in HINTS:
            if "name" in HINTS[python_interface_name]:
                python_interface_name = HINTS[python_interface_name]['name']
        
        python_global_load_functions_name = "load_functions_of_" + underbarlize(python_interface_name, lower=True)
        python_global_function_names = []
        python_function_names = []

        output_code += "import ctypes" + "\n"
        output_code += "import ctypes.wintypes as wintypes" + "\n"
        output_code += "\n"
        
        output_code += "IS_FUNCTIONS_LOADED = False"
        
        output_code += "\n"
        
        for function in interface_functions:
            function_name = function['name']

            if not function_name in IGNORES:
                python_function_name = underbarlize(function_name, lower=True)

                while python_function_name in python_function_names:
                    python_function_name = python_function_name + "_overloaded"
                
                python_global_function_name = "FUNCTION_" + underbarlize(python_interface_name, lower=False) + "_" + python_function_name.upper()

                python_function_names.append(python_function_name)
                python_global_function_names.append(python_global_function_name)

                output_code += python_global_function_name + " = None" + "\n"
        
        output_code += "\n"
        output_code += "def " + python_global_load_functions_name + "(function_table_address: int):" + "\n"
        output_code += "    global IS_FUNCTIONS_LOADED\n"
        output_code += "    \n"
        output_code += "    if IS_FUNCTIONS_LOADED:" + "\n"
        output_code += "        return" + "\n"

        function_index = 0
        function_offset = 0
        
        for function in interface_functions:
            function_name = function['name']
            function_call_convention = function['call_convention']
            function_return_type = function['return_type']
            function_arguments = function['arguments']

            if not function_name in IGNORES:
                python_function_type = ""
            
                if function_call_convention == "__stdcall":
                    python_function_type = "ctypes.WINFUNCTYPE"
                elif function_call_convention == "__cdecl":
                    python_function_type = "ctypes.CFUNCTYPE"
                else:
                    raise Exception("Unknown call convention `{0}`".format(function_call_convention))
                
                output_code += "    " + "\n"
                output_code += "    function_address = ctypes.cast(function_table_address + " + str(function_offset) + ", ctypes.POINTER(ctypes.c_void_p))[0]\n"
                output_code += "    global " + python_global_function_names[function_index] + "\n"
                output_code += "    " + python_global_function_names[function_index] + " = "
                output_code += "" + python_function_type + "("

                if function_return_type == "void":
                    output_code += "None"
                else:
                    output_code += convert_raw_argument_to_python_ctype(function_return_type)
                
                # This
                output_code += ", wintypes.LPVOID"

                python_function_ctypes = convert_raw_arguments_to_python_ctypes(function_arguments)

                for python_function_ctype in python_function_ctypes:
                    output_code += ", " + python_function_ctype

                output_code += ")"
                output_code += "(function_address)" + "\n"

                function_index += 1

            function_offset += 8

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

        function_index = 0

        for function in interface_functions:
            function_name = function['name']
            function_return_type = function['return_type']
            function_arguments = function['arguments']

            if not function_name in IGNORES:
                python_function_name = python_function_names[function_index]
                output_code += "    def " + python_function_name + "(self"

                python_function_argument_names, python_function_arguments_types = convert_raw_arguments_to_python_types_with_name(function_arguments)

                for argument_index in range(len(python_function_argument_names)):
                    python_name = python_function_argument_names[argument_index]
                    python_type = python_function_arguments_types[argument_index]

                    if python_type:
                        output_code += ", "
                        output_code += python_name
                        output_code += ": "
                        output_code += python_type
                    else:
                        output_code += ", "
                        output_code += python_name

                output_code += ")"

                output_code += " -> "

                if function_return_type != "void":
                    python_function_ctypes = convert_raw_argument_to_python_type(function_return_type)

                    output_code += python_function_ctypes
                else:
                    output_code += "None"

                output_code += ":" + "\n"
                
                if function_return_type != "void":
                    output_code += "        return " + python_global_function_names[function_index] + "(" + (", ".join(["self.address"] + python_function_argument_names)) + ")\n"
                else:
                    output_code += "        " + python_global_function_names[function_index] + "(" + (", ".join(["self.address"] + python_function_argument_names)) + ")\n"
                output_code += "    " + "\n"

                function_index += 1
                
        with open(OUTPUT_DIRECTORY + "/" + interface_name + ".py", 'w') as file:
            file.write(output_code)