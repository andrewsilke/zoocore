from maya.api import OpenMaya as om2

from zoo.libs.maya.meta import base
from zoo.libs.maya.api import attrtypes, nodes


class MetaCamera(base.MetaBase):
    def __init__(self, node=None, name=None, initDefaults=True):
        super(MetaCamera, self).__init__(node, name, initDefaults)
        child = list(nodes.iterChildren(self.mobject(), False, om2.MFn.kCamera))
        self.camMfn = om2.MFnCamera(child[0])

    def _initMeta(self):
        super(MetaCamera, self)._initMeta()
        self.addAttribute("isCamera", True, attrtypes.kMFnNumericBoolean)
        self.addAttribute("startFrame", 0, attrtypes.kMFnNumericInt)
        self.addAttribute("endFrame", 0, attrtypes.kMFnNumericInt)
        self.addAttribute("framePadding", 10, attrtypes.kMFnNumericInt)
        self.addAttribute("shotName", "", attrtypes.kMFnDataString)
        self.addAttribute("camera_version", 1, attrtypes.kMFnNumericInt)

    @property
    def aspectRatio(self):
        return self.camMfn.aspectRatio()

    @aspectRatio.setter
    def aspectRatio(self, value):
        self.camMfn.setAspectRatio(value)

    @property
    def focalLength(self):
        return self.camMfn.focalLength

    @focalLength.setter
    def focalLength(self, value):
        self.camMfn.focalLength = value

    @property
    def verticalFilmAperture(self):
        return self.camMfn.verticalFilmAperture

    @verticalFilmAperture.setter
    def verticalFilmAperture(self, value):
        self.camMfn.verticalFilmAperture = value

    @property
    def horizontalFilmAperture(self):
        return self.camMfn.horizontalFilmAperture

    @horizontalFilmAperture.setter
    def horizontalFilmAperture(self, value):
        self.camMfn.horizontalFilmAperture = value

    @property
    def filmFit(self):
        return self.camMfn.filmFit

    @filmFit.setter
    def filmFit(self, value):
        self.camMfn.filmFit = int(value)

    def copyFrom(self, metaCamera):
        self.lockedOff = metaCamera.lockedOff.asBool()
        self.startFrame = metaCamera.startFrame.asInt()
        self.endFrame = metaCamera.endFrame.asInt()
        self.framePadding = metaCamera.framePadding.asInt()
        self.shotName = metaCamera.shotName.asString()
        self.camera_version = metaCamera.camera_version.asInt()
        self.shotgun_context = metaCamera.shotgun_context.asString()
        self.filmFit = float(metaCamera.filmFit)
        self.aspectRatio = float(metaCamera.aspectRatio)
        self.focalLength = float(metaCamera.focalLength)
        self.verticalFilmAperture = float(metaCamera.verticalFilmAperture)

