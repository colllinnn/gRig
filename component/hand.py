from . import component
import os
import bpy
from . import utils
from math import radians
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

 # name, head, tail, roll
    
def build(side):
    # create armature
    arm = bpy.data.objects['buildArmature']
    gArm = bpy.data.objects['guideArmature']
    indexDict = {
                'index_finger_{}_1'.format(side) : utils.get_bone_location(gArm, 'index_finger_{}_1'.format(side)),
                'index_finger_{}_2'.format(side) : utils.get_bone_location(gArm, 'index_finger_{}_2'.format(side)),
                'index_finger_{}_3'.format(side) : utils.get_bone_location(gArm, 'index_finger_{}_3'.format(side)), 
                'index_finger_{}_4'.format(side) : utils.get_bone_location(gArm, 'index_finger_{}_4'.format(side))
                }

    middleDict = {
                'middle_finger_{}_1'.format(side) : utils.get_bone_location(gArm, 'middle_finger_{}_1'.format(side)),
                'middle_finger_{}_2'.format(side) : utils.get_bone_location(gArm, 'middle_finger_{}_2'.format(side)),
                'middle_finger_{}_3'.format(side) : utils.get_bone_location(gArm, 'middle_finger_{}_3'.format(side)), 
                'middle_finger_{}_4'.format(side) : utils.get_bone_location(gArm, 'middle_finger_{}_4'.format(side))
                }
    ringDict = {
                'ring_finger_{}_1'.format(side) : utils.get_bone_location(gArm, 'ring_finger_{}_1'.format(side)),
                'ring_finger_{}_2'.format(side) : utils.get_bone_location(gArm, 'ring_finger_{}_2'.format(side)),
                'ring_finger_{}_3'.format(side) : utils.get_bone_location(gArm, 'ring_finger_{}_3'.format(side)), 
                'ring_finger_{}_4'.format(side) : utils.get_bone_location(gArm, 'ring_finger_{}_4'.format(side))
                }
    pinkyDict = {
                'pinky_finger_{}_1'.format(side) : utils.get_bone_location(gArm, 'pinky_finger_{}_1'.format(side)),
                'pinky_finger_{}_2'.format(side) : utils.get_bone_location(gArm, 'pinky_finger_{}_2'.format(side)),
                'pinky_finger_{}_3'.format(side) : utils.get_bone_location(gArm, 'pinky_finger_{}_3'.format(side)), 
                'pinky_finger_{}_4'.format(side) : utils.get_bone_location(gArm, 'pinky_finger_{}_4'.format(side))
                }
    
    thumbDict = {
                'thumb_{}_1'.format(side) : utils.get_bone_location(gArm, 'thumb_{}_1'.format(side)),
                'thumb_{}_2'.format(side) : utils.get_bone_location(gArm, 'thumb_{}_2'.format(side)),
                'thumb_{}_3'.format(side) : utils.get_bone_location(gArm, 'thumb_{}_3'.format(side))
                }

    handControlDict = {
                'hand_control_{}'.format(side) : utils.get_bone_location(gArm, 'hand_control_{}'.format(side))
                }

    # create bones

    # master bone
    mstBone = utils.addBone(arm, name='mst.hand.{}.001'.format(side), head=middleDict['middle_finger_{}_1'.format(side)][0], tail=middleDict['middle_finger_{}_1'.format(side)][1], roll=0)
    mstBone.length = mstBone.length*.5
    # hand control
    for bone in handControlDict.keys():
        head = handControlDict[bone][0]
        tail = handControlDict[bone][1]
        roll = handControlDict[bone][2]
        handCtl = utils.addBone(arm, name='ctl.hand_control.{}.001'.format(side), head=head, tail=tail, roll=roll)
    # finger bend controls
    bendCtls = []
    for bone in middleDict:
        head = middleDict[bone][0]
        tail = middleDict[bone][1]
        roll = middleDict[bone][2]
        baseName = bone[:-4]
        num = bone.split('_')[-1]
        bendCtl = utils.addBone(arm, name='ctl.bend.{}.{}'.format(side, num.zfill(3)), head=head, tail=tail, roll=roll)
        bendCtls.append(bendCtl)
    # bone layers
    # hand control
    handCtl.layers[utils.boneLayerDict['fk']] = True
    handCtl.layers[utils.boneLayerDict['ik']] = True
    handCtl.layers[utils.boneLayerDict['god']] = False
    # mstBone
    mstBone.layers[utils.boneLayerDict['mst']] = True
    mstBone.layers[utils.boneLayerDict['god']] = False
    # bend controls
    for bone in bendCtls:
        bone.layers[utils.boneLayerDict['fk']] = True
        bone.layers[utils.boneLayerDict['ik']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    
    # parent bones
    # finger bend controls
    utils.parent_bone_chain(bendCtls, connected=True)
    bendCtls[0].parent = mstBone
    # hand control
    handCtl.parent = mstBone

    #store bone names
    mstBoneName = mstBone.name
    handCtlName = handCtl.name

    # def bones
    for dict in [indexDict, middleDict, ringDict, pinkyDict, thumbDict]:
        bpy.ops.object.mode_set(mode='EDIT')
        mstBone = arm.data.edit_bones[mstBoneName]
        defBones = []
        conBones = []
        prtBones = []   
        fkBones = []
        bendCtls = []
        tweaks = []
        for bone in dict.keys():
            head = dict[bone][0]
            tail = dict[bone][1]
            roll = dict[bone][2]
            boneName = bone[:-4]
            num = bone.split('_')[-1]
            bone = utils.addBone(arm, name='def.{}.{}.{}'.format(boneName, side, num.zfill(3)), head=head, tail=tail, roll=roll)
            defBones.append(bone)
        
        for eBone in defBones:
            # con bones
            conBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','con'), scale = 1) 
            conBones.append(conBone)
            # hlp bones
            prtBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','prt'), scale = .5) 
            prtBones.append(prtBone)
            # fk controls
            baseName = eBone.name.split('.')[1] 
            fkBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','ctl').replace(baseName, baseName+'_fk'), scale = 1) 
            fkBones.append(fkBone)
            # tweaks
            tweak = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','ctl').replace(baseName, baseName+'_tweak'), scale = .5)
            tweaks.append(tweak)
            if eBone == defBones[-1]:
                head = eBone.tail
                tail = (eBone.tail[0]+1, eBone.tail[1], eBone.tail[2])
                num = int(eBone.name.split('.')[-1]) 
                newNum = num + 1
                name = eBone.name.replace('def','ctl').replace(baseName, baseName+'_tweak').replace(str(num), str(newNum))
                tweak = utils.addBone(arm, name=name, head=head, tail=tail, roll=eBone.roll)
                tweak.length = eBone.length
                tweaks.append(tweak)

        #store bone names
        defBoneNames = [bone.name for bone in defBones]
        conBoneNames = [bone.name for bone in conBones]
        prtBoneNames = [bone.name for bone in prtBones]
        fkBoneNames = [bone.name for bone in fkBones]
        bendCtlNames = [bone.name for bone in bendCtls]
        tweaksNames = [bone.name for bone in tweaks]

        # set bone layers
        # def
        for bone in defBones:
            bone.layers[31] = True
            bone.layers[0] = False
        # con
        for bone in conBones:
            bone.layers[30] = True
            bone.layers[0] = False
        # prt
        for bone in prtBones:
            bone.layers[25] = True
            bone.layers[0] = False
        # controls  
        for bone in fkBones:
            bone.layers[1] = True
            bone.layers[0] = False 
        # tweaks
        for bone in tweaks :
            bone.layers[3] = True
            bone.layers[0] = False 

        # parent bones
        # def
        utils.parent_bone_chain(defBones, connected=True) 
        defBones[0].parent = mstBone
        # con bones
        utils.parent_bone_chain(conBones, connected=True) 
        conBones[0].parent = mstBone
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
        for i, bone  in enumerate(tweaks):
            if bone is not tweaks[-1]:
                bone.parent = fkBones[i]
            else:
                bone.parent = fkBones[-1]


        bpy.ops.object.mode_set(mode='POSE')
        # constrain joints
        # def
        for boneName, targetName in zip(defBoneNames, conBoneNames):
            copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
            copyTrans.target = arm
            copyTrans.subtarget = targetName
        # con
        for i, boneName in enumerate(conBoneNames):
            targetName = tweaksNames[i]
            copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
            copyTrans.target = arm
            copyTrans.subtarget = targetName

            targetName = tweaksNames[i+1]
            stretchTo = arm.pose.bones[boneName].constraints.new('STRETCH_TO')
            stretchTo.target = arm
            stretchTo.subtarget = targetName
        # prt
        subtarget = handCtlName
        for boneName in prtBoneNames[1:]:
            transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM') #rot x transformation
            transformCon.name = 'Hand Control Rot X Transformation'
            transformCon.target = arm
            transformCon.subtarget = subtarget
            transformCon.use_motion_extrapolate = True
            transformCon.owner_space = 'LOCAL'  
            transformCon.target_space = 'LOCAL' 
            transformCon.map_from = 'ROTATION'
            transformCon.map_to = 'ROTATION' 
            transformCon.from_min_x_rot = -1
            transformCon.to_min_x_rot = -1
            transformCon.from_max_x_rot = 1 
            transformCon.to_max_x_rot = 1 
        for i, boneName in enumerate(prtBoneNames[0:2]):
            if 'index' not in boneName and 'thumb' not in boneName:
                transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM') #rot y transformation
                transformCon.name = 'Hand Control Rot Y Transformation'
                transformCon.target = arm
                transformCon.subtarget = subtarget
                transformCon.use_motion_extrapolate = True
                transformCon.owner_space = 'LOCAL'  
                transformCon.target_space = 'LOCAL' 
                transformCon.map_from = 'ROTATION'
                transformCon.map_to = 'ROTATION' 
                transformCon.map_to_x_from = 'Y' 
                transformCon.from_max_y_rot = radians(1)
                transformCon.to_max_x_rot = radians(1)
                influence = 1
                if i == 0:
                    influence = influence/4
                if 'middle' in boneName:
                    influence = influence*.33
                if 'ring' in boneName:
                    influence = influence*.6
                transformCon.influence = influence
        boneName = prtBoneNames[0]
        if 'index' in boneName or 'ring' in boneName or 'pinky' in boneName:
            transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM') #rot x transformation
            transformCon.name = 'Hand Control Rot Y Transformation'
            transformCon.target = arm
            transformCon.subtarget = subtarget
            transformCon.use_motion_extrapolate = True
            transformCon.owner_space = 'LOCAL'  
            transformCon.target_space = 'LOCAL' 
            transformCon.map_from = 'SCALE'
            transformCon.map_to = 'ROTATION' 
            transformCon.map_to_z_from = 'X' 
            transformCon.from_min_x_scale = 1
            transformCon.from_max_x_scale = 2
            if 'index' in boneName:
                to_max_z_rot = radians(-20)
            elif 'ring' in boneName:
                to_max_z_rot = radians(10)
            elif 'pinky' in boneName:
                to_max_z_rot = radians(20)
            if i == 0:
                to_max_z_rot = to_max_z_rot/4
            transformCon.to_max_z_rot = to_max_z_rot
        if 'thumb' not in boneName:
            for boneName, subtarget in zip(prtBoneNames, bendCtls):
                transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM') #rot x transformation
                transformCon.name = 'Bend Rot X Transformation'
                transformCon.target = arm
                transformCon.subtarget = subtarget
                transformCon.use_motion_extrapolate = True
                transformCon.owner_space = 'LOCAL'  
                transformCon.target_space = 'LOCAL' 
                transformCon.map_from = 'ROTATION'
                transformCon.map_to = 'ROTATION' 
                transformCon.from_min_x_rot = -1
                transformCon.to_min_x_rot = -1
                transformCon.from_max_x_rot = 1 
                transformCon.to_max_x_rot = 1 
        

    bpy.ops.object.mode_set(mode='OBJECT')

class HandGuides(component.CreateGuides):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "guide.hand"
    bl_label = "Hand Guides"

    componentParent = ''#parent guide
    guideInfoDict = {} #tag:[world matrix, parent, guide shape, def/hlp]

    def execute(self, context):
        boneDict = utils.get_bone_dict_data(fileName='hand_guide_data.json')
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
            utils.add_custom_property_to_pose_bone(arm, boneName=name, propertyName="Component", default='hand')

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

class BUILD_OT_Hand(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "build.hand"
    bl_label = "Limb Build"

    def execute(self, context):
        build('L')
        boneNames = [bone.name for bone in bpy.data.armatures['guideArmature'].bones]
        if 'index_finger_R_1' in boneNames:
            build('R')
        return {"FINISHED"}



classes = [HandGuides, BUILD_OT_Hand]