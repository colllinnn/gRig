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

def build(side):
    # create legature
    arm = bpy.data.objects['buildArmature']
    gAarm = bpy.data.objects['guideArmature']
    boneDict = {
    'upper_leg_{}'.format(side) : utils.get_bone_location(gAarm, 'upper_leg_{}'.format(side)), 
    'lower_leg_{}'.format(side) : utils.get_bone_location(gAarm, 'lower_leg_{}'.format(side)), 
    'ankle_{}'.format(side) : utils.get_bone_location(gAarm, 'ankle_{}'.format(side)), 
    }
    defBones = []
    conBones = []
    hlpTwistBones = []
    hlpBones = []
    mstBone = ''
    ikmBones = []
    noStretchIkmBones = []
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
    legControl = ''
    # create def joints
    keyList = list(boneDict.keys())
    upperLegLocations = []
    lowerLegLocations = []
    for i in range(2):
        location1 = boneDict[keyList[i]][0]
        location5 = boneDict[keyList[i]][1]
        roll = boneDict[keyList[0]][2]
        location2 = utils.find_in_betweeen_point(location1, location5, 0.75,  0.25)
        location3 = utils.find_in_betweeen_point(location1, location5, 0.5,  0.5)
        location4 = utils.find_in_betweeen_point(location1, location5, 0.25,  0.75)

        if i == 0:
            upperLegLocations.extend([location1, location2, location3, location4, location5])
        else:
            lowerLegLocations.extend([location1, location2, location3, location4, location5])

    for index, location in enumerate(upperLegLocations):
        if location != upperLegLocations[-1]:
            head = upperLegLocations[index]
            tail = upperLegLocations[index+1]
            bone = utils.addBone(arm, name='def.upper_leg.{}.00{}'.format(side, str(index+1)), head=head, tail=tail, roll=roll)
            defBones.append(bone)

    for index, location in enumerate(lowerLegLocations):
        if location != lowerLegLocations[-1]:
            head = lowerLegLocations[index]
            tail = lowerLegLocations[index+1]
            bone = utils.addBone(arm, name='def.lower_leg.{}.00{}'.format(side, str(index+1)), head=head, tail=tail, roll=roll)
            defBones.append(bone)

    head = boneDict[keyList[2]][0]
    tail = boneDict[keyList[2]][1]
    roll = boneDict[keyList[0]][2]
    bone = utils.addBone(arm, name='def.ankle.{}.001'.format(side), head=head, tail=tail, roll=roll)
    # hlp bones
    for eBone in defBones:
        # con bones
        conBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def', 'con'), scale = .8) 
        conBones.append(conBone)
        #hlp twist bones
        baseName = eBone.name.split('.')[1] 
        hlpBoneName = eBone.name.replace('def', 'hlp').replace(baseName, baseName + '_twist')
        hlpTwistBone = utils.duplicate_bone(arm, eBone, hlpBoneName, scale = .6) 
        hlpTwistBones.append(hlpTwistBone)
    # mst bone
    mstBone = utils.addBone(arm, name='mst.leg.{}.001'.format(side), head=boneDict['upper_leg_{}'.format(side)][0], tail=boneDict['upper_leg_{}'.format(side).format(side)][1], roll=roll)
    mstBone.length = mstBone.length*.5
    # hlp bones
    for bone in boneDict.keys():
        name = bone[0:-2]
        head = boneDict[bone][0]
        tail = boneDict[bone][1]
        roll = boneDict[bone][2]
        hlpBone = utils.addBone(arm, name='hlp.{}.{}.001'.format(name, side), head=head, tail=tail, roll=roll)
        hlpBones.append(hlpBone)
    # ikm bones
    for eBone in hlpBones:
        #ikm bones 
        ikmBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('hlp', 'ikm'), scale = 1) 
        ikmBones.append(ikmBone)
        #ikm no stretch bones
        baseName = eBone.name.split('.')[1]
        noStretchIkmBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('hlp', 'ikm').replace(baseName, baseName+'_no_stretch'), scale = 1) 
        noStretchIkmBones.append(noStretchIkmBone)
    # hlp stretch bones
    for eBone in hlpBones:
        baseName = eBone.name.split('.')[1] 
        hlpIkStretchBone = utils.duplicate_bone(arm, eBone, eBone.name.replace(baseName, baseName + '_ik_stretch'), scale = .5) 
        hlpIkStretchBones.append(hlpIkStretchBone)
    i=1
    # tweak prt bones
    for eBone in [defBones[2], defBones[4], defBones[6]]:
        tweakParentBone = utils.duplicate_bone(arm, eBone, 'prt.leg_fk_tweak.{}.00{}'.format(side, str(i)), scale = .4)
        tweakParentBones.append(tweakParentBone)
        i += 1
    # ik prt bone
    ikPrtBone = utils.addBone(arm, name='prt.leg_ik.{}.001'.format(side), head=boneDict['upper_leg_{}'.format(side)][0], tail=boneDict['upper_leg_{}'.format(side)][1], roll=roll)
    ikPrtBone.length = ikPrtBone.length*.4
    # pole vector prt bone
    ikPolePrtBone = utils.addBone(arm, name='prt.leg_pole_vector.{}.001'.format(side), head=boneDict['upper_leg_{}'.format(side)][0], tail=boneDict['ankle_{}'.format(side)][1], roll=roll)
    '''
    avgHead = ((boneDict['upper_leg_{}'.format(side)][0][0]+boneDict['ankle_{}'.format(side)][0][0])/2, (boneDict['upper_leg_{}'.format(side)][0][1]+boneDict['ankle_{}'.format(side)][0][1])/2, (boneDict['upper_leg_{}'.format(side)][0][2]+boneDict['ankle_{}'.format(side)][0][2])/2)
    avgTail = ((boneDict['upper_leg_{}'.format(side)][1][0]+boneDict['ankle_{}'.format(side)][1][0])/2, (boneDict['upper_leg_{}'.format(side)][1][1]+boneDict['ankle_{}'.format(side)][1][1])/2, (boneDict['upper_leg_{}'.format(side)][1][2]+boneDict['ankle_{}'.format(side)][1][2])/2)
    ikPolePrtBone = utils.addBone(arm, name='prt.leg_pole_vector.{}.001'.format(side), head=avgHead, tail=avgTail, roll=roll)
    ikPolePrtBone.length = ikPolePrtBone.length*.4
    '''
    # tweak control bones
    i=1
    for eBone in tweakParentBones:
        tweak = utils.duplicate_bone(arm, eBone, 'ctl.leg_fk_tweak.{}.00{}'.format(side,str(i)), scale = 1)
        tweaks.append(tweak)
        i += 1
    # fk bones
    for eBone in hlpBones:
        #main
        baseName = eBone.name.split('.')[1] 
        fkBone = utils.duplicate_bone(arm, eBone, eBone.name.replace(baseName, baseName + '_fk').replace('hlp','ctl'), scale = 1) 
        fkBones.append(fkBone)
        #sub
        fkSubBone = utils.duplicate_bone(arm, eBone, eBone.name.replace(baseName, baseName + '_fk_sub').replace('hlp','ctl'), scale = .75)
        fkSubBones.append(fkSubBone)
    # ik bones
    for eBone in [hlpBones[0], hlpBones[2]]:
        #main
        baseName = eBone.name.split('.')[1] 
        ikBone = utils.duplicate_bone(arm, eBone, eBone.name.replace(baseName, baseName + '_ik').replace('hlp','ctl'), scale = 1) 
        ikBones.append(ikBone)
        #sub
        ikSubBone = utils.duplicate_bone(arm, eBone, eBone.name.replace(baseName, baseName + '_ik_sub').replace('hlp','ctl'), scale = .75)
        ikSubBones.append(ikSubBone)
    # pole vector
    head = (boneDict['lower_leg_{}'.format(side)][0][0], boneDict['lower_leg_{}'.format(side)][0][1]-1, boneDict['lower_leg_{}'.format(side)][0][2])
    tail = (head[0]-1, head[1], head[2])
    poleVector = utils.addBone(arm, name='ctl.leg_pole_vector.{}.001'.format(side), head=head, tail=tail, roll=roll)
    poleVectorSub = utils.addBone(arm, name='ctl.leg_pole_vector_sub.{}.001'.format(side), head=head, tail=tail, roll=roll)
    poleVectorSub.length = poleVectorSub.length*.7
    # property control bone
    head = (boneDict['ankle_{}'.format(side)][0][0], boneDict['ankle_{}'.format(side)][0][1]-1, boneDict['ankle_{}'.format(side)][0][2] )
    tail = (boneDict['ankle_{}'.format(side)][1][0], boneDict['ankle_{}'.format(side)][1][1]-1, boneDict['ankle_{}'.format(side)][1][2] )
    legControl = utils.addBone(arm, name='ctl.leg_controls.{}.001'.format(side), head=head, tail=tail, roll=roll)
    
    #store bone names
    defBoneNames = [bone.name for bone in defBones]
    conBoneNames = [bone.name for bone in conBones]
    fkBoneNames = [bone.name for bone in fkBones]
    tweaksNames = [bone.name for bone in tweaks]

    hlpTwistBoneNames = [bone.name for bone in hlpTwistBones]
    hlpBoneNames = [bone.name for bone in hlpBones]
    mstBoneName = mstBone.name
    ikmBoneNames = [bone.name for bone in ikmBones]
    noStretchIkmBoneNames = [bone.name for bone in noStretchIkmBones]
    hlpIkStretchBoneNames = [bone.name for bone in hlpIkStretchBones]
    tweakParentBoneNames = [bone.name for bone in tweakParentBones]
    ikPrtBoneName = ikPrtBone.name
    tweakNames = [bone.name for bone in tweaks]
    fkBoneNames = [bone.name for bone in fkBones]
    fkSubBoneNames = [bone.name for bone in fkSubBones]
    ikBoneNames = [bone.name for bone in ikBones]
    ikSubBoneNames = [bone.name for bone in ikSubBones]
    poleVectorName = poleVector.name
    poleVectorSubName = poleVectorSub.name
    legControlName = legControl.name
    ikPolePrtBoneName = ikPolePrtBone.name

    # set bone layers
    # def
    for bone in defBones:
        bone.layers[utils.boneLayerDict['def']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # con
    for bone in conBones:
        bone.layers[utils.boneLayerDict['con']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # hlp twist
    for bone in hlpTwistBones:
        bone.layers[utils.boneLayerDict['hlp']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # hlp
    for bone in hlpBones:
        bone.layers[utils.boneLayerDict['hlp']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # ikm, ikNoStretch
    for bone in noStretchIkmBones + ikmBones:
        bone.layers[utils.boneLayerDict['hlp']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # hlpIkStretchBones
    for bone in hlpIkStretchBones:
        bone.layers[utils.boneLayerDict['hlpStretch']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # parent bones
    for bone in tweakParentBones + [ikPrtBone] + [ikPolePrtBone]:
        bone.layers[utils.boneLayerDict['ikm']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # fk controls
    for bone in fkBones + fkSubBones:
        bone.layers[utils.boneLayerDict['fk']] = True
        bone.layers[utils.boneLayerDict['god']] = False 
    # ik controls
    for bone in ikBones + ikSubBones + [poleVector] + [poleVectorSub]:
        bone.layers[utils.boneLayerDict['ik']] = True
        bone.layers[utils.boneLayerDict['god']] = False 
    # property bone 
    for bone in tweaks:
        bone.layers[utils.boneLayerDict['tweak']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # legControl
    legControl.layers[utils.boneLayerDict['fk']] = True
    legControl.layers[utils.boneLayerDict['ik']] = True
    legControl.layers[utils.boneLayerDict['god']] = False
    # mstBone
    mstBone.layers[utils.boneLayerDict['mst']] = True
    mstBone.layers[utils.boneLayerDict['god']] = False

    # parent bones
    # def
    utils.parent_bone_chain(defBones, connected=True) 
    defBones[0].parent = mstBone
    #con
    utils.parent_bone_chain(conBones, connected=False) 
    conBones[0].parent = mstBone
    #hlp twist
    for i, bone in enumerate(hlpTwistBones):
        if i < 4:
            bone.parent = bpy.data.objects['buildArmature'].data.edit_bones['hlp.upper_leg.{}.001'.format(side)]
        elif i > 3:
            bone.parent = bpy.data.objects['buildArmature'].data.edit_bones['hlp.lower_leg.{}.001'.format(side)]
        elif i == (len(hlpTwistBones)-1):
            bone.parent = bpy.data.objects['buildArmature'].data.edit_bones['hlp.ankle.{}.001'.format(side)]
    # fkBones
    i = 0
    for main, sub in zip(fkBones, fkSubBones):
        sub.parent = main
    for i, ctl in enumerate(fkBones):
        if i is not 0:
            ctl.parent = fkSubBones[i-1]
        else:
            ctl.parent = mstBone
    # ikBones
    for main, sub in zip (ikBones, ikSubBones):
        sub.parent = main
    ikBones[0].parent = mstBone
    ikBones[1].parent = ikPrtBone
    # tweaks
    for ctl, prt in zip(tweaks, tweakParentBones):
        ctl.parent = prt
    # poleVectorSub
    poleVectorSub.parent = poleVector
    poleVector.parent = ikPolePrtBone
    # hlp 
    for bone in hlpBones:
        bone.parent = mstBone
    # ikm + ikm no stretch
    utils.parent_bone_chain(ikmBones, connected=True) 
    utils.parent_bone_chain(noStretchIkmBones, connected=True) 
    for boneList in [ikmBones, noStretchIkmBones]:
        boneList[0].use_connect = False
        boneList[0].parent = ikSubBones[0]
        boneList[2].use_connect = False
        boneList[2].parent = ikSubBones[0]
    # hlpIkStretchBones
    for i, bone in enumerate(hlpIkStretchBones):
        if i < 2:
            bone.parent = noStretchIkmBones[i]
        else:
            bone.parent = hlpIkStretchBones[i-1]
    # ik prt
    ikPrtBone.parent = mstBone
    # ik pole prt
    ikPolePrtBone.parent = mstBone
    # prt tweak bones
    for i, bone in enumerate(tweakParentBones):
        if i == 0:
            bone.parent = hlpBones[0]
        elif i == 1:
            bone.parent = mstBone
        else:
            bone.parent = hlpBones[1]
    # legControl
    legControl.parent = hlpBones[2]

    bpy.ops.object.mode_set(mode='POSE')
    # custom properties
    utils.add_custom_property_to_pose_bone(arm, boneName=legControlName, propertyName="IKFK_switch", default=1.0, min=0.0, max=1.0 )
    utils.add_custom_property_to_pose_bone(arm, boneName=legControlName, propertyName="IKPoleVector_follow_god_ankle", default=1.0, min=0.0, max=1.0 )
    utils.add_custom_property_to_pose_bone(arm, boneName=legControlName, propertyName="IK_stretch", default=0.0, min=0.0, max=1.0 )
    utils.add_custom_property_to_pose_bone(arm, boneName=legControlName, propertyName="auto_bend_switch", default=0.0, min=0.0, max=1.0 )
    utils.add_custom_property_to_pose_bone(arm, boneName=legControlName, propertyName="volume_preservation", default=1.0, min=0.0, max=1.0 )

    # constrain joints
    # def constraints
    for boneName, subtargetName in zip(defBoneNames, conBoneNames):
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = subtargetName
    # con constraints
    i=0
    for boneName, subtargetName in zip(conBoneNames, hlpTwistBoneNames):
        pBone = arm.pose.bones[boneName]
        copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = subtargetName
        if i != len(hlpTwistBoneNames)-1:
            stretchTO = pBone.constraints.new('STRETCH_TO')
            stretchTO.target = arm
            stretchTO.subtarget = hlpTwistBoneNames[i+1]
            drv = utils.add_driver(pBone.constraints['{}'.format(stretchTO.name)], 'bulge', func = 'var')
            utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["volume_preservation"]'.format(side))
            i+=1
    # hlp twist constraints
    for i,boneName in enumerate(hlpTwistBoneNames):
        if i < 4:
            subtarget = 'hlp.upper_leg.{}.001'.format(side)
            transSubtarget = 'ctl.leg_fk_tweak.{}.001'.format(side)
        elif 3 < i < 8 :
            subtarget = 'hlp.lower_leg.{}.001'.format(side)
            transSubtarget = 'ctl.leg_fk_tweak.{}.003'.format(side)
        if i in (1, 3, 5, 7):
            # copy location
            copyLoc = arm.pose.bones[boneName].constraints.new('COPY_LOCATION')
            copyLoc.target = arm
            copyLoc.subtarget = subtarget
            copyLoc.use_bbone_shape = True
            if i in [1, 5]:
                copyLoc.head_tail = 0.25
            else:
                copyLoc.head_tail = 0.75
            # copy rotation
            copyRot = arm.pose.bones[boneName].constraints.new('COPY_ROTATION')
            copyRot.target = arm
            copyRot.subtarget = subtarget  
            copyRot.use_x = False
            copyRot.use_z = False
            # Location Y Transformation
            transformYLoc = arm.pose.bones[boneName].constraints.new('TRANSFORM')
            transformYLoc.name = 'Transformation Y Location'
            transformYLoc.target = arm
            transformYLoc.subtarget = transSubtarget  
            transformYLoc.use_motion_extrapolate = True
            transformYLoc.owner_space = 'LOCAL'  
            transformYLoc.target_space = 'LOCAL'  
            transformYLoc.from_min_y = -1
            transformYLoc.from_max_y = 1
            transformYLoc.to_min_y = -0.5
            transformYLoc.to_max_y = 0.5
            # Rotation Y Transformation
            transformYRot = arm.pose.bones[boneName].constraints.new('TRANSFORM')
            transformYRot.name = 'Transformation Y Rotation'
            transformYRot.target = arm
            transformYRot.subtarget = transSubtarget  
            transformYRot.use_motion_extrapolate = True
            transformYRot.owner_space = 'LOCAL'  
            transformYRot.target_space = 'LOCAL' 
            transformYRot.map_from = 'ROTATION'
            transformYRot.map_to = 'ROTATION'
            transformYRot.from_min_y_rot = radians(-1)
            transformYRot.from_max_y_rot = radians(1)
            transformYRot.to_min_y_rot = radians(-0.5)
            transformYRot.to_max_y_rot = radians(0.5)

        elif i in (2, 6):
            copyLoc = arm.pose.bones[boneName].constraints.new('COPY_LOCATION')
            copyLoc.target = arm
            copyLoc.subtarget = subtarget
            copyLoc.use_bbone_shape = True
            copyLoc.head_tail = 0.5
            # copy rotation
            copyRot = arm.pose.bones[boneName].constraints.new('COPY_ROTATION')
            copyRot.target = arm
            copyRot.subtarget = subtarget  
            copyRot.use_x = False
            copyRot.use_z = False
        
        elif i in (2, 6):
            if i == 2:
                coptTransSubTarget = 'ctl.leg_fk_tweak.{}.001'.format(side)
            elif i == 6:
                coptTransSubTarget = 'ctl.leg_fk_tweak.{}.002'.format(side)
            copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
            copyTrans.target = arm
            copyTrans.subtarget = coptTransSubTarget

            copyRot = arm.pose.bones[boneName].constraints.new('COPY_ROTATION')
            copyRot.target = arm
            copyRot.subtarget = subtarget
            copyRot.use_x = False
            copyRot.use_z = False
            copyRot.influence = 0.5
            # Rotation Y Transformation     
            transformYRot = arm.pose.bones[boneName].constraints.new('TRANSFORM')
            transformYRot.name = 'Transformation Y Rotation'
            transformYRot.target = arm
            transformYRot.subtarget = transSubtarget  
            transformYRot.use_motion_extrapolate = True
            transformYRot.owner_space = 'LOCAL'  
            transformYRot.target_space = 'LOCAL' 
            transformYRot.map_from = 'ROTATION'
            transformYRot.map_to = 'ROTATION'
            transformYRot.from_min_y_rot = radians(-1)
            transformYRot.from_max_y_rot = radians(1)
            transformYRot.to_min_y_rot = radians(-1)
            transformYRot.to_max_y_rot = radians(1)

        elif i in (0, 4, 8):
            if i== 0:
                subtarget = 'hlp.upper_leg.{}.001'.format(side)
            elif i== 0:
                subtarget = 'hlp.lower_leg.{}.001'.format(side)
            elif i== 0:
                subtarget = 'hlp.ankle.{}.001'.format(side)

            copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
            copyTrans.target = arm
            copyTrans.subtarget = subtarget
    # hlp constraints
    # copy Transform fk
    for i,boneName in enumerate(hlpBoneNames):
        pBone = arm.pose.bones[boneName]
        copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
        copyTrans.name = 'Copy Transforms FK'
        copyTrans.target = arm
        if i == 0: 
            copyTrans.subtarget = 'ctl.upper_leg_fk_sub.{}.001'.format(side)
        if i == 1: 
            copyTrans.subtarget = 'ctl.lower_leg_fk_sub.{}.001'.format(side)
        if i == 2: 
            copyTrans.subtarget = 'ctl.ankle_fk_sub.{}.001'.format(side)
    # copy Transform ik
        copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
        copyTrans.name = 'Copy Transforms IK'
        copyTrans.target = arm
        if i == 0: 
            copyTrans.subtarget = 'hlp.upper_leg_ik_stretch.{}.001'.format(side)
        if i == 1: 
            copyTrans.subtarget = 'hlp.lower_leg_ik_stretch.{}.001'.format(side)
        if i == 2: 
            copyTrans.subtarget = 'hlp.ankle_ik_stretch.{}.001'.format(side)
        # copy transforms driver   
        drv = utils.add_driver(pBone.constraints['{}'.format(copyTrans.name)], 'influence', func = 'var')
        utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["IKFK_switch"]'.format(side))
        # copy Location tweak
        if i in [0, 1]:
            copyLoc = pBone.constraints.new('COPY_LOCATION')
            copyLoc.name = 'Copy Location Tweak'
            copyLoc.target = arm
            if i == 0: 
                copyLoc.subtarget = 'hlp.upper_leg_ik_stretch.{}.001'.format(side)
            if i == 1: 
                copyLoc.subtarget = 'ctl.leg_fk_tweak.{}.002'.format(side)
            # stretch to
            stretchTO = arm.pose.bones[boneName].constraints.new('STRETCH_TO')
            stretchTO.target = arm
            stretchTO.subtarget = hlpBoneNames[i+1]
            # Y rotation transformation
            if i == 1:
                transformYRot = arm.pose.bones[boneName].constraints.new('TRANSFORM')
                transformYRot.name = 'Transformation Y Rotation'
                transformYRot.target = arm
                transformYRot.subtarget = 'ctl.leg_fk_tweak.{}.002'.format(side)
                transformYRot.use_motion_extrapolate = True
                transformYRot.owner_space = 'LOCAL'  
                transformYRot.target_space = 'LOCAL' 
                transformYRot.map_from = 'ROTATION'
                transformYRot.map_to = 'ROTATION'
                transformYRot.from_min_y_rot = radians(-1)
                transformYRot.from_max_y_rot =radians( 1)
                transformYRot.to_min_y_rot = radians(-1)
                transformYRot.to_max_y_rot = radians(1)

    # ikm constraints + ikm no stretch
    # ik handle 
    for boneList in [noStretchIkmBoneNames, ikmBoneNames]:
        boneName = boneList[1]
        IK = arm.pose.bones[boneName].constraints.new('IK')
        IK.target = arm
        IK.subtarget  = 'ctl.ankle_ik_sub.{}.001'.format(side)
        IK.pole_target = arm
        IK.pole_subtarget = 'ctl.leg_pole_vector_sub.{}.001'.format(side)
        IK.pole_angle = -1.5708
        IK.chain_count = 2
        if boneList == noStretchIkmBoneNames:
            IK.use_stretch = False
        else:
            arm.pose.bones[boneName].ik_stretch = 0.1
    # copy transform
        boneName = boneList[2]
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = 'ctl.ankle_ik_sub.{}.001'.format(side)
    
    # hlp IK bone constraints
    # copy transforms
    i=0
    for boneName, subtarget in zip(hlpIkStretchBoneNames, ikmBoneNames):
        pBone = arm.pose.bones[boneName]
        if i in (0,1):
            copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
            copyTrans.target = arm
            copyTrans.subtarget = subtarget
            drv = utils.add_driver(pBone.constraints['{}'.format(copyTrans.name)], 'influence', func = 'var')
            utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["IK_stretch"]'.format(side))
        else:
            # copy rotation/scale
            subtarget = 'ctl.leg_ik_sub.{}.002'.format(side)
            copyRot = pBone.constraints.new('COPY_ROTATION')
            copyRot.target = arm
            copyRot.subtarget = subtarget
            copyScale = pBone.constraints.new('COPY_SCALE')
            copyScale.target = arm
            copyScale.subtarget = subtarget

    # prt
    # ik prt
    pBone = arm.pose.bones[ikPrtBoneName]
    copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
    copyTrans.target = arm
    copyTrans.subtarget = 'ctl.upper_leg_ik_sub.{}.001'.format(side)
    # ikPolePrtBone
    pBone = arm.pose.bones[ikPolePrtBoneName]
    copyTrans = pBone.constraints.new('DAMPED_TRACK')
    copyTrans.target = arm
    copyTrans.subtarget = 'ctl.foot_ik_sub.{}.001'.format(side)
    '''
    pBone = arm.pose.bones[ikPolePrtBoneName]
    copyTrans = pBone.constraints.new('COPY_LOCATION')
    copyTrans.target = arm
    copyTrans.subtarget = 'ctl.ankle_ik_sub.{}.001'.format(side)
    drv = utils.add_driver(pBone.constraints['{}'.format(copyTrans.name)], 'influence', func = 'var')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["IKPoleVector_follow_god_ankle"]'.format(side))
    
    copyTrans = pBone.constraints.new('COPY_LOCATION')
    copyTrans.target = arm
    copyTrans.subtarget = 'mst.leg.{}.001'.format(side)
    copyTrans.influence = .5
    drv = utils.add_driver(pBone.constraints['{}'.format(copyTrans.name)], 'influence', func = 'var/2')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["IKPoleVector_follow_god_ankle"]'.format(side))
    '''
    # prt tweak 
    pBone = arm.pose.bones[tweakParentBoneNames[1]]
    copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
    copyTrans.name = 'Copy Transforms FK'
    copyTrans.target = arm
    copyTrans.subtarget = 'ctl.lower_leg_fk_sub.{}.001'.format(side)

    copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
    copyTrans.name = 'Copy Transforms IK'
    copyTrans.target = arm
    copyTrans.subtarget = 'hlp.lower_leg_ik_stretch.{}.001'.format(side)
    drv = utils.add_driver(pBone.constraints['{}'.format(copyTrans.name)], 'influence', func = 'var')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["IKFK_switch"]'.format(side))

    copyRot = pBone.constraints.new('COPY_ROTATION')
    copyRot.name = 'Copy Rotation FK'
    copyRot.target = arm
    copyRot.influence = .5
    copyRot.subtarget = 'ctl.lower_leg_fk_sub.{}.001'.format(side)

    copyRot = pBone.constraints.new('COPY_ROTATION')
    copyRot.name = 'Copy Rotation IK'
    copyRot.target = arm
    copyRot.influence = .5
    copyRot.subtarget = 'hlp.upper_leg_ik_stretch.{}.001'.format(side)
    drv = utils.add_driver(pBone.constraints['{}'.format(copyRot.name)], 'influence', func = 'var/2')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["IKFK_switch"]'.format(side))

    # prt tweak drivers
    for i, boneName in enumerate(tweakParentBoneNames):
        if i in (0,2):
            pBone = arm.pose.bones[boneName]
            drv = utils.add_driver(pBone, 'location', func = '(1/1.8-scale/1.8) +(auto_switch*(auto/5))', index=0)
            if i == 2:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.003"].location[0]'.format(side))
            else:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.001"].location[0]'.format(side))
            utils.add_driver_transform_variable(drv, varName='auto', target=arm, bone_target='hlp.lower_leg.{}.001'.format(side), transform_type='ROT_Z', transform_space = 'LOCAL_SPACE')
            utils.add_driver_variable(drv, varName='scale', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.002"].scale[1]'.format(side))
            utils.add_driver_variable(drv, varName='auto_switch', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["auto_bend_switch"]'.format(side))
    
    # hlp drivers
    for i, boneName in enumerate(hlpBoneNames):
        if i in (0,1):
            arm.data.bones[boneName].bbone_segments = 10
            pBone = arm.pose.bones[boneName]
            drv = utils.add_driver(pBone, 'bbone_curveinx', func = '(var*1.51+1/1.5-scale/1.5) -(auto_switch*(auto/7))')
            if i == 1:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.003"].location[0]'.format(side))
            else:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.001"].location[0]'.format(side))
            utils.add_driver_variable(drv, varName='scale', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.002"].scale[1]'.format(side))
            utils.add_driver_rotation_diff_variable(drv, varName='auto', target=arm, bone_target1='hlp.leg.{}.001'.format(side), bone_target2='hlp.leg.{}.002'.format(side))
            utils.add_driver_variable(drv, varName='auto_switch', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["auto_bend_switch"]'.format(side))
    
            drv = utils.add_driver(pBone, 'bbone_curveoutx', func = '(var*1.51+1/1.5-scale/1.5) +(auto_switch*(auto/3))')
            if i == 1:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.003"].location[0]'.format(side))
            else:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.001"].location[0]'.format(side))
            utils.add_driver_variable(drv, varName='scale', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.002"].scale[1]'.format(side))
            utils.add_driver_transform_variable(drv, varName='auto', target=arm, bone_target='hlp.lower_leg.{}.001'.format(side), transform_type='ROT_Z', transform_space = 'LOCAL_SPACE')
            utils.add_driver_variable(drv, varName='auto_switch', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["auto_bend_switch"]'.format(side))
    
            drv = utils.add_driver(pBone, 'bbone_curveinz', func = 'var*1.5')
            if i == 1:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.003"].location[2]'.format(side))
            else:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.001"].location[2]'.format(side))

            drv = utils.add_driver(pBone, 'bbone_curveoutz', func = 'var*1.5')
            if i == 1:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.003"].location[2]'.format(side))
            else:
                utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_fk_tweak.{}.001"].location[2]'.format(side))
    bpy.ops.object.mode_set(mode='OBJECT')

class LegGuides(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "guide.leg"
    bl_label = "Leg Guides"

    componentParent = ''#parent guide
    guideInfoDict = {} #tag:[world matrix, parent, guide shape, def/hlp]

    def execute(self, context):
        boneDict = boneDict = utils.get_bone_dict_data(fileName='leg_guide_data.json') 
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
            utils.add_custom_property_to_pose_bone(arm, boneName=editBone.name, propertyName="Component", default='leg' )

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

class BUILD_OT_Leg(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "build.leg"
    bl_label = "Leg Build"

    def execute(self, context):
        build('L')
        boneNames = [bone.name for bone in bpy.data.armatures['guideArmature'].bones]
        if 'upper_leg_R' in boneNames:
            build('R')
        return {"FINISHED"}

classes = [LegGuides, BUILD_OT_Leg]