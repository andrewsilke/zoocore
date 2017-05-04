import contextlib

from maya import cmds, mel
from maya.api import OpenMaya as om2
from zoo.libs.maya.api import nodes
from zoo.libs.maya.api import plugs


@contextlib.contextmanager
def exportContext(rootNode):
    changed = []
    for i in nodes.iterChildren(rootNode, recursive=True):
        dp = om2.MFnDependencyNode(i)
        plug = dp.findPlug("visibility", False)
        with plugs.setLockedContext(plug):
            if plug.asFloat() != 1.0:
                plugs.setAttr(plug, 1.0)
                changed.append(dp)
    yield
    for i in iter(changed):
        plug = i.findPlug("visibility", False)
        with plugs.setLockedContext(plug):
            plugs.setAttr(plug, 0.0)


def exportAbc(filePath, sceneNode):
    command = "-frameRange 1 1 -uvWrite -writeVisibility -writeCreases -writeUVSets -dataFormat ogawa -file {}".format(
        filePath)
    command += " -root {}".format(sceneNode)
    cmds.AbcExport(j=command)


def exportObj(filePath, sceneNode):
    cmds.select(sceneNode)
    cmds.file(filePath, force=True, options="groups=0;ptgroups=0;materials=0;smoothing=1;normals=1", typ="OBJexport",
              pr=True,
              es=True)
    cmds.select(cl=True)


def importFbx(filepath):
    mel.eval("FBXImportMode -v Exmerge")
    mel.eval("FBXImportMergeAnimationLayers -v false")
    mel.eval("FBXImportProtectDrivenKeys -v false")
    mel.eval("FBXImportConvertDeformingNullsToJoint -v false")
    mel.eval("FBXImportMergeBackNullPivots -v false")
    mel.eval("FBXImportSetLockedAttribute -v true")
    mel.eval("FBXImportConstraints -v false")
    mel.eval("FBXImportLights -v false")
    mel.eval("FBXImportCameras -v false")
    mel.eval("FBXImportHardEdges -v true")
    mel.eval("FBXImportShapes -v true")
    mel.eval("FBXImportUnlockNormals -v true")
    mel.eval('FBXImport -f "{}"'.format(filepath.replace("\\", "/")))  # stupid autodesk and there mel crap


def exportFbx(filePath, sceneNode):
    with exportContext(nodes.asMObject(sceneNode)):
        mel.eval("FBXExportSmoothingGroups -v true")
        mel.eval("FBXExportHardEdges -v true")
        mel.eval("FBXExportTangents -v true")
        mel.eval("FBXExportSmoothMesh -v true")
        mel.eval("FBXExportInstances -v true")
        # Animation
        mel.eval("FBXExportBakeComplexAnimation -v false")
        mel.eval("FBXExportUseSceneName -v false")
        mel.eval("FBXExportQuaternion -v euler")
        mel.eval("FBXExportShapes -v true")
        mel.eval("FBXExportSkins -v false")
        mel.eval("FBXExportConstraints -v false")
        mel.eval("FBXExportCameras -v false")
        mel.eval("FBXExportLights -v false")
        mel.eval("FBXExportEmbeddedTextures -v false")
        mel.eval("FBXExportInputConnections -v false")
        mel.eval("FBXExportUpAxis y")
        cmds.select(sceneNode)
        mel.eval('FBXExport -f "{}" -s'.format(filePath.replace("\\", "/")))
        cmds.select(cl=True)