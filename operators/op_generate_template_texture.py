import bpy
import mathutils
import bmesh

import math


class OP_Generate_Template_Texture(bpy.types.Operator):
    bl_idname = "hymodler.generate_template_texture"
    bl_label = "generate_template_texture"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set("")
        return not False

    def execute(self, context):
        meshes = bpy.context.view_layer.objects.selected

        def get_image(ref):
            if isinstance(ref, str):
                if ref in bpy.data.images:
                    return bpy.data.images[ref]
            else:
                return ref

        texture_size = bpy.context.scene.hymodler_texturesize
        img = get_image("template_texture")
        if img == None:
            img = bpy.data.images.new(
                "template_texture",
                width=texture_size[0],
                height=texture_size[1],
                alpha=True,
            )
        elif img.size[0] != texture_size[0] or img.size[1] != texture_size[1]:
            img.resize((texture_size[0], texture_size[1]))
        pixels = list(img.pixels)
        for i in range(0, len(pixels), 4):
            pixels[i + 3] = 0.0
        img.pixels = pixels
        img.update()
        for mesh in meshes:
            bm = bmesh.new()
            bm.from_mesh(mesh.data)
            uv_lay = bm.loops.layers.uv.verify()
            bbs = []

            def get_all_bb(face):
                nv = (float("inf"), float("inf"))
                xv = (0.0, 0.0)
                for loop in face.loops:
                    uv = loop[uv_lay].uv
                    nv = (min(nv[0], uv[0]), min(nv[1], uv[1]))
                    xv = (max(xv[0], uv[0]), max(xv[1], uv[1]))
                bbs.append((nv, xv, face.normal))

            for face in bm.faces:
                get_all_bb(face)

            def draw_box_with_outline_uv(
                img,
                uv_x,
                uv_y,
                uv_x_end,
                uv_y_end,
                fill_color=(1, 1, 1, 1),
                outline_color=(0.5, 0.5, 0.5, 1),
                outline_thickness=1,
            ):
                img_w, img_h = img.size
                pixels = list(img.pixels)
                # Convert UV → pixel coordinates
                x = int(uv_x * img_w)
                y = int(uv_y * img_h)
                end_x = int(uv_x_end * img_w)
                end_y = int(uv_y_end * img_h)
                width_px = end_x - x
                height_px = end_y - y

                def set_pixel(px, py, color):
                    if 0 <= px < img_w and 0 <= py < img_h:
                        i = (py * img_w + px) * 4
                        pixels[i : i + 4] = color

                for py in range(y, y + height_px):
                    for px in range(x, x + width_px):
                        is_outline = (
                            px < x + outline_thickness
                            or px >= x + width_px - outline_thickness
                            or py < y + outline_thickness
                            or py >= y + height_px - outline_thickness
                        )
                        if is_outline:
                            set_pixel(px, py, outline_color)
                        else:
                            set_pixel(px, py, fill_color)
                img.pixels = pixels
                img.update()

            def get_color(normal):
                mn = 0.5
                if normal.x > mn:
                    return (0.48, 1.0, 0.64, 1), (0.26, 0.9, 0.55, 1)
                elif normal.x < -mn:
                    return (1.0, 0.65, 0.64, 1), (0.95, 0.52, 0.52, 1)
                elif normal.z > mn:
                    return (0.93, 0.97, 0.99, 1), (0.71, 0.83, 0.88, 1)
                elif normal.z < -mn:
                    return (0.43, 0.47, 0.55, 1), (0.33, 0.38, 0.45, 1)
                elif normal.y > mn:
                    return (0.48, 0.83, 1.0, 1), (0.36, 0.74, 0.96, 1)
                elif normal.y < -mn:
                    return (1.0, 0.97, 0.6, 1), (0.97, 0.87, 0.45, 1)

            for b in bbs:
                cols = get_color(b[2])
                draw_box_with_outline_uv(
                    img, b[0][0], b[0][1], b[1][0], b[1][1], cols[0], cols[1]
                )
            bm.free()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    bpy.utils.register_class(OP_Generate_Template_Texture)


def unregister():
    bpy.utils.unregister_class(OP_Generate_Template_Texture)
