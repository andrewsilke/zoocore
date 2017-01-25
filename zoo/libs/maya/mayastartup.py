import os

from zoo.libs.maya.utils import general
from zoo.libs.utils import zlogging

logger = zlogging.zooLogger


class ZooMayaStartUp(object):
    def __init__(self):
        self.startUp()

    def startUp(self):
        ZooMayaStartUp.setupLogger()
        ZooMayaStartUp.setupPlugins()
        ZooMayaStartUp.setupIcons()

    @staticmethod
    def setupPlugins():
        """
        sets up paths for plugins (both binary and python ones) and loads them
        """
        basePaths = os.environ['MAYA_PLUG_IN_PATH'].split(os.pathsep)
        extraPaths = str(os.path.join(os.environ.get("ZOO_BASE", "").split(os.pathsep)[0], "libs", "maya",
                                      'plugins'))
        if extraPaths not in basePaths:
            basePaths.append(extraPaths)
            # Set the plug-in path
            os.environ["MAYA_PLUG_IN_PATH"] = os.pathsep.join(basePaths)
        general.loadPlugin("zooundo.py")

    @staticmethod
    def setupIcons():
        """
        sets up paths for icons
        """
        basePaths = os.environ['XBMLANGPATH'].split(os.pathsep)
        icons = str(os.path.join(os.environ.get("ZOO_BASE", "").split(os.pathsep)[0], 'icons'))
        if icons not in basePaths:
            basePaths.append(icons)
            os.environ['XBMLANGPATH'] = os.pathsep.join(basePaths)

    @staticmethod
    def setupLogger():
        zlogging.CentralLogManager()
