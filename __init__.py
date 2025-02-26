bl_info = {
    "name": "gRig",
    "author": "Colin Okoduwa",
    "location": "3D View > Sidebar",
    "version": (0, 0, 0),
    "blender": (3, 0, 0),
    "description": "Rigging system for Gladiotron",
    "category": "Development"
    }

import bpy
from importlib import reload 
from . import ui 
from .component import component, foot, hand, spine, tail, biped, utils, limb, leg, build


classes = []
for cls in ui.classes + component.classes + foot.classes + hand.classes + limb.classes + spine.classes + tail.classes + utils.classes + biped.classes + leg.classes + build.classes:
    classes.append(cls)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()