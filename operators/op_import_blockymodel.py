import math
import mathutils
import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
import json
import copy
from .. import hyobjects
from .. import hyobject_edit


class HytaleDeserializer:
    class _Node:
        def __init__(self, node, parent):
            self.node = node
            self.parent = parent
            self.obj = None

    node_tree = {}

    def _pre_parse_nodes(self, node, parent):
        self.node_tree[node["id"]] = HytaleDeserializer._Node(node, parent)

        if "children" in node:
            for child in node["children"]:
                self._pre_parse_nodes(child, node)

    def _split_groups(self):
        to_add = {}
        id = 0
        for n in self.node_tree:
            node = self.node_tree[n]
            if node.node["shape"]["type"] != "none":
                if "children" not in node.node:
                    continue
                while str(id) in self.node_tree or str(id) in to_add:
                    id = id + 1
                new_parent = copy.deepcopy(node.node)
                new_parent["id"] = id
                for c in node.node["children"]:
                    self.node_tree[c["id"]].parent = new_parent
                node.node.pop("children")
                new_parent["children"].insert(0, node.node)
                new_parent["name"] = new_parent["name"] + "_G"
                new_parent["shape"]["type"] = "none"
                to_add[str(id)] = HytaleDeserializer._Node(new_parent, node.parent)
                node.parent = new_parent
                node.node["position"]["x"] = 0.0
                node.node["position"]["y"] = 0.0
                node.node["position"]["z"] = 0.0
                node.node["orientation"]["x"] = 0.0
                node.node["orientation"]["y"] = 0.0
                node.node["orientation"]["z"] = 0.0
                node.node["orientation"]["w"] = 1.0
        for a in to_add:
            self.node_tree[a] = to_add[a]

    def _gen_objects(self):
        for n in self.node_tree:
            node = self.node_tree[n]
            offset = mathutils.Vector(
                (
                    -node.node["shape"]["offset"]["x"] / 10.0,
                    node.node["shape"]["offset"]["z"] / 10.0,
                    node.node["shape"]["offset"]["y"] / 10.0,
                )
            )
            rotation = mathutils.Quaternion(
                (
                    node.node["orientation"]["w"],
                    -node.node["orientation"]["x"],
                    node.node["orientation"]["z"],
                    node.node["orientation"]["y"],
                )
            )
            match node.node["shape"]["type"]:
                case "none":
                    if node.node["name"].endswith("-Attachement"):
                        node.obj = hyobjects.create_attachement()
                    else:
                        node.obj = hyobjects.create_group()

                    pass
                case "box":
                    node.obj = hyobjects.create_hybox()

                    node.obj.hymodler_size[0] = node.node["shape"]["settings"]["size"][
                        "x"
                    ]
                    node.obj.hymodler_size[2] = node.node["shape"]["settings"]["size"][
                        "y"
                    ]
                    node.obj.hymodler_size[1] = node.node["shape"]["settings"]["size"][
                        "z"
                    ]

                    hyobject_edit.set_origin_to_geometry_center(node.obj)
                    hyobject_edit.add_offset_to_hyobject(node.obj, -offset)

                    pass
                case "quad":
                    node.obj = hyobjects.create_hyquad()
                    node.obj.hymodler_size[0] = node.node["shape"]["settings"]["size"][
                        "x"
                    ]
                    node.obj.hymodler_size[1] = node.node["shape"]["settings"]["size"][
                        "y"
                    ]
                    prot = hyobject_edit.get_initial_quad_rot(
                        node.node["shape"]["settings"]["normal"]
                    )

                    rotation = rotation @ prot
                    offset.rotate(prot)

                    hyobject_edit.set_origin_to_geometry_center(node.obj)
                    hyobject_edit.add_offset_to_hyobject(node.obj, -offset)
                    pass
            node.obj.name = node.node["name"]
            node.obj.hymodler_bbname = node.node["name"]
            node.obj.location.x = -node.node["position"]["x"] / 10.0
            node.obj.location.y = node.node["position"]["z"] / 10.0
            node.obj.location.z = node.node["position"]["y"] / 10.0

            node.obj.rotation_quaternion = rotation

    def _parent_objects(self):
        for n in self.node_tree:
            node = self.node_tree[n]
            if node.parent is not None:
                node.obj.parent = self.node_tree[str(node.parent["id"])].obj
        pass
        pass

    def load_nodes(self, nodes):
        for node in nodes:
            self._pre_parse_nodes(node, None)

        self._split_groups()
        self._gen_objects()
        self._parent_objects()

        # self.debug_output()
        pass

    def debug_output(self):
        with open("/home/flo_12344/Documents/hytale-modding/debug/debug.txt", "w") as f:
            for n in self.node_tree:
                f.write(str(n) + " : {" + self.node_tree[n].node["name"])
                if self.node_tree[n].parent != None:
                    f.write(", " + self.node_tree[n].parent["name"])
                f.write("} " + self.node_tree[n].node["shape"]["type"] + "\n")
            pass


class OP_Import_Blockymodel(bpy.types.Operator, ImportHelper):
    bl_idname = "hymodler.import_blockymodel"
    bl_label = "import_Blockymodel"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty(default="*.blockymodel", options={"HIDDEN"})
    filename_ext = ".blockymodel"
    hymodler_selection_only: bpy.props.BoolProperty(
        name="Selection Only", description="", default=False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        deserializer = HytaleDeserializer()
        with open(self.filepath, "r") as file:
            j = json.load(file)

        if "nodes" in j:
            deserializer.load_nodes(j["nodes"])
        return {"FINISHED"}


def add_to_topbar_mt_file_import(self, context):
    layout = self.layout
    op = layout.operator(
        "hymodler.import_blockymodel",
        text="Blockymodel",
        icon_value=0,
        emboss=True,
        depress=False,
    )
    op.sna_selection_only = False


def register():
    bpy.utils.register_class(OP_Import_Blockymodel)
    bpy.types.TOPBAR_MT_file_import.append(add_to_topbar_mt_file_import)


def unregister():
    bpy.utils.unregister_class(OP_Import_Blockymodel)
    bpy.types.TOPBAR_MT_file_import.remove(add_to_topbar_mt_file_import)
