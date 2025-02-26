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

class gRig_Panel(Panel):
    """Creates a Panel"""
    bl_idname = "GRIG_PT_main"
    bl_label = "gRIG"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "gRig"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # 
        layout = self.layout
        box = layout.box()
        box.label(text="Guides")
        #add buttons
        box.operator("guide.limb", text="Limb Guides")
        box.operator("guide.spine", text="Spine Guides")
        #box.operator("guide.clavicle", text="Guide")
        box.operator("guide.tail", text="Tail Guides")
        box.operator("guide.hand", text="Hand Guides")
        box.operator("guide.leg", text="Leg Guides")
        box.operator("guide.foot", text="Foot Guides")
        box.operator("guide.biped", text="Biped Guides")
        #add scale slider
        #add generate buton

        # mirror box
        box.label(text="Mirror Guides")
        box.operator("utils.mirror", text="Mirror Guides")

        # build box
        box.label(text="Build", icon='OUTLINER_OB_ARMATURE')
        box.operator("build.build", text="Build")

        '''
        box.operator("build.limb", text="Limb Build")
        box.operator("build.spine", text="Spine Build")
        #box.operator("guide.clavicle", text="Guide")
        box.operator("build.tail", text="Tail Build")
        box.operator("build.hand", text="Hand Build")
        box.operator("build.foot", text="Foot Build")
        '''
        #will not be accessible unless a root is  selected 
        #build operator 
        
        #box for the exporting and exporting of guides
        #mirror button

classes = [gRig_Panel]