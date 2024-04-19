# LSystemInstancerNode.py

import sys
import random

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

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
kPluginNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    inNumPoints = OpenMaya.MObject()

    minX = OpenMaya.MObject()
    minY = OpenMaya.MObject()
    minZ = OpenMaya.MObject()
    maxX = OpenMaya.MObject()
    maxY = OpenMaya.MObject()
    maxZ = OpenMaya.MObject()

    minVec = OpenMaya.MObject()
    maxVec = OpenMaya.MObject()

    outPoints = OpenMaya.MObject()
    
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        # TODO:: create the main functionality of the node. Your node should 
        #         take in three floats for max position (X,Y,Z), three floats 
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData 
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData. 
        # rewrite this function
        if plug == randomNode.outPoints:
            
            inNumPointsData = data.inputValue(randomNode.inNumPoints)
            inNumPointsValue = inNumPointsData.asInt()
            
            minVecData = data.inputValue(randomNode.minVec)
            minVecDataValue = minVecData.asDouble3()
            maxVecData = data.inputValue(randomNode.maxVec)
            maxVecDataValue = maxVecData.asDouble3()

            pointsData = data.outputValue(randomNode.outPoints)
            pointsAAD = OpenMaya.MFnArrayAttrsData()
            pointsObject = pointsAAD.create()
            
            positionArray = pointsAAD.vectorArray("position")
            idArray = pointsAAD.doubleArray("id")
            
            for index in range(inNumPointsValue):
                ranX = random.uniform(minVecDataValue[0], maxVecDataValue[0])
                ranY = random.uniform(minVecDataValue[1], maxVecDataValue[1])
                ranZ = random.uniform(minVecDataValue[2], maxVecDataValue[2])
                
                newPos = OpenMaya.MVector(ranX, ranY, ranZ)
                positionArray.append(newPos)
                idArray.append(index)
            
            pointsData.setMObject(pointsObject)

        data.setClean(plug)
    
# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    randomNode.inNumPoints = nAttr.create("numPoints", "n", OpenMaya.MFnNumericData.kInt, 15)
    MAKE_INPUT(nAttr)

    randomNode.minX = nAttr.create("minX", "minx", OpenMaya.MFnNumericData.kDouble, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxX = nAttr.create("maxX", "maxx", OpenMaya.MFnNumericData.kDouble, 3.0)
    MAKE_INPUT(nAttr)
    randomNode.minY = nAttr.create("minY", "miny", OpenMaya.MFnNumericData.kDouble, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxY = nAttr.create("maxY", "maxy", OpenMaya.MFnNumericData.kDouble, 3.0)
    MAKE_INPUT(nAttr)
    randomNode.minZ = nAttr.create("minZ", "minz", OpenMaya.MFnNumericData.kDouble, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxZ = nAttr.create("maxZ", "maxz", OpenMaya.MFnNumericData.kDouble, 3.0)
    MAKE_INPUT(nAttr)
    randomNode.minVec = nAttr.create("minVec", "minvec", randomNode.minX, randomNode.minY, randomNode.minZ)
    MAKE_INPUT(nAttr)
    randomNode.maxVec = nAttr.create("maxVec", "maxvec", randomNode.maxX, randomNode.maxY, randomNode.maxZ)
    MAKE_INPUT(nAttr)

    randomNode.outPoints = tAttr.create("outPoints", "op", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print("Initialization!\n")

        randomNode.addAttribute(randomNode.inNumPoints)
        randomNode.addAttribute(randomNode.minVec)
        randomNode.addAttribute(randomNode.maxVec)
        randomNode.addAttribute(randomNode.outPoints)

        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.minVec, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.maxVec, randomNode.outPoints)

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
