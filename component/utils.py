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
import json
import os

boneLayerDict = {
    'def':31,
    'con':30,
    'helpTwist':29,
    'hlp':28,
    'hlpStretch':27,
    'ikm':26,
    'prt':25,
    'mst':24,
    'att':15,
    'tweak':3,
    'ik':2,
    'fk':1,
    'god':0
    }
    
def addBone(armature, name='Bone', head=(0,0,0), tail=(0,0,1), roll=0):
    """
    Creates bone under determined armature
    """
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    armature.data.edit_bones.new(name)
    eb = armature.data.edit_bones[name]
    eb.head = head
    eb.tail = tail
    eb.roll = roll

    return armature.data.edit_bones[name]

def create_build_rig():
    #create build rig. deletes existing build rig if it already exists
    # delete existing build rig
    bpy.ops.object.mode_set(mode='OBJECT')
    if 'buildArmature' in bpy.data.objects:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['buildArmature'].select_set(True)
        bpy.ops.object.delete()

    #create new build rig
    bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    arm = bpy.data.objects['Armature']
    #delete base bone
    arm.data.edit_bones.remove( arm.data.edit_bones['Bone'])
    #rename armature
    arm.name = 'buildArmature'
    arm.data.name = 'buildArmature'
    bpy.ops.object.mode_set(mode='OBJECT')

    return arm

def find_in_betweeen_point(point1 = (0,0,0), point2 = (0,0,0), numerator=5., denominator=.5):
    newPoint = []
    for axis1, axis2 in zip(point1, point2):
        qAxis = (axis1*numerator +axis2*denominator)
        newPoint.append(qAxis)

    return newPoint

def duplicate_bone(armature, editBone, name, scale=1):
    #returns duplicated edit bone
    eBone = addBone(armature, name=name, head=editBone.head, tail=editBone.tail, roll=editBone.roll)
    eBone.length = eBone.length*scale

    return eBone

def get_bone_location(armature, bone=''):
    #returns head location of bone
    mode =  bpy.context.mode
    armature.select_set(True)
    head = armature.pose.bones[bone].head
    tail = armature.pose.bones[bone].tail
    bpy.ops.object.mode_set(mode='EDIT')
    roll = armature.data.edit_bones[bone].roll
    bpy.ops.object.mode_set(mode=mode)

    return  (head, tail, roll)

def parent_bone_chain(chain = [], connected = False):
    for i in range(0, len(chain)-1):
        parent = chain[i]
        child = chain[i+1]
        child.parent = parent
        if connected == True:
            child.use_connect = True
        else:
            child.use_connect = False

def add_driver(source, prop, func = '', index=-1):
    ''' Add driver to source prop '''
    # add driver
    if index != -1:
        drv = source.driver_add( prop, index ).driver
    else:
        drv = source.driver_add( prop ).driver
    # driver expression
    drv.expression = func
    return drv

def add_driver_variable(drv, varName='', target=None, dataPath=''):
    ''' Add variable to defined driver '''
    var = drv.variables.new()
    var.name                 = varName
    var.targets[0].id        = target
    var.targets[0].data_path = dataPath

def add_driver_transform_variable(drv, varName='', target=None, bone_target='', transform_type='SCALE_Y', transform_space = 'LOCAL_SPACE'):
    ''' Add variable to defined driver '''
    var = drv.variables.new()
    var.type                        = 'TRANSFORMS'
    var.name                        = varName
    var.targets[0].id               = target
    var.targets[0].bone_target      = bone_target 
    var.targets[0].transform_type   = transform_type
    var.targets[0].transform_space  = transform_space

def add_driver_rotation_diff_variable(drv, varName='', target=None, bone_target1=None, bone_target2=None):
    var = drv.variables.new()
    var.type                    = 'ROTATION_DIFF'
    var.name                    = varName
    var.targets[0].id           = target
    var.targets[1].id           = target
    var.targets[0].bone_target  = bone_target1
    var.targets[1].bone_target  = bone_target2

    var.type = 'ROTATION_DIFF'
