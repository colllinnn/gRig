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

def build():
    # create armature
    arm = bpy.data.objects['buildArmature']
    gArm = bpy.data.objects['guideArmature']
    boneDict = {
    'pelvis_C_1' : utils.get_bone_location(gArm, 'pelvis_C_1'),
    'spine_C_1' : utils.get_bone_location(gArm, 'spine_C_1'),
    'spine_C_2' : utils.get_bone_location(gArm, 'spine_C_2'),
    'spine_C_3' : utils.get_bone_location(gArm, 'spine_C_3'),
    'neck_C_1' : utils.get_bone_location(gArm, 'neck_C_1'),
    'neck_C_2' : utils.get_bone_location(gArm, 'neck_C_2'),
    'head_C_1' : utils.get_bone_location(gArm, 'head_C_1')
    }

    defBones = []
    conBones = []
    fkReverseBones = []
    hlpBones = []
    hlpReverseBones = []

    mstBone = ''
    ikmBones = []
    prtBones = []
    hlpIkStretchBones = []
    tweakParentBones = []
    ikPrtBone = ''
    tweaks = []
    fkBones = []
    fkSubBones = []
    ikBones = []
    ikSubBones = []
    poleVector = []
    poleVectorSub = []
    armControl = ''

    # create def joints
    for i, bone in enumerate(boneDict.keys()):
        if '_' in bone:
            boneName = bone.split('_')[0] 
            boneNum = bone.split('_')[-1]
            boneName = 'def.{}.C.00{}'.format(boneName, boneNum)
        else:
            boneName = 'def.{}.C.001'.format(bone)
        head = boneDict[bone][0]
        tail = boneDict[bone][1]
        bone = utils.addBone(arm, name=boneName, head=head, tail=tail, roll=0)
        defBones.append(bone)

    for eBone in defBones:
        # con bones
        conBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'con'), scale = 1) 
        conBones.append(conBone)
        # hlp bones
        hlpBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'hlp'), scale = .8) 
        hlpBones.append(hlpBone)
        #fk bones
        boneName = bone.name.split('.')[1]
        fkBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'ctl').replace(boneName, boneName+'_fk'), scale = .5) 
        fkBones.append(fkBone)
        if 'spine' in eBone.name or 'pelvis' in eBone.name:
            # hlp reverse bones
            boneName = eBone.name.split('.')[1] 
            hlpReverseBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'hlp').replace(boneName, boneName+'_reverse'), scale = .6) 
            hlpReverseBones.append(hlpReverseBone)
            # fk reverse bones
            fkReverseBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'ctl').replace(boneName, boneName+'_reverse_fk'), scale = .5) 
            fkReverseBones.append(fkReverseBone)
        if 'spine' in eBone.name:
            boneName = eBone.name.split('.')[1]
            ikBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'ctl').replace(boneName, boneName+'_ik'), scale = .5) 
            ikBones.append(ikBone)
    # mid ik parent
    avgHead = ((boneDict['spine_C_1'][0][0]+boneDict['spine_C_3'][0][0])/2, (boneDict['spine_C_1'][0][1]+boneDict['spine_C_3'][0][1])/2, (boneDict['spine_C_1'][0][2]+boneDict['spine_C_3'][0][2])/2)
    avgTail = ((boneDict['spine_C_1'][1][0]+boneDict['spine_C_3'][1][0])/2, (boneDict['spine_C_1'][1][1]+boneDict['spine_C_3'][1][1])/2, (boneDict['spine_C_1'][1][2]+boneDict['spine_C_3'][1][2])/2)
    ikPrt = utils.addBone(arm, name='prt.spine_ik.C.002', head=avgHead, tail=avgTail, roll=0)
    # neck prt
    for bone in defBones:
        if 'neck' in bone.name:
            neckPrt = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'prt'), scale = .6)
            break
        else:
            continue
    # spine controls
    head = boneDict['spine_C_2'][0]
    tail = boneDict['spine_C_2'][1]
    spineControl = utils.addBone(arm, name='ctl.spine_control.C.001', head=head, tail=tail, roll=math.pi)
    #root
    root = utils.duplicate_bone(arm, defBones[1], 'ctl.root.C.001', scale = 1)
    rootSub = utils.duplicate_bone(arm, defBones[1], 'ctl.root_sub.C.001', scale = 1)
    # mstBone
    mstBone = utils.duplicate_bone(arm, defBones[1], defBones[1].name.replace('def', 'mst'), scale = 1) 

    #store bone names
    defBoneNames = [bone.name for bone in defBones]
    conBonesNames = [bone.name for bone in conBones]
    fkReverseBoneNames = [bone.name for bone in fkReverseBones]
    hlpBoneNames = [bone.name for bone in hlpBones]
    hlpReverseBoneNames = [bone.name for bone in hlpReverseBones]
    mstBoneName = mstBone.name
    fkBonesNames = [bone.name for bone in fkBones]
    ikBonesNames = [bone.name for bone in ikBones]
    spineControlName = spineControl.name
    ikPrtName = ikPrt.name

    # set bone layers
    # def
    for bone in defBones:
        bone.layers[utils.boneLayerDict['def']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # con
    for bone in conBones:
        bone.layers[utils.boneLayerDict['con']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # neckPrt
    for bone in [neckPrt] + [ikPrt]:
        bone.layers[utils.boneLayerDict['prt']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # hlp reverse
    for bone in hlpReverseBones:
        bone.layers[utils.boneLayerDict['hlp']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # hlp
    for bone in hlpBones:
        bone.layers[utils.boneLayerDict['hlp']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # fk controls
    for bone in fkBones + fkReverseBones + [root] + [rootSub]:
        bone.layers[utils.boneLayerDict['fk']] = True
        bone.layers[utils.boneLayerDict['god']] = False 
    # ik controls
    for bone in ikBones + [root] + [rootSub]:
        bone.layers[utils.boneLayerDict['ik']] = True
        bone.layers[utils.boneLayerDict['god']] = False 
    # tailControl
    spineControl.layers[utils.boneLayerDict['fk']] = True
    spineControl.layers[utils.boneLayerDict['ik']] = True
    spineControl.layers[utils.boneLayerDict['god']] = False
    # mstBone
    mstBone.layers[utils.boneLayerDict['mst']] = True
    mstBone.layers[utils.boneLayerDict['god']] = False

    # parent bones
    # def
    utils.parent_bone_chain(defBones[1:], connected=True) 
    defBones[0].parent = mstBone
    defBones[1].parent = mstBone
    # con
    utils.parent_bone_chain(conBones[1:], connected=False) 
    conBones[0].parent = mstBone
    conBones[1].parent = mstBone
    # hlp
    utils.parent_bone_chain(hlpBones[1:], connected=False) 
    hlpBones[0].parent = mstBone
    hlpBones[1].parent = mstBone
    # ikPrt
    ikPrt.parent = hlpReverseBones[2]
    spineControl.parent = hlpReverseBones[2]
    # hlpReverseBones
    utils.parent_bone_chain(hlpReverseBones[1:], connected=False) 
    hlpReverseBones[0].parent = mstBone
    hlpReverseBones[1].parent = mstBone
    # fkBones
    utils.parent_bone_chain(fkBones[1:], connected=False) 
    fkBones[0].parent = rootSub
    fkBones[1].parent = rootSub
    # ikBones
    for i, bone in enumerate(ikBones):
        if i != 1:
            bone.parent = hlpReverseBones[i+1]
        else:
            bone.parent = ikPrt
    # root
    rootSub.parent = root
    root.parent = mstBone
    # fkReverseBones
    utils.parent_bone_chain(fkReverseBones[::-1], connected=False) 
    fkReverseBones[-1].parent = rootSub

    bpy.ops.object.mode_set(mode='POSE')
    # custom properties'
    utils.add_custom_property_to_pose_bone(arm, boneName=spineControlName, propertyName="reverse_spine", default=0.0, min=0.0, max=1.0 )
    utils.add_custom_property_to_pose_bone(arm, boneName=spineControlName, propertyName="volume_preservation", default=1.0, min=0.0, max=1.0 )


    
    #constrain bones
    # def
    for boneName, target in zip(defBoneNames, conBonesNames):
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = target
    # con
    for i, boneName in enumerate(conBonesNames):
        pBone =  arm.pose.bones[boneName]
        if 'spine' in boneName:
            baseName = boneName.split('.')[1]
            target = boneName.replace('con', 'ctl').replace(baseName, baseName+'_ik')
        else:
            target = hlpBoneNames[i]
        copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = target
        if boneName != conBonesNames[-1]:
            if i != 0:
                target = hlpBoneNames[i+1]
                stretchTo = pBone.constraints.new('STRETCH_TO')
                stretchTo.target = arm
                stretchTo.subtarget = target
                drv = utils.add_driver(pBone.constraints['{}'.format(stretchTo.name)], 'bulge', func = 'var')
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.spine_controls.C.001"]["volume_preservation"]')
    # hlp
    for i, boneName in enumerate(hlpBoneNames):
        if 'spine' in boneName:
            baseName = boneName.split('.')[1]
            subtarget = boneName.replace('hlp', 'ctl').replace(baseName, baseName+'_ik')
        else:
            subtarget = fkBonesNames[i]
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = subtarget
    # hlpReverseBones
    for i, boneName in enumerate(hlpReverseBoneNames):
        pBone =  arm.pose.bones[boneName]
        target = fkBonesNames[i]
        # fk transform constraint
        copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
        copyTrans.name = 'Copy Transforms FK'
        copyTrans.target = arm
        copyTrans.subtarget = target
        # reverse fk transform constraint
        target = fkReverseBoneNames[i]
        copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
        copyTrans.name = 'Copy Transforms Reverse FK'
        copyTrans.target = arm
        copyTrans.subtarget = target
        # reverse fk influence driver 
        drv = utils.add_driver(pBone.constraints['{}'.format(copyTrans.name)], 'influence', func = 'var')
        utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.spine_controls.C.001"]["reverse_spine"]')
    '''
    # neckPrt
    copyTrans = arm.pose.bones[neckPrt.name].constraints.new('COPY_TRANSFORMS')
    copyTrans.target = arm
    copyTrans.subtarget = target
    '''
    # ikPrt
    for subtarget in [ikBonesNames[0], ikBonesNames[2]]:
        boneName = ikPrtName
        copyRot = arm.pose.bones[boneName].constraints.new('COPY_ROTATION')
        if i == ikBonesNames[0]:
            copyRot.name = 'Copy Rotation Bottom'
        else:
            copyRot.name = 'Copy Rotation Top'
            copyRot.influence = .5
        copyRot.target = arm
        copyRot.subtarget = subtarget        

        transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM') #rot y transformation
        if i == ikBonesNames[0]:
            transformCon.name = 'Bottom IK Translate Transformation'
        else:
            transformCon.name = 'Top IK Translate Transformation'
        transformCon.target = arm
        transformCon.subtarget = subtarget
        transformCon.use_motion_extrapolate = True
        transformCon.owner_space = 'LOCAL'  
        transformCon.target_space = 'LOCAL' 
        transformCon.map_from = 'ROTATION'
        transformCon.map_to = 'ROTATION' 
        for attr in [transformCon.from_min_x, 
                    transformCon.from_min_y, 
                    transformCon.from_min_z]:
                    attr = math.radians(-1)
        for attr in [transformCon.from_max_x, 
                    transformCon.from_max_y, 
                    transformCon.from_max_z]:
                    attr = math.radians(1)
        for attr in [transformCon.to_min_x, 
                    transformCon.to_min_y, 
                    transformCon.to_min_z]:
                    attr = math.radians(-0.5)
        for attr in [transformCon.to_max_x, 
                    transformCon.to_max_y, 
                    transformCon.to_min_z]:
                    attr = math.radians(0.5)

    bpy.ops.object.mode_set(mode='OBJECT')
    
class SpineGuides(component.CreateGuides):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "guide.spine"
    bl_label = "Limb Guides"

    componentParent = ''#parent guide
    guideInfoDict = {} #tag:[world matrix, parent, guide shape, def/hlp]

    def execute(self, context):
        boneDict = boneDict = utils.get_bone_dict_data(fileName='spine_guide_data.json') 
        utils.import_shapes()

        if "guideArmature" not in bpy.data.objects:
            bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            arm = bpy.data.objects['Armature']
            #delete base bone
            arm.data.edit_bones.remove( arm.data.edit_bones['Bone'])
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
            utils.add_custom_property_to_pose_bone(arm, boneName=editBone.name, propertyName="Component", default='spine' )

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

class BUILD_OT_Spine(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "build.spine"
    bl_label = "Limb Build"

    def execute(self, context):
        build()

        return {"FINISHED"}

classes = [SpineGuides, BUILD_OT_Spine]