# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random
import LSystem
import math

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import maya.mel as mel

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

# Define the name of the node
kPluginNodeTypeName = "LSystemInstancerNode"

kDefaultStringAttrValue = "F:\Study\Homework\HW3_final\HW3\plants\simple1.txt"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
LSystemInstancerNodeID  = OpenMaya.MTypeId(0x8724)

# Node definition
class LSystemInstancerNode(OpenMayaMPx.MPxNode):
    # Declare class variables:

    angle = OpenMaya.MObject()
    stepSize = OpenMaya.MObject()
    grammarFile = OpenMaya.MObject()
    iterations = OpenMaya.MObject()
    
    outBranches = OpenMaya.MObject()
    outFlowers = OpenMaya.MObject()
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):

        # retrive data 
        angleData = data.inputValue(LSystemInstancerNode.angle)
        stepSizeData = data.inputValue(LSystemInstancerNode.stepSize)
        grammarFileData = data.inputValue(LSystemInstancerNode.grammarFile)
        iterationsData = data.inputValue(LSystemInstancerNode.iterations)

        angleValue = angleData.asDouble()
        stepSizeValue = stepSizeData.asDouble()
        grammarFileValue = grammarFileData.asString()
        iterationsValue = iterationsData.asInt()
       
        # init output data
        outBranchesData = data.outputValue(LSystemInstancerNode.outBranches)
        outBranchesAAD = OpenMaya.MFnArrayAttrsData()
        outBranchesObj = outBranchesAAD.create()
       
        outFlowersData = data.outputValue(LSystemInstancerNode.outFlowers)
        outFlowersAAD = OpenMaya.MFnArrayAttrsData()
        outFlowersObj = outFlowersAAD.create()

        # vectors for pos, id, scale, aim for branches and flowers
        branchPosArr = outBranchesAAD.vectorArray("position")
        branchIDArr = outBranchesAAD.doubleArray("id")
        branchScaleArr = outBranchesAAD.vectorArray("scale")
        branchAimDirArr = outBranchesAAD.vectorArray("aimDirection")

        flowerPosArr = outFlowersAAD.vectorArray("position")
        flowerIDArr = outFlowersAAD.doubleArray("id")

        lsystem = LSystem.LSystem()
        lsystem.loadProgram(str(grammarFileValue))
        lsystem.setDefaultAngle(angleValue)
        lsystem.setDefaultStep(stepSizeValue)

        branches = LSystem.VectorPyBranch()
        flowers = LSystem.VectorPyBranch()

        lsystem.processPy(iterationsValue, branches, flowers)

        # fill branches vector
        for index, branch in enumerate(branches):
            aimDir = OpenMaya.MVector(branch[3] - branch[0], branch[4] - branch[1],  branch[5] - branch[2])
            branchAimDirArr.append(aimDir)

            branchPos = OpenMaya.MVector((branch[3] + branch[0])/2.0, (branch[4] + branch[1])/2.0, (branch[5] + branch[2])/2.0)
            branchPosArr.append(branchPos)

            aimDirlength = math.sqrt(math.pow(branch[3] - branch[0], 2)+ math.pow(branch[5] - branch[2], 2) + math.pow(branch[4] - branch[1], 2))
            branchScaleArr.append(OpenMaya.MVector(aimDirlength, 1.0, 1.0))

            branchIDArr.append(index)
            

        # fill flowers vector
        for index, flower in enumerate(flowers):
            pos = OpenMaya.MVector(flower[0], flower[1], flower[2])      
            flowerPosArr.append(pos)
            flowerIDArr.append(index)

        outBranchesData.setMObject(outBranchesObj)
        outFlowersData.setMObject(outFlowersObj)
        
        data.setClean(plug)
    
# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print("Initialization!\n")
        LSystemInstancerNode.angle = nAttr.create("angle", "a", OpenMaya.MFnNumericData.kDouble, 5.0)
        MAKE_INPUT(nAttr)
        LSystemInstancerNode.stepSize = nAttr.create("stepSize", "ss", OpenMaya.MFnNumericData.kDouble, 5.0)
        MAKE_INPUT(nAttr)
        
        strDefault = OpenMaya.MFnStringData().create(kDefaultStringAttrValue)
        LSystemInstancerNode.grammarFile = tAttr.create("grammarFile", "g", OpenMaya.MFnData.kString, strDefault)
        MAKE_INPUT(nAttr)
        LSystemInstancerNode.iterations = nAttr.create("iterations", "i", OpenMaya.MFnNumericData.kInt, 2)
        MAKE_INPUT(nAttr)
            
        LSystemInstancerNode.outBranches = tAttr.create("outBranches", "ob", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
        MAKE_OUTPUT(tAttr)
        LSystemInstancerNode.outFlowers = tAttr.create("outFlowers", "of", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
        MAKE_OUTPUT(tAttr)

    except:
        sys.stderr.write( ("Failed to create attributes - 1\n") )   

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print("Create io attributes 2!\n")

        LSystemInstancerNode.addAttribute(LSystemInstancerNode.angle)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.stepSize)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.iterations)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.grammarFile)
        
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.outBranches)     
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.outFlowers) 

        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.angle,LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.angle,LSystemInstancerNode.outFlowers) 
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.stepSize,LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.stepSize,LSystemInstancerNode.outFlowers)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.grammarFile,LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.grammarFile,LSystemInstancerNode.outFlowers)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.iterations,LSystemInstancerNode.outBranches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.iterations,LSystemInstancerNode.outFlowers)

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstancerNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, LSystemInstancerNodeID, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )
    
    try:
        UIPath =  mplugin.loadPath() + "/ui.mel"
        UIFileDataStr = ''
        with open(UIPath, 'r') as myfile:
            UIFileDataStr = myfile.read().replace('\n', '')

    except:
        sys.stderr.write( "Failed to UI File\n")

    OpenMaya.MGlobal.executeCommand(UIFileDataStr, False, False)
    
# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( LSystemInstancerNodeID  )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
