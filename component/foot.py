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
    boneDict = {
    'ankle_{}'.format(side) : utils.get_bone_location(gArm, 'ankle_{}'.format(side)),
    'toe_{}'.format(side) : utils.get_bone_location(gArm, 'toe_{}'.format(side)),
    'heel_pivot_{}'.format(side) : utils.get_bone_location(gArm, 'heel_pivot_{}'.format(side)),
    'toe_pivot_{}'.format(side) : utils.get_bone_location(gArm, 'toe_pivot_{}'.format(side)),
    'inner_pivot_{}'.format(side) : utils.get_bone_location(gArm, 'inner_pivot_{}'.format(side)),
    'outer_pivot_{}'.format(side) : utils.get_bone_location(gArm, 'outer_pivot_{}'.format(side)),
    'ball_pivot_{}'.format(side) : utils.get_bone_location(gArm, 'ball_pivot_{}'.format(side)),
    'leg_control_{}'.format(side) :  utils.get_bone_location(gArm, 'leg_control_{}'.format(side)),
    'heel_control_{}'.format(side) :  utils.get_bone_location(gArm, 'heel_control_{}'.format(side))
    }
    defBones = []
    conBones = []
    hlpSwitchBones = []
    hlpBones = []
    mstBone = ''
    ikmBones = []
    ikmPivots = []
    ikControls = []
    fkBones = []
    fkSubBones = []

    # create edit bones
    # mst bone
    mstBone = utils.addBone(arm, name='mst.foot.{}.001'.format(side), head=boneDict['ankle_{}'.format(side)][0], tail=boneDict['ankle_{}'.format(side)][1], roll=0)
    mstBone.length = mstBone.length*.5
    # def bones
    for i, bone in enumerate(boneDict.keys()):
        if i < 2:
            head = boneDict[bone][0]
            tail = boneDict[bone][1]
            bone = utils.addBone(arm, name='def.{}.{}.001'.format(bone.split('_')[0], side), head=head, tail=tail, roll=0)
            defBones.append(bone)
    # con bones
    for eBone in defBones:
        conBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','con'), scale = 1) 
        conBones.append(conBone)
    # hlp bones
    for eBone in defBones:
        hlpBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','hlp'), scale = .5) 
        hlpBones.append(hlpBone)
    # hlp switch bones
    for eBone in defBones:
        baseName = eBone.name.split('.')[1] 
        hlpSwitchBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','hlp').replace(baseName, baseName+'_switch'), scale = .4) 
        hlpSwitchBones.append(hlpSwitchBone)
    # ikm bones
    for eBone in defBones:
        ikmBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','ikm'), scale = .6) 
        ikmBones.append(ikmBone) 
    # ikm pivot bones
    ikmHeelPivot = utils.addBone(arm, name='ikm.heel_pivot.{}.001'.format(side), head=boneDict['heel_pivot_{}'.format(side)][0], tail=boneDict['toe_pivot_{}'.format(side)][0], roll=0)
    ikmToePivot = utils.addBone(arm, name='ikm.toe_pivot.{}.001'.format(side), head=boneDict['toe_{}'.format(side)][1], tail=boneDict['toe_{}'.format(side)][0], roll=0)
    ikmAnklePivot = utils.addBone(arm, name='ikm.ankle_pivot.{}.001'.format(side), head=boneDict['ankle_{}'.format(side)][1], tail=boneDict['ankle_{}'.format(side)][0], roll=0)
    ikmInnerPivot = utils.addBone(arm, name='ikm.inner_pivot.{}.001'.format(side), head=boneDict['inner_pivot_{}'.format(side)][0], tail=boneDict['inner_pivot_{}'.format(side)][1], roll=0)
    ikmOuterPivot = utils.addBone(arm, name='ikm.outer_pivot.{}.001'.format(side), head=boneDict['outer_pivot_{}'.format(side)][0], tail=boneDict['outer_pivot_{}'.format(side)][1], roll=0)
    for i in [ikmAnklePivot, ikmToePivot, ikmHeelPivot, ikmInnerPivot,  ikmOuterPivot]:
        ikmPivots.append(i)

    # fk controls
    for eBone in defBones:
        baseName = eBone.name.split('.')[1] 
        fkBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','ctl').replace(baseName, baseName+'_fk'), scale = 1) 
        fkBones.append(fkBone)

        fkSubBone = utils.duplicate_bone(arm, eBone, eBone.name.replace('def','ctl').replace(baseName, baseName+'_fk_sub'), scale = .75) 
        fkSubBones.append(fkSubBone)

    # ik controls heel_control
    ikHeelControl = utils.addBone(arm, name='ctl.heel_control.{}.001'.format(side), head=boneDict['heel_control_{}'.format(side)][0], tail=boneDict['heel_control_{}'.format(side)][1], roll=0)
    ikheelPivot = utils.addBone(arm, name='ctl.heel_pivot.{}.001'.format(side), head=boneDict['heel_pivot_{}'.format(side)][0], tail=boneDict['heel_pivot_{}'.format(side)][1], roll=0)
    iktoePivot = utils.addBone(arm, name='ctl.toe_pivot.{}.001'.format(side), head=boneDict['toe_pivot_{}'.format(side)][1], tail=boneDict['toe_pivot_{}'.format(side)][0], roll=0)
    ikToe = utils.addBone(arm, name='ctl.toe_ik.{}.001'.format(side), head=boneDict['toe_{}'.format(side)][0], tail=boneDict['toe_{}'.format(side)][1], roll=0)
    ikBallPivot = utils.addBone(arm, name='ctl.ball_pivot.{}.001'.format(side), head=boneDict['ball_pivot_{}'.format(side)][0], tail=boneDict['ball_pivot_{}'.format(side)][1], roll=0)
    ikInner = utils.addBone(arm, name='ctl.inner_pivot.{}.001'.format(side), head=boneDict['inner_pivot_{}'.format(side)][0], tail=boneDict['inner_pivot_{}'.format(side)][1], roll=0)
    ikOuter = utils.addBone(arm, name='ctl.outer_pivot.{}.001'.format(side), head=boneDict['outer_pivot_{}'.format(side)][0], tail=boneDict['outer_pivot_{}'.format(side)][1], roll=0)
    ikheelRaiseTail = (boneDict['toe_{}'.format(side)][0][0], boneDict['ankle_{}'.format(side)][0][1], boneDict['toe_{}'.format(side)][0][2])
    ikheelRaise = utils.addBone(arm, name='ctl.heel_raise.{}.001'.format(side), head=boneDict['toe_{}'.format(side)][0], tail=ikheelRaiseTail, roll=0)
    ikFootTail = (boneDict['ankle_{}'.format(side)][0][0], boneDict['ankle_{}'.format(side)][0][1]-.5, boneDict['ankle_{}'.format(side)][0][2])
    ikFoot = utils.addBone(arm, name='ctl.foot_ik.{}.001'.format(side), head=boneDict['ankle_{}'.format(side)][0], tail=ikFootTail, roll=0)
    ikFootSub = utils.duplicate_bone(arm, ikFoot, ikFoot.name.replace(ikFoot.name.split('.')[1], ikFoot.name.split('.')[1]+'_sub'), scale = .6) 
    for i in [ikHeelControl, ikheelPivot, iktoePivot, ikToe, ikBallPivot, ikInner, ikOuter, ikheelRaise, ikFoot, ikFootSub]:
        ikControls.append(i)
    
    #property control
    legControl = utils.addBone(arm, name='ctl.leg_controls.{}.001'.format(side), head=boneDict['leg_control_{}'.format(side)][0], tail=boneDict['leg_control_{}'.format(side)][1], roll=0)
    
    defBoneNames = [bone.name for bone in defBones]
    conBonesNames = [bone.name for bone in conBones]
    hlpBoneNames = [bone.name for bone in hlpBones]
    mstBoneName = mstBone.name
    fkBonesNames = [bone.name for bone in fkBones]
    hlpSwitchBoneNames = [bone.name for bone in hlpSwitchBones]
    hlpBonesName = [bone.name for bone in hlpBones]
    mstBonename = mstBone
    ikmBoneNames = [bone.name for bone in ikmBones]
    ikmPivotNames = [bone.name for bone in ikmPivots]
    ikControlNames = [bone.name for bone in ikControls]
    fkBoneNames = [bone.name for bone in fkBones]
    fkSubBoneNames = [bone.name for bone in fkSubBones]
    legControlName = legControl.name
    mstBoneName = mstBone
    ikHeelControlName =ikHeelControl.name
    ikheelPivotName = ikheelPivot.name
    iktoePivotName = iktoePivot.name
    ikToeName = ikToe.name
    ikBallPivotName = ikBallPivot.name
    ikInnerName = ikInner.name
    ikOuterName = ikOuter.name
    ikheelRaiseName = ikheelRaise.name
    ikFootName = ikFoot.name
    ikFootSubName = ikFootSub.name
    ikmAnklePivotName = ikmAnklePivot.name
    ikmToePivotName = ikmToePivot.name
    ikmHeelPivotName = ikmHeelPivot.name
    ikmInnerPivotName = ikmInnerPivot.name
    ikmOuterPivotName = ikmOuterPivot.name

    
    # set bone layers
    # def
    for bone in defBones:
        bone.layers[utils.boneLayerDict['def']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # con
    for bone in conBones:
        bone.layers[utils.boneLayerDict['con']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # hlp
    for bone in hlpBones + hlpSwitchBones:
        bone.layers[utils.boneLayerDict['hlp']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # fk controls
    for bone in fkBones + fkSubBones:
        bone.layers[utils.boneLayerDict['fk']] = True
        bone.layers[utils.boneLayerDict['god']] = False 
    # ik controls
    for bone in ikControls:
        bone.layers[utils.boneLayerDict['ik']] = True
        bone.layers[utils.boneLayerDict['god']] = False 
    # ikmPivots
    for bone in ikmPivots + ikmBones:
        bone.layers[utils.boneLayerDict['ikm']] = True
        bone.layers[utils.boneLayerDict['god']] = False
    # legControl
    legControl.layers[utils.boneLayerDict['ik']] = True
    legControl.layers[utils.boneLayerDict['fk']] = True
    legControl.layers[utils.boneLayerDict['god']] = False
    # mstBone
    mstBone.layers[utils.boneLayerDict['mst']] = True
    mstBone.layers[utils.boneLayerDict['god']] = False

    # parent bones
    # def
    utils.parent_bone_chain(defBones, connected=True) 
    defBones[0].parent = mstBone
    # con
    utils.parent_bone_chain(conBones, connected=False) 
    conBones[0].parent = mstBone
    # hlp
    utils.parent_bone_chain(hlpBones, connected=False) 
    hlpBones[0].parent = mstBone
    # hlpSwitchBones
    utils.parent_bone_chain(hlpSwitchBones, connected=False) 
    hlpSwitchBones[0].parent = mstBone
    # fkBones
    i = 0
    for main, sub in zip(fkBones, fkSubBones):
        sub.parent = main
    for i, ctl in enumerate(fkBones):
        if i is not 0:
            ctl.parent = fkSubBones[i-1]
        else:
            ctl.parent = mstBone
    # ik controls
    iktoePivot.parent = ikInner
    ikInner.parent = ikOuter
    ikOuter.parent = ikBallPivot
    ikBallPivot.parent = ikheelPivot
    ikheelPivot.parent = ikFootSub
    ikheelRaise.parent = ikFootSub
    ikHeelControl.parent = ikFootSub
    ikFootSub.parent = ikFoot
    ikFoot.parent = mstBone
    ikToe.parent = ikmToePivot

    # ikmPivots
    ikmAnklePivot.parent = ikmToePivot
    ikmToePivot.parent = ikmHeelPivot
    ikmHeelPivot.parent = ikmInnerPivot
    ikmInnerPivot.parent = ikmOuterPivot
    ikmOuterPivot.parent = ikToe

    # ikm
    i = 0
    for parent, child in zip(ikmPivots, ikmBones):
        if i < 2:
            child.parent = parent

    # legControl
    legControl.parent = hlpSwitchBones[-1]

    bpy.ops.object.mode_set(mode='POSE')
    # custom properties
    utils.add_custom_property_to_pose_bone(arm, boneName=legControlName, propertyName="IKFK_switch", default=1.0, min=0.0, max=1.0 )
    utils.add_custom_property_to_pose_bone(arm, boneName=ikHeelControlName, propertyName="foot_roll_liimit", default=30.0, min=-180.0, max=180.0 )
    
    # constrain joints
    # def
    for boneName, target in zip(defBoneNames, conBonesNames):
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = target

    # con
    for boneName, target in zip(conBonesNames, hlpSwitchBoneNames):
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.subtarget = target

    # hlp
    for i, boneName in enumerate(hlpSwitchBoneNames):
        pBone =  arm.pose.bones[boneName]
        #FK copy transforms
        copyTrans = pBone.constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.name = 'Fk Copy Transforms'
        copyTrans.subtarget = fkSubBoneNames[i]
        #IK copy transforms
        copyTrans = arm.pose.bones[boneName].constraints.new('COPY_TRANSFORMS')
        copyTrans.target = arm
        copyTrans.name = 'Ik Copy Transforms'
        copyTrans.subtarget = ikmBoneNames[i]
        # IK copy transforms driver   
        drv = utils.add_driver(pBone.constraints['{}'.format(copyTrans.name)], 'influence', func = 'var')
        utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.leg_controls.{}.001"]["IKFK_switch"]'.format(side))

    #ikm pivots
    subTarget = ikHeelControlName

    boneName = ikmHeelPivotName
    transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM')
    transformCon.name = 'Transformation Foot Roll'
    transformCon.target = arm
    transformCon.subtarget = subTarget 
    transformCon.use_motion_extrapolate = False
    transformCon.owner_space = 'LOCAL'  
    transformCon.target_space = 'LOCAL' 
    transformCon.map_from = 'ROTATION'
    transformCon.map_to = 'ROTATION' 
    transformCon.from_min_x_rot = radians(-180)
    transformCon.from_max_x_rot = radians(0)
    transformCon.to_min_x_rot = radians(180)
    transformCon.to_max_x_rot = radians(0)

    pBone = arm.pose.bones[ikmToePivotName] 
    transformCon = pBone.constraints.new('TRANSFORM')
    transformCon.name = 'Transformation Foot Roll'
    transformCon.target = arm
    transformCon.subtarget = subTarget
    transformCon.use_motion_extrapolate = False
    transformCon.owner_space = 'LOCAL'  
    transformCon.target_space = 'LOCAL' 
    transformCon.map_from = 'ROTATION'
    transformCon.map_to = 'ROTATION' 
    transformCon.from_max_x_rot = radians(180)
    transformCon.to_max_x_rot = radians(180)
    #from_min_x driver
    drv = utils.add_driver(pBone.constraints['{}'.format(transformCon.name)], 'from_min_x_rot', func = 'var*pi/180')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.heel_control.{}.001"]["foot_roll_limit"]'.format(side))
    
    pBone = arm.pose.bones[ikmAnklePivotName] 
    transformCon = pBone.constraints.new('TRANSFORM')
    transformCon.name = 'Transformation Foot Roll'
    transformCon.target = arm
    transformCon.subtarget = subTarget 
    transformCon.use_motion_extrapolate = False
    transformCon.owner_space = 'LOCAL'  
    transformCon.target_space = 'LOCAL' 
    transformCon.map_from = 'ROTATION'
    transformCon.map_to = 'ROTATION' 
    # from_max_x driver
    drv = utils.add_driver(pBone.constraints['{}'.format(transformCon.name)], 'from_max_x_rot', func = 'var*pi/180')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.heel_control.{}.001"]["foot_roll_limit"]'.format(side))
    # to_max_x driver
    drv = utils.add_driver(pBone.constraints['{}'.format(transformCon.name)], 'to_max_x_rot', func = 'var*pi/180')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.heel_control.{}.001"]["foot_roll_limit"]'.format(side))

    transformCon = pBone.constraints.new('TRANSFORM')
    transformCon.name = 'Transformation Foot Roll Second'
    transformCon.target = arm
    transformCon.subtarget = subTarget
    transformCon.use_motion_extrapolate = False
    transformCon.owner_space = 'LOCAL'  
    transformCon.target_space = 'LOCAL' 
    transformCon.map_from = 'ROTATION'
    transformCon.map_to = 'ROTATION' 
    # from_min_x driver
    drv = utils.add_driver(pBone.constraints['{}'.format(transformCon.name)], 'from_min_x_rot', func = 'var*pi/180')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.heel_control.{}.001"]["foot_roll_limit"]'.format(side))
    # from_max_x driver
    drv = utils.add_driver(pBone.constraints['{}'.format(transformCon.name)], 'from_max_x_rot', func = '(var+60)*pi/180')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.heel_control.{}.001"]["foot_roll_limit"]'.format(side))
    # to_max_x driver
    drv = utils.add_driver(pBone.constraints['{}'.format(transformCon.name)], 'to_max_x_rot', func = '(-var)*pi/180')
    utils.add_driver_variable(drv, varName='var', target=arm, dataPath='pose.bones["ctl.heel_control.{}.001"]["foot_roll_limit"]'.format(side))

    transformCon = pBone.constraints.new('TRANSFORM')
    transformCon.name = 'Transformation Heel Raise'
    transformCon.target = arm
    transformCon.subtarget = ikheelRaiseName
    transformCon.use_motion_extrapolate = False
    transformCon.owner_space = 'LOCAL'  
    transformCon.target_space = 'LOCAL' 
    transformCon.map_from = 'ROTATION'
    transformCon.map_to = 'ROTATION' 
    transformCon.from_min_x_rot = radians(-180)
    transformCon.from_min_y_rot = radians(-180) 
    transformCon.from_min_z_rot = radians(-180) 
    transformCon.to_min_x_rot = radians(-180) 
    transformCon.to_min_y_rot = radians(-180)
    transformCon.to_min_z_rot = radians(-180)
    transformCon.from_max_x_rot = radians(180)
    transformCon.from_max_y_rot = radians(180)
    transformCon.from_max_z_rot = radians(180)
    transformCon.to_max_x_rot = radians(180)
    transformCon.to_max_y_rot = radians(180)
    transformCon.to_max_z_rot = radians(180)

    boneName = ikmInnerPivotName
    transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM')
    transformCon.name = 'Transformation Foot Roll'
    transformCon.target = arm
    transformCon.subtarget = subTarget
    transformCon.use_motion_extrapolate = False
    transformCon.owner_space = 'LOCAL'  
    transformCon.target_space = 'LOCAL' 
    transformCon.map_from = 'ROTATION'
    transformCon.map_to = 'ROTATION' 
    transformCon.from_min_y_rot = radians(-180)
    transformCon.to_min_y_rot = radians(180)

    boneName = ikmOuterPivotName
    transformCon = arm.pose.bones[boneName].constraints.new('TRANSFORM')
    transformCon.name = 'Transformation Foot Roll'
    transformCon.target = arm
    transformCon.subtarget = subTarget
    transformCon.use_motion_extrapolate = False
    transformCon.owner_space = 'LOCAL'  
    transformCon.target_space = 'LOCAL' 
    transformCon.map_from = 'ROTATION'
    transformCon.map_to = 'ROTATION' 
    transformCon.from_max_y_rot = radians(180)
    transformCon.to_max_y_rot = radians(-180)

    bpy.ops.object.mode_set(mode='OBJECT')
class FootGuides(component.CreateGuides):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "guide.foot"
    bl_label = "Foot Guides"

    componentParent = ''#parent guide
    guideInfoDict = {} #tag:[world matrix, parent, guide shape, def/hlp]
        
    def execute(self, context):
        boneDict = boneDict = utils.get_bone_dict_data(fileName='foot_guide_data.json') 
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
            utils.addBone(arm, name=name, head=head, tail=tail, roll=roll)
            utils.add_custom_property_to_pose_bone(arm, boneName=name, propertyName="Component", default='foot' )


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

class BUILD_OT_Foot(Operator):
    """Creates operator for drop-down menu of rig components and templates"""
    bl_idname = "build.foot"
    bl_label = "Foot Build"


    def execute(self, context):
        build('L')
        boneNames = [bone.name for bone in bpy.data.armatures['guideArmature'].bones]
        if 'ankle_R' in boneNames:
            build('R')
        return {"FINISHED"}



classes = [FootGuides, BUILD_OT_Foot]