from . import component
import os
import bpy
from . import utils
import math
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

def build(side):
    # create armature
    arm = bpy.data.objects['buildArmature']
    gArm = bpy.data.objects['guideArmature']
    boneDict = {
                'tail_1_C' : utils.get_bone_location(gArm, 'tail_1_C'),
                'tail_2_C' : utils.get_bone_location(gArm, 'tail_2_C'),
                'tail_3_C' : utils.get_bone_location(gArm, 'tail_3_C'),
                'tail_4_C' : utils.get_bone_location(gArm, 'tail_4_C'),
                'tail_5_C' : utils.get_bone_location(gArm, 'tail_5_C'),
                'tail_6_C' : utils.get_bone_location(gArm, 'tail_6_C'),
                'tail_7_C' : utils.get_bone_location(gArm, 'tail_7_C'),
                'tail_8_C' : utils.get_bone_location(gArm, 'tail_8_C'),
                'tail_9_C' : utils.get_bone_location(gArm, 'tail_9_C'),
                'tail_10_C' : utils.get_bone_location(gArm, 'tail_10_C'),
                }      
    defBones = []
    conBones = []
    prtBones = []
    mstBone = ''
    fkBones = []
    ikBones = []

    # create edit bones
    # mst bone
    mstBone = utils.addBone(arm, name='mst.tail.C.001', head=boneDict['tail_1_C'][0], tail=boneDict['tail_1_C'][1], roll=0)
    mstBone.length = mstBone.length*.5
    # def bones
    for i, bone in enumerate(boneDict.keys()):
        head = boneDict[bone][0]
        tail = boneDict[bone][1]
        baseName = bone.split('_')[0]
        num = bone.split('_')[1]
        bone = utils.addBone(arm, name='def.{}.C.{}'.format(baseName, num.zfill(3)), head=head, tail=tail, roll=0)
        defBones.append(bone)
    
    for eBone in defBones:
        # con bones
        conBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','con'), scale = 1) 
        conBones.append(conBone)
        # prt bones
        prtBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','prt'), scale = .5) 
        prtBones.append(prtBone)
        # fk controls bones
        baseName = eBone.name.split('.')[1]
        fkBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','ctl').replace(baseName, baseName+'_fk'), scale = .5) 
        fkBones.append(fkBone)
        # ik controls bones
        ikBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','ctl').replace(baseName, baseName+'_ik'), scale = .5) 
        ikBones.append(ikBone)

    # last ik control
    nameindex = str(int(ikBones[-1].name.split('.')[-1]) + 1).zfill(3)
    name = ikBones[-1].name.replace(ikBones[-1].name.split('.')[-1], nameindex)
    head = defBones[-1].tail
    tail = (defBones[-1].tail[0], defBones[-1].tail[1]+(defBones[-1].length)*2, defBones[-1].tail[2])
    ikBone = utils.addBone(arm, name=name, head=head, tail=tail)
    ikBone.length = ikBones[-1].length
    ikBones.append(ikBone)

    # tail controller control
    name = 'ctl.tail_controls.C.001'
    head = ikBones[-1].tail
    tail = (ikBones[-1].tail[0], ikBones[-1].tail[1]+(ikBones[-1].length*2), ikBones[-1].tail[2])
    tailControl = utils.addBone(arm, name=name, head=head, tail=tail)
    tailControl.length = ikBones[-1].length

    #store bone names
    defBoneNames = [bone.name for bone in defBones]
    conBonesNames = [bone.name for bone in conBones]
    prtBonesNames = [bone.name for bone in prtBones]
    mstBoneName = mstBone.name
    tailControlName = tailControl.name
    fkBonesNames = [bone.name for bone in fkBones]
    ikBonesNames = [bone.name for bone in ikBones]

    '''
    # set bone layers
    # def
    sadsasfor bone in defBones:
        dcsdvsbone.layers[utils.boneLayerDict['def']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # conasa
    for bone in conBones:
        bone.layers[utils.boneLayerDict['con']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # prt
    for bone in prtBones:
        bone.layers[utils.boneLayerDict['prt']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # fk + ik controls
    for bone in fkBones + ikBones:
        bone.layers[utils.boneLayerDict['fk']] = True
        bone.layers[utils.boneLayerDict['ik']] = True
        bone.layers[utils.boneLayerDict['god']] = False 
    # tailControl
    tailControl.layers[utils.boneLayerDict['ik']] = True
    tailControl.layers[utils.boneLayerDict['fk']] = True
    tailControl.layers[utils.boneLayerDict['god']] = False
    # mstBone
    mstBone.layers[utils.boneLayerDict['mst']] = True
    mstBone.layers[utils.boneLayerDict['god']] = False
    '''
    # parent bones
    # def
    utils.parent_bone_chain(defBones, connected=True) 
    defBones[0].parent = mstBone
    # con
    utils.parent_bone_chain(conBones, connected=True) 
    defBones[0].parent = mstBone
    # prt
    for i, bone in enumerate(prtBones):
        if i == 0:
            parent = mstBone
        else:
            parent = fkBones[i-1]
        bone.parent = parent
    # fk controls
    for i, bone in enumerate(fkBones):
        bone.parent = prtBones[i]
    # ik controls 
    for bone, parent in zip(ikBones, fkBones):
        bone.parent = parent
    ikBones[-1].parent = fkBones[-1].parent
    # tailControl
    tailControl.parent = mstBone

    bpy.ops.object.mode_set(mode='POSE')
    #constrain bones
    for boneName, target in zip(defBoneNames, conBones):
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = target.name
    # con
    for i, boneName in enumerate(conBonesNames):
        target = ikBonesNames[i]
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = target

        target = ikBonesNames[i+1]
        stretchTo = arm.pose.bones[boneName].constraints.new('STRETCH_TO')
        stretchTo.target = arm
        stretchTo.subtarget = target
    #prt
    dTrack = arm.pose.bones[prtBonesNames[0]].constraints.new('DAMPED_TRACK')
    dTrack.target = arm
    dTrack.subtarget = tailControlName
    for i, boneName in enumerate(prtBonesNames):
        transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM')
        transformCon.name = 'Tail Transform'
        transformCon.target = arm
        transformCon.subtarget = tailControlName
        transformCon.use_motion_extrapolate = True
        transformCon.owner_space = 'LOCAL'  
        transformCon.target_space = 'LOCAL' 
        transformCon.map_from = 'ROTATION'
        transformCon.map_to = 'ROTATION' 
        for attr in [transformCon.from_min_x_rot, 
                    transformCon.from_min_y_rot, 
                    transformCon.from_min_z_rot, 
                    transformCon.to_min_x_rot, 
                    transformCon.to_min_y_rot, 
                    transformCon.to_min_z_rot]:
            attr = math.radians(-1)
        for attr in [transformCon.from_max_x_rot, 
                    transformCon.from_max_y_rot, 
                    transformCon.from_max_z_rot, 
                    transformCon.to_max_x_rot, 
                    transformCon.to_max_y_rot, 
                    transformCon.to_min_z_rot]:
            attr = math.radians(1)
        transformCon.influence = 1/len(prtBonesNames)*(i+1)

    bpy.ops.object.mode_set(mode='OBJECT')
    
