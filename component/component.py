import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

class CreateGuides(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "guide.component"
    bl_label = "guide template"

    componentParent = ''#parent guide
    guideInfoDict = {} #tag:[world matrix, parent, guide shape, def/hlp]


classes = [CreateGuides]