def add_custom_property_to_pose_bone(armature, boneName='', propertyName='', default=0, min=0, max=1 ):
    ''' Add custom property '''
    current_mode = bpy.context.object.mode
    if current_mode !='POSE':
        bpy.ops.object.mode_set(mode='POSE')
    pbone = armature.pose.bones[boneName]
    pbone[propertyName] = default
    '''
    if "_RNA_UI" not in pbone.keys():
            pbone["_RNA_UI"] = {}
    '''
    if isinstance(default, str) == False:
        manager = pbone.id_properties_ui(propertyName)
        manager.update(min=min, max=max)
    '''
        pbone["_RNA_UI"].update({propertyName: {"min":min, "max":max}})
        bpy.context.object.pose.bones[boneName][propertyName] = default
    else:
        pbone["_RNA_UI"].update({propertyName: {"min":min, "max":max}})
        bpy.context.object.pose.bones[boneName][propertyName] = default
    '''
    bpy.ops.object.mode_set(mode=current_mode)

    return pbone[propertyName]

def get_bone_dict_data(fileName=''):
    '''
    Returns bone dictionary data of defined json file
    '''
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filePath = os.path.join(__location__, fileName)
    with open(filePath) as json_file:
        boneDict = json.load(json_file)
    return boneDict

def apply_bone_custom_shapes(fileName=''):
    '''
    Reads custom bone shape json and applies data
    '''
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filePath = os.path.join(__location__, fileName)
    with open(filePath) as json_file:
        boneDict = json.load(json_file)
    arm =bpy.context.object.pose
    for boneName in boneDict.keys():
        try:
            arm.bones[boneName].custom_shape = bpy.data.objects[boneDict[boneName]]
        except:
            print(boneName+' does not have a shape')

def import_shapes():
    '''
    append all objects ending with '.shape'
    '''
    objNames = [obj.name for obj in bpy.data.objects]
    if 'Shapes' not in objNames:
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        filePath = os.path.join(__location__, 'shapes.blend')

        with bpy.data.libraries.load(filePath) as (data_from, data_to):
            files = []
            for obj in data_from.objects:
                files.append({'name' : obj})
            bpy.ops.wm.append(directory=filePath+'\\Object\\', files=files)
        for obj in bpy.data.objects:
            if obj.name.endswith('.shape'):
                bpy.data.objects[obj.name].hide_viewport = True

class UTILS_OT_mirror(Operator):
    """Mirror Giudes"""
    bl_idname = "utils.mirror"
    bl_label = "Mirror Guides"

    def execute(self, context):
        # check if object is an armature
        arm = bpy.context.active_object
        if arm.type == 'ARMATURE':
            current_mode = bpy.context.object.mode
            # mirror all edit bones with the suffix L
            boneList = [bone.name for bone in bpy.context.object.data.bones]
            for boneName in  boneList:
                bpy.ops.object.mode_set(mode='EDIT')
                editBone = arm.data.edit_bones[boneName]
                poseBone = arm.pose.bones[boneName]
                boneName = editBone.name
                if "_L" in boneName:           
                    mirrorName = boneName.replace('_L', '_R')
                    dupBone = duplicate_bone(arm, editBone, name=mirrorName)
                    dupName = dupBone.name
                    dupBone.tail = (-1*poseBone.tail[0], poseBone.tail[1], poseBone.tail[2])
                    dupBone.head = (-1*poseBone.head[0], poseBone.head[1], poseBone.head[2])
                    dupBone.roll = dupBone.roll*-1
                    bpy.ops.object.mode_set(mode='POSE')
                    bpy.context.object.pose.bones[mirrorName].custom_shape = bpy.data.objects['guide.shape']
                    propSetting = arm.pose.bones[boneName]['Component']
                    add_custom_property_to_pose_bone(arm, boneName=dupName, propertyName="Component", default=propSetting)
                # return to previous mode
            bpy.ops.object.mode_set(mode=current_mode)
        else:
            print('Please select an armature')
        return {"FINISHED"}

classes = [UTILS_OT_mirror]