class TailGuides(component.CreateGuides):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "guide.tail"
    bl_label = "Hand Guides"

    componentParent = ''#parent guide
    guideInfoDict = {} #tag:[world matrix, parent, guide shape, def/hlp]

    def execute(self, context):
        boneDict = boneDict = utils.get_bone_dict_data(fileName='tail_guide_data.json')
        utils.import_shapes()

        if "guideArmature" not in bpy.data.objects:
            bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            arm = bpy.data.objects['Armature']
            #delete base bone
            arm.edit_bones.remove( arm.edit_bones['Bone'])
            #rename armature
            arm.name = 'guideArmature'
            arm.data.name = 'guideArmature'
            bpy.ops.object.mode_set(mode='OBJECT')

        #add joints with custom property tags
        arm = bpy.data.objects['guideArmature']
        for bone in boneDict.keys():
            name = bone
            head = boneDict[bone][0]
            tail = boneDict[bone][1]
            roll = boneDict[bone][2]
            editBone = utils.addBone(arm, name=name, head=head, tail=tail, roll=roll)
            utils.add_custom_property_to_pose_bone(arm, boneName=editBone.name, propertyName="Component", default='tail' )

        keyList = list(boneDict.keys())
        for i in range(len(keyList)-1):
            parentName = keyList[i]
            childName = keyList[i+1]
            arm.data.edit_bones[childName].parent = arm.data.edit_bones[parentName]

        # set bone shapes
        bpy.ops.object.mode_set(mode='POSE')
        custom_shape = bpy.data.objects['guide.shape']
        for bone in keyList:
            arm.pose.bones[bone].custom_shape = custom_shape
        # add necessary constraints
        # assign pose bone group
        bpy.ops.object.mode_set(mode='OBJECT')
        return {"FINISHED"}

class BUILD_OT_Tail(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "build.tail"
    bl_label = "Tail Build"

    def execute(self, context):
        build('C')

        return {"FINISHED"}

classes = [TailGuides, BUILD_OT_Tail]