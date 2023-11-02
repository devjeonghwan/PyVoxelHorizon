from __future__ import annotations

import ctypes

import time

from abc import *
from typing import TypeVar, Type, Callable, Any

from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.type import *
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.plugin.game.voxel import *
from pyvoxelhorizon.plugin.util import Color
from pyvoxelhorizon.struct import *

PLUGIN_NAME = "CircuitPlugin"

AND_GATE = 0
AND_GATE_SHAPES = [
    {
        "shape": [
            [[True, True, False]],
            [[True, True, True]],
            [[True, True, False]],
        ],
        "indicator": (2, 0, 1),
        "inputs": [(-1, 0, 0), (-1, 0, 2)],
        "output": (3, 0, 1)
    },
    {
        "shape": [
            [[True, True, True]],
            [[True, True, True]],
            [[False, True, False]],
        ],
        "indicator": (1, 0, 2),
        "inputs": [(0, 0, -1), (2, 0, -1)],
        "output": (1, 0, 3)
    },
    {
        "shape": [
            [[False, True, True]],
            [[True, True, True]],
            [[False, True, True]],
        ],
        "indicator": (0, 0, 1),
        "inputs": [(3, 0, 0), (3, 0, 2)],
        "output": (-1, 0, 1)
    },
    {
        "shape": [
            [[False, True, False]],
            [[True, True, True]],
            [[True, True, True]],
        ],
        "indicator": (1, 0, 0),
        "inputs": [(0, 0, 3), (2, 0, 3)],
        "output": (1, 0, -1)
    }
]

OR_GATE = 1
OR_GATE_SHAPES = [
    {
        "shape": [
            [[True, True, False]],
            [[False, True, True]],
            [[True, True, False]],
        ],
        "indicator": (2, 0, 1),
        "inputs": [(-1, 0, 0), (-1, 0, 2)],
        "output": (3, 0, 1)
    },
    {
        "shape": [
            [[True, False, True]],
            [[True, True, True]],
            [[False, True, False]],
        ],
        "indicator": (1, 0, 2),
        "inputs": [(0, 0, -1), (2, 0, -1)],
        "output": (1, 0, 3)
    },
    {
        "shape": [
            [[False, True, True]],
            [[True, True, False]],
            [[False, True, True]],
        ],
        "indicator": (0, 0, 1),
        "inputs": [(3, 0, 0), (3, 0, 2)],
        "output": (-1, 0, 1)
    },
    {
        "shape": [
            [[False, True, False]],
            [[True, True, True]],
            [[True, False, True]],
        ],
        "indicator": (1, 0, 0),
        "inputs": [(0, 0, 3), (2, 0, 3)],
        "output": (1, 0, -1)
    }
]

XOR_GATE = 2
XOR_GATE_SHAPES = [
    {
        "shape": [
            [[True, True, True]],
            [[False, False, True]],
            [[True, True, True]],
        ],
        "indicator": (2, 0, 1),
        "inputs": [(-1, 0, 0), (-1, 0, 2)],
        "output": (3, 0, 1)
    },
    {
        "shape": [
            [[True, False, True]],
            [[True, False, True]],
            [[True, True, True]],
        ],
        "indicator": (1, 0, 2),
        "inputs": [(0, 0, -1), (2, 0, -1)],
        "output": (1, 0, 3)
    },
    {
        "shape": [
            [[True, True, True]],
            [[True, False, False]],
            [[True, True, True]],
        ],
        "indicator": (0, 0, 1),
        "inputs": [(3, 0, 0), (3, 0, 2)],
        "output": (-1, 0, 1)
    },
    {
        "shape": [
            [[True, True, True]],
            [[True, False, True]],
            [[True, False, True]],
        ],
        "indicator": (1, 0, 0),
        "inputs": [(0, 0, 3), (2, 0, 3)],
        "output": (1, 0, -1)
    }
]

NOT_GATE = 3
NOT_GATE_SHAPES = [
    {
        "shape": [
            [[True, False, False]],
            [[True, True, True]],
            [[True, False, False]],
        ],
        "indicator": (2, 0, 1),
        "inputs": [(-1, 0, 1)],
        "output": (3, 0, 1)
    },
    {
        "shape": [
            [[True, True, True]],
            [[False, True, False]],
            [[False, True, False]],
        ],
        "indicator": (1, 0, 2),
        "inputs": [(1, 0, -1)],
        "output": (1, 0, 3)
    },
    {
        "shape": [
            [[False, False, True]],
            [[True, True, True]],
            [[False, False, True]],
        ],
        "indicator": (0, 0, 1),
        "inputs": [(3, 0, 1)],
        "output": (-1, 0, 1)
    },
    {
        "shape": [
            [[False, True, False]],
            [[False, True, False]],
            [[True, True, True]],
        ],
        "indicator": (1, 0, 0),
        "inputs": [(1, 0, 3)],
        "output": (1, 0, -1)
    }
]

DELAY_GATE = 6
DELAY_GATE_SHAPES = [
    {
        "shape": [
            [[True, False, False]],
            [[True, True, True]],
        ],
        "indicator": (2, 0, 1),
        "inputs": [(-1, 0, 1)],
        "output": (3, 0, 1)
    },
    {
        "shape": [
            [[True, True, True]],
            [[True, False, False]],
        ],
        "indicator": (2, 0, 0),
        "inputs": [(-1, 0, 0)],
        "output": (3, 0, 0)
    },
    {
        "shape": [
            [[True, True]],
            [[True, False]],
            [[True, False]],
        ],
        "indicator": (0, 0, 2),
        "inputs": [(0, 0, -1)],
        "output": (0, 0, 3)
    },
    {
        "shape": [
            [[True, True]],
            [[False, True]],
            [[False, True]],
        ],
        "indicator": (1, 0, 2),
        "inputs": [(1, 0, -1)],
        "output": (1, 0, 3)
    },
    {
        "shape": [
            [[True, True, True]],
            [[False, False, True]],
        ],
        "indicator": (0, 0, 0),
        "inputs": [(3, 0, 0)],
        "output": (-1, 0, 0)
    },
    {
        "shape": [
            [[False, False, True]],
            [[True, True, True]],
        ],
        "indicator": (0, 0, 1),
        "inputs": [(3, 0, 1)],
        "output": (-1, 0, 1)
    },
    {
        "shape": [
            [[False, True]],
            [[False, True]],
            [[True, True]],
        ],
        "indicator": (1, 0, 0),
        "inputs": [(1, 0, 3)],
        "output": (1, 0, -1)
    },
    {
        "shape": [
            [[True, False]],
            [[True, False]],
            [[True, True]],
        ],
        "indicator": (0, 0, 0),
        "inputs": [(0, 0, 3)],
        "output": (0, 0, -1)
    }
]

GATE_OFF_COLOR = 11
GATE_ON_COLOR = 29
GATE_COLORS = [GATE_OFF_COLOR, GATE_ON_COLOR]

WIRE_COLORS = [26]

LAMP = 4
LAMP_OFF_COLOR = 12
LAMP_ON_COLOR = 28
LAMP_COLORS = [LAMP_OFF_COLOR, LAMP_ON_COLOR]

SWITCH = 5
SWITCH_OFF_COLOR = 45
SWITCH_ON_COLOR = 46
SWITCH_COLORS = [SWITCH_OFF_COLOR, SWITCH_ON_COLOR]

ALLOW_COLORS_WITHOUT_WIRE = GATE_COLORS + LAMP_COLORS + SWITCH_COLORS
ALLOW_COLORS_SINGLE = LAMP_COLORS + SWITCH_COLORS
ALLOW_COLORS = ALLOW_COLORS_WITHOUT_WIRE + WIRE_COLORS

TICK_PER_SECONDS = 10


class CircuitPlugin(Plugin, ABC):
    circuit_executor: CircuitExecutor | None = None
    elements: dict

    last_update_time: float

    load_mode: bool = False

    def on_create(self):
        self.elements = {}

    def on_destroy(self):
        pass

    def on_update(self):
        if self.circuit_executor:
            current_time = time.time()

            if current_time - self.last_update_time > 1.0 / TICK_PER_SECONDS:
                self.circuit_executor.update()

                self.last_update_time = current_time

    def on_command(self, command: str) -> bool:
        if command == 'load':
            self.load_mode = True
            self.circuit_executor = None
            self.last_update_time = 0.0
            self.elements = {}

            self.game.print_line_to_system_dialog("[Circuit] Please right click the board voxel that you want to load as circuit.", Color(0, 255, 0))

            return True

        return False

    def search_voxels_recursively(self, voxels: list[tuple[int, int, int]], voxel_editor: VoxelEditor, x: int, y: int, z: int, colors: list[int], allow_y_axis: bool = False):
        value = (x, y, z)

        if value in voxels:
            return

        voxel_color = voxel_editor.get_voxel_color_if_exists(x, y, z)

        if voxel_color and voxel_color.index in colors:
            voxels.append(value)

            self.search_voxels_recursively(voxels, voxel_editor, x + 50, y, z, colors, allow_y_axis)
            self.search_voxels_recursively(voxels, voxel_editor, x - 50, y, z, colors, allow_y_axis)
            self.search_voxels_recursively(voxels, voxel_editor, x, y, z + 50, colors, allow_y_axis)
            self.search_voxels_recursively(voxels, voxel_editor, x, y, z - 50, colors, allow_y_axis)

            if allow_y_axis:
                self.search_voxels_recursively(voxels, voxel_editor, x, y + 50, z, colors, allow_y_axis)
                self.search_voxels_recursively(voxels, voxel_editor, x, y - 50, z, colors, allow_y_axis)

    def load_voxels_gate(self, voxel_editor: VoxelEditor, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int, size_x: int, size_y: int, size_z: int, shapes: list) -> dict | None:
        for shape in shapes:
            shape_voxel = shape['shape']
            shape_size_z = len(shape_voxel)
            shape_size_y = len(shape_voxel[0])
            shape_size_x = len(shape_voxel[0][0])

            if shape_size_x == size_x and shape_size_y == size_y and shape_size_z == size_z:
                all_matched = True

                for z_index in range(len(shape_voxel)):
                    shape_voxel_z = shape_voxel[z_index]

                    for y_index in range(len(shape_voxel_z)):
                        shape_voxel_y = shape_voxel_z[y_index]

                        for x_index in range(len(shape_voxel_y)):
                            shape_value = shape_voxel_y[x_index]

                            x = min_x + (50 * x_index)
                            y = min_y + (50 * y_index)
                            z = min_z + (50 * z_index)

                            voxel_color = voxel_editor.get_voxel_color_if_exists(x, y, z)

                            if shape_value:
                                if not (voxel_color and voxel_color.index in GATE_COLORS):
                                    all_matched = False
                            else:
                                if voxel_color:
                                    all_matched = False

                if all_matched:
                    inputs = []

                    shape_inputs = shape['inputs']
                    for shape_input in shape_inputs:
                        inputs.append((
                            min_x + (50 * shape_input[0]),
                            min_y + (50 * shape_input[1]),
                            min_z + (50 * shape_input[2]),
                        ))

                    shape_output = shape['output']
                    output = (
                        min_x + (50 * shape_output[0]),
                        min_y + (50 * shape_output[1]),
                        min_z + (50 * shape_output[2]),
                    )

                    shape_indicator = shape['indicator']
                    indicator = (
                        min_x + (50 * shape_indicator[0]),
                        min_y + (50 * shape_indicator[1]),
                        min_z + (50 * shape_indicator[2]),
                    )

                    return {
                        "inputs": inputs,
                        "outputs": [output],
                        "indicators": [indicator]
                    }

        return None

    def load_voxels_element_recursively(self, elements: dict[tuple[int, int, int], dict], voxel_editor: VoxelEditor, x: int, y: int, z: int) -> tuple[int, int, int] | None:
        voxels: list[tuple[int, int, int]] = []

        voxel_color = voxel_editor.get_voxel_color_if_exists(x, y, z)

        if voxel_color and voxel_color.index in ALLOW_COLORS_SINGLE:
            voxels.append((x, y, z))
        else:
            self.search_voxels_recursively(voxels, voxel_editor, x, y, z, GATE_COLORS, True)

        min_x = 0xffffffff
        max_x = -0xffffffff
        min_y = 0xffffffff
        max_y = -0xffffffff
        min_z = 0xffffffff
        max_z = -0xffffffff

        for voxel_position in voxels:
            x, y, z = voxel_position

            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)

        element_key = (min_x, min_y, min_z)

        if element_key not in elements:
            size_x = int((max_x - min_x) / 50) + 1
            size_y = int((max_y - min_y) / 50) + 1
            size_z = int((max_z - min_z) / 50) + 1

            element_info = None

            if size_x == 1 and size_y == 1 and size_z == 1:
                voxel_color = voxel_editor.get_voxel_color_if_exists(min_x, min_y, min_z)

                if voxel_color and voxel_color.index in LAMP_COLORS:
                    element_info = {
                        "type": LAMP,
                        "inputs": [
                            (min_x - 50, min_y, min_z),
                            (min_x + 50, min_y, min_z),
                            (min_x, min_y, min_z - 50),
                            (min_x, min_y, min_z + 50),
                            (min_x, min_y - 50, min_z),
                            (min_x, min_y + 50, min_z)
                        ],
                        "outputs": [],
                        "indicators": [
                            (min_x, min_y, min_z)
                        ]
                    }
                elif voxel_color and voxel_color.index in SWITCH_COLORS:
                    element_info = {
                        "type": SWITCH,
                        "inputs": [],
                        "outputs": [
                            (min_x - 50, min_y, min_z),
                            (min_x + 50, min_y, min_z),
                            (min_x, min_y, min_z - 50),
                            (min_x, min_y, min_z + 50),
                            (min_x, min_y - 50, min_z),
                            (min_x, min_y + 50, min_z)
                        ],
                        "indicators": [
                            (min_x, min_y, min_z)
                        ]
                    }

            # AND Gate
            if not element_info:
                result = self.load_voxels_gate(voxel_editor, min_x, max_x, min_y, max_y, min_z, max_z, size_x, size_y, size_z, AND_GATE_SHAPES)

                if result:
                    result["type"] = AND_GATE
                    element_info = result

            # OR Gate
            if not element_info:
                result = self.load_voxels_gate(voxel_editor, min_x, max_x, min_y, max_y, min_z, max_z, size_x, size_y, size_z, OR_GATE_SHAPES)

                if result:
                    result["type"] = OR_GATE
                    element_info = result

            # XOR Gate
            if not element_info:
                result = self.load_voxels_gate(voxel_editor, min_x, max_x, min_y, max_y, min_z, max_z, size_x, size_y, size_z, XOR_GATE_SHAPES)

                if result:
                    result["type"] = XOR_GATE
                    element_info = result

            # NOT Gate
            if not element_info:
                result = self.load_voxels_gate(voxel_editor, min_x, max_x, min_y, max_y, min_z, max_z, size_x, size_y, size_z, NOT_GATE_SHAPES)

                if result:
                    result["type"] = NOT_GATE
                    element_info = result

            # DELAY Gate
            if not element_info:
                result = self.load_voxels_gate(voxel_editor, min_x, max_x, min_y, max_y, min_z, max_z, size_x, size_y, size_z, DELAY_GATE_SHAPES)

                if result:
                    result["type"] = DELAY_GATE
                    element_info = result

            if element_info:
                elements[element_key] = element_info

                element_info['output_elements'] = []

                scan_positions = element_info['inputs'] + element_info['outputs']
                scan_offsets = [
                    (50, 0, 0),
                    (-50, 0, 0),
                    (0, 0, 50),
                    (0, 0, -50),
                    (0, 50, 0),
                    (0, -50, 0)
                ]
                inputs_length = len(element_info['inputs'])

                for scan_position_index in range(len(scan_positions)):
                    is_input = scan_position_index < inputs_length
                    scan_position = scan_positions[scan_position_index]

                    x, y, z = scan_position

                    voxels = []
                    self.search_voxels_recursively(voxels, voxel_editor, x, y, z, WIRE_COLORS, True)

                    for voxel_position_index in range(len(voxels)):
                        voxel_position = voxels[voxel_position_index]

                        for scan_offset in scan_offsets:
                            scan_x = voxel_position[0] + scan_offset[0]
                            scan_y = voxel_position[1] + scan_offset[1]
                            scan_z = voxel_position[2] + scan_offset[2]

                            voxel_color = voxel_editor.get_voxel_color_if_exists(scan_x, scan_y, scan_z)

                            if voxel_color and voxel_color.index in ALLOW_COLORS_WITHOUT_WIRE:
                                child_element_key = self.load_voxels_element_recursively(elements, voxel_editor, scan_x, scan_y, scan_z)

                                if not is_input and child_element_key != element_key and voxel_position in elements[child_element_key]["inputs"]:
                                    element_info['output_elements'].append(child_element_key)

                return element_key
        else:
            return element_key

        return None

    def on_voxel_click(self, x: int, y: int, z: int, button_type: MouseButtonType, pressed: bool) -> bool:
        if button_type == MouseButtonType.RIGHT and pressed:
            voxel_editor = VoxelEditor(self.game)

            voxel_color = voxel_editor.get_voxel_color_if_exists(x, y, z)

            if voxel_color and voxel_color is not None:
                if not self.load_mode and voxel_color.index in SWITCH_COLORS:
                    element_key = (x, y, z)

                    if self.elements and element_key in self.elements:
                        element = self.elements[element_key]
                        gate = element['gate']

                        if isinstance(gate, Switch):
                            if gate.get() is None or not gate.get():
                                gate.set(True)
                            else:
                                gate.set(False)

                if self.load_mode and voxel_color.index in ALLOW_COLORS_WITHOUT_WIRE:
                    self.load_mode = False
                    self.game.print_line_to_system_dialog("[Circuit] Loading..", Color(0, 255, 0))

                    elements = {}
                    self.load_voxels_element_recursively(elements, voxel_editor, x, y, z)

                    gates = []
                    gate_map = {}
                    gate_input_count_map = {}

                    self.circuit_executor = CircuitExecutor(self.game)
                    self.last_update_time = time.time()
                    self.elements = elements

                    # Creates
                    for element_key in elements.keys():
                        element = elements[element_key]
                        gate = None

                        def on_gate_update(circuit_executor: CircuitExecutor, inner_gate: Gate, output: bool):
                            inner_element = elements[inner_gate.tag]

                            if isinstance(inner_gate, Switch):
                                inner_x, inner_y, inner_z = inner_element['indicators'][0]

                                if output:
                                    circuit_executor.voxel_editor.set_voxel_color(inner_x, inner_y, inner_z, get_voxel_color(SWITCH_ON_COLOR))
                                else:
                                    circuit_executor.voxel_editor.set_voxel_color(inner_x, inner_y, inner_z, get_voxel_color(SWITCH_OFF_COLOR))

                            if isinstance(inner_gate, Lamp):
                                inner_x, inner_y, inner_z = inner_element['indicators'][0]

                                if output:
                                    circuit_executor.voxel_editor.set_voxel_color(inner_x, inner_y, inner_z, get_voxel_color(LAMP_ON_COLOR))
                                else:
                                    circuit_executor.voxel_editor.set_voxel_color(inner_x, inner_y, inner_z, get_voxel_color(LAMP_OFF_COLOR))

                            if isinstance(inner_gate, AndGate) or isinstance(inner_gate, OrGate) or isinstance(inner_gate, XorGate) or isinstance(inner_gate, NotGate) or isinstance(inner_gate, DelayGate):
                                inner_x, inner_y, inner_z = inner_element['indicators'][0]

                                if output:
                                    circuit_executor.voxel_editor.set_voxel_color(inner_x, inner_y, inner_z, get_voxel_color(GATE_ON_COLOR))
                                else:
                                    circuit_executor.voxel_editor.set_voxel_color(inner_x, inner_y, inner_z, get_voxel_color(GATE_OFF_COLOR))

                        if element['type'] == AND_GATE:
                            gate = AndGate()
                        elif element['type'] == OR_GATE:
                            gate = OrGate()
                        elif element['type'] == XOR_GATE:
                            gate = XorGate()
                        elif element['type'] == NOT_GATE:
                            gate = NotGate()
                        elif element['type'] == DELAY_GATE:
                            gate = DelayGate()
                        elif element['type'] == LAMP:
                            gate = Lamp()
                        elif element['type'] == SWITCH:
                            gate = Switch()

                        if not gate:
                            raise Exception("Unexpected element type.")

                        element['gate'] = gate
                        gate.tag = element_key
                        gate.set_output_callback(on_gate_update)

                        self.circuit_executor.append_gate(gate)

                        gates.append(gate)
                        gate_map[element_key] = gate
                        gate_input_count_map[element_key] = 0

                    # Linking..
                    for gate_key in gate_map.keys():
                        gate = gate_map[gate_key]
                        element = elements[gate_key]

                        output_gates = []

                        for output_element in element['output_elements']:
                            if output_element in gate_map:
                                output_gate = gate_map[output_element]

                                if output_gate.get_input_number() > 0:
                                    input_id = gate_input_count_map[output_element]
                                    gate_input_count_map[output_element] += 1
                                    gate_input_count_map[output_element] %= output_gate.get_input_number()

                                    output_gates.append((output_gate, input_id))
                            else:
                                raise Exception("Not found output element.")

                        gate.set_output_gates(output_gates)

                    voxel_editor.finish()

                    return True

        return False

    def on_mouse_click(self, x: int, y: int, button_type: MouseButtonType, pressed: bool) -> bool:
        out_cursor_object_position = Vector3()
        out_cursor_voxel_position = IntVector3()
        out_cursor_width_depth_height = ctypes.c_uint()
        out_cursor_voxel_size = ctypes.c_float()
        out_cursor_voxel_color_index = ctypes.c_byte()

        if self.game.controller.get_cursor_status(
                out_cursor_object_position,
                out_cursor_voxel_position,
                out_cursor_width_depth_height,
                out_cursor_voxel_size,
                out_cursor_voxel_color_index):
            x = out_cursor_object_position.x - 200 + (out_cursor_voxel_position.x * 50)
            y = out_cursor_object_position.y - 200 + (out_cursor_voxel_position.y * 50)
            z = out_cursor_object_position.z - 200 + (out_cursor_voxel_position.z * 50)

            if self.on_voxel_click(x, y, z, button_type, pressed):
                return True


class CircuitExecutor:
    game: Game
    voxel_editor: VoxelEditor | None

    gates: list[Gate]

    def __init__(self, game: Game):
        self.game = game
        self.voxel_editor = None
        self.gates = []

    def append_gate(self, gate: Gate) -> Gate:
        self.gates.append(gate)

        return gate

    def update(self):
        first_update = self.voxel_editor is None

        self.voxel_editor = VoxelEditor(self.game)

        if first_update:
            for gate in self.gates:
                gate.init(self)

        for gate in self.gates:
            gate.update(self)

        self.voxel_editor.finish()


class Gate(metaclass=ABCMeta):
    inputs: list[int]
    tag: Any

    output: bool = False
    output_callback: Callable[[CircuitExecutor, Gate, bool], None] | None = None,
    output_require_callback: bool = False

    output_gates: list[tuple[Gate, int]]

    def __init__(self):
        self.inputs = [0 for _ in range(self.get_input_number())]
        self.output_gates = []

    def set_output_gates(self, output_gates: list[tuple[Gate, int]]):
        self.output_gates = output_gates

    def set_output_callback(self, output_callback: Callable[[CircuitExecutor, Gate, bool], None] | None):
        self.output_callback = output_callback

    def init(self, circuit_executor: CircuitExecutor):
        if self.output_callback:
            self.output_callback(circuit_executor, self, self.output)

        self.on_init(circuit_executor)

    def update(self, circuit_executor: CircuitExecutor):
        self.on_update(circuit_executor)

        if self.output_require_callback:
            self.output_require_callback = False

            if self.output_callback:
                self.output_callback(circuit_executor, self, self.output)

    @abstractmethod
    def get_input_number(self) -> int:
        pass

    @abstractmethod
    def on_init(self, circuit_executor: CircuitExecutor):
        pass

    @abstractmethod
    def on_update(self, circuit_executor: CircuitExecutor):
        pass

    @abstractmethod
    def on_input(self):
        pass

    def get_input(self, index: int) -> bool:
        return self.inputs[index] != 0

    def out(self, value: bool):
        if self.output != value:
            self.output = value
            self.output_require_callback = True

            for output_gate in self.output_gates:
                if self.output:
                    output_gate[0].inputs[output_gate[1]] += 1
                else:
                    output_gate[0].inputs[output_gate[1]] -= 1

                output_gate[0].on_input()


class Lamp(Gate, ABC):
    def get_input_number(self) -> int:
        return 1

    def on_init(self, circuit_executor: CircuitExecutor):
        pass

    def on_update(self, circuit_executor: CircuitExecutor):
        pass

    def on_input(self):
        self.out(self.get_input(0))


class Switch(Gate, ABC):
    def get_input_number(self) -> int:
        return 0

    def get(self) -> bool:
        return self.output

    def set(self, status: bool):
        self.out(status)

    def on_init(self, circuit_executor: CircuitExecutor):
        pass

    def on_update(self, circuit_executor: CircuitExecutor):
        pass

    def on_input(self):
        pass


class AndGate(Gate, ABC):
    def get_input_number(self) -> int:
        return 2

    def on_init(self, circuit_executor: CircuitExecutor):
        pass

    def on_update(self, circuit_executor: CircuitExecutor):
        pass

    def on_input(self):
        self.out(self.get_input(0) and self.get_input(1))


class OrGate(Gate, ABC):
    def get_input_number(self) -> int:
        return 2

    def on_init(self, circuit_executor: CircuitExecutor):
        pass

    def on_update(self, circuit_executor: CircuitExecutor):
        pass

    def on_input(self):
        self.out(self.get_input(0) or self.get_input(1))


class NotGate(Gate, ABC):
    def get_input_number(self) -> int:
        return 1

    def on_init(self, circuit_executor: CircuitExecutor):
        self.out(not self.get_input(0))

    def on_update(self, circuit_executor: CircuitExecutor):
        pass

    def on_input(self):
        self.out(not self.get_input(0))


class XorGate(Gate, ABC):
    def get_input_number(self) -> int:
        return 2

    def on_init(self, circuit_executor: CircuitExecutor):
        pass

    def on_update(self, circuit_executor: CircuitExecutor):
        pass

    def on_input(self):
        self.out(self.get_input(0) != self.get_input(1))


class DelayGate(Gate, ABC):
    last_status: bool = False

    def get_input_number(self) -> int:
        return 1

    def on_init(self, circuit_executor: CircuitExecutor):
        pass

    def on_update(self, circuit_executor: CircuitExecutor):
        if self.last_status != self.get_input(0):
            self.last_status = self.get_input(0)
        else:
            self.out(self.last_status)

    def on_input(self):
        pass
