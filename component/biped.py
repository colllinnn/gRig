import bpy
import os
from . import utils
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from . import utils, component, limb, spine, foot, hand

class Biped_Guides( component.CreateGuides):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "guide.biped"
    bl_label = "Biped Guides"
    
    def execute(self, context):
        # append all objects ending with '.shape'
        utils.import_shapes()
        #hide guide
        bpy.data.objects['guide.shape'].hide_viewport = True
        
        # build
        bpy.ops.guide.limb()
        bpy.ops.guide.spine()
        bpy.ops.guide.foot()
        bpy.ops.guide.hand()
        bpy.ops.guide.leg()
        return {"FINISHED"}

class BUILD_OT_Biped(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "build.biped"
    bl_label = "Biped Build"

    def execute(self, context):
        arm = bpy.data.objects['guideArmature']
        componentList = [arm.pose.bones[bone.name]['Component'] for bone in bpy.context.object.data.bones]
        if 'limb' in component:
            bpy.ops.build.limb()
        if 'spine' in component:
            bpy.ops.build.spine()
        if 'foot' in component:
            bpy.ops.build.foot()
        if 'hand' in component:
            bpy.ops.build.hand()
        if 'leg' in component:
            bpy.ops.build.leg()
        return {"FINISHED"}

classes = [Biped_Guides, BUILD_OT_Biped]