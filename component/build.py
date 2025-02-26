import bpy
import os
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from . import utils, component, limb, spine, foot, hand

class Build( component.CreateGuides):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "build.build"
    bl_label = "Biped Guides"

    def execute(self, context):
        # set build armature as active object 
        utils.create_build_rig()
        guideArm =  bpy.data.objects['guideArmature']
        arm = bpy.data.objects['buildArmature']
        #bpy.context.view_layer.objects.active = arm
        #bpy.ops.object.mode_set(mode='POSE')    
        # check if module guides are in scene and build
        propList = [guideArm.pose.bones[bone.name]['Component'] for bone in guideArm.pose.bones]
        for bone in arm.pose.bones:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        if 'spine' in propList:
            bpy.ops.build.spine()
            print('built spine!')
        if 'foot' in propList:
            bpy.ops.build.foot()
            print('built foot!')
        if 'hand' in propList:
            bpy.ops.build.hand()
            print('built hand!')
        if 'limb' in propList:
            bpy.ops.build.limb()
            print('built limb!')
        if 'tail' in propList:
            bpy.ops.build.tail()
            print('built tail!')
        if 'leg' in propList:
            bpy.ops.build.leg()
            print('built leg!')
    
        # apply custom shapes
        utils.apply_bone_custom_shapes(fileName='custom_shapes.json')
        
        # create bone groups
        boneLayerDict = {
                    0:('deform','THEME04'),
                    1:('constraint','THEME01'),
                    2:('helper_twist','THEME09'),
                    3:('helper','THEME09'),
                    4:('ik_mechanic','THEME15'),
                    5:('parent','THEME09'),
                    6:('helper_ik','THEME09'),
                    7:('control_left', 'THEME01'),
                    8:('control_right', 'THEME04'),
                    9:('control_centre', 'THEME09'),
                    10:('master', 'THEME08')
                    }   
        for i, key in enumerate(boneLayerDict.keys()):
            grpName = boneLayerDict[key][0]
            colorSet = boneLayerDict[key][1]
            boneGrp = arm.pose.bone_groups.new(name = grpName)
            boneGrp.color_set = colorSet
            #bpy.ops.pose.select_all(action='DESELECT')

        for bone in bpy.data.objects['buildArmature'].pose.bones:
            if 'def.' in bone.name:
                i = 0
            elif 'con.' in bone.name:
                i = 1
            elif '_twist' in bone.name:
                i = 2
            elif 'hlp.' in bone.name:
                i = 3
            elif 'ikm.' in bone.name:
                i = 4
            elif 'prt.' in bone.name:
                i = 5
            elif 'hlp.' in bone.name and '_ik' in bone.name:
                i = 6
            elif '.L.' in bone.name and bone.name.startswith('ctl'):
                i = 7
            elif '.R.' in bone.name and bone.name.startswith('ctl'):
                i = 8
            elif '.C.' in bone.name and bone.name.startswith('ctl'):
                i = 9
            elif 'mst.' in bone.name:
                i = 10 
            if i != None:
                arm.pose.bones[bone.name].bone_group_index = i

        # set rotation order
        for pBone in arm.pose.bones:
            pBone.rotation_mode = "XYZ"
        # set deform 
        bones = bpy.data.armatures[arm.name].bones
        for bone in bones:
            if not bone.name.startswith('def.'):
                bone.use_deform = False

        return {"FINISHED"}

classes = [Build]