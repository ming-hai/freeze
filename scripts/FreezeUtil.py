# **********************************************************************
#
# Copyright (c) 2003-2018 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

import os, sys
from Util import *

toplevel = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TransformDB(SimpleClient):

    def __init__(self):
        SimpleClient.__init__(self, exe="transformdb", quiet=True)

class FreezeCppMapping(CppMapping):

    def getNugetPackage(self, compiler, version):
        return "zeroc.freeze.{0}.{1}".format(compiler, version)

    def getCommandLine(self, current, process, exe):
        if isinstance(process, TransformDB):
            return os.path.join(current.driver.getInstallDir(self, current, "FREEZE_HOME", "FREEZE_BIN_DIST"),
                                platform.getBinSubDir(self, process, current),
                                exe)
        else:
            return CppMapping.getCommandLine(self, current, process, exe)

    def getEnv(self, process, current):
        env = CppMapping.getEnv(self, process, current)
        if isinstance(platform, Windows):
            env["PATH"] += "{}{}".format(os.pathsep, Mapping.getByName("ice/cpp").getLibDir(process, current))
        return env

class FreezeJavaMapping(JavaCompatMapping):

    def getJavaArgs(self, process, current):
        if process.isFromBinDir():
            return []
        return ["-Djava.library.path={0}".format(self.getBerkeleyDB(process, current))]

    def getEnv(self, process, current):
        env = JavaCompatMapping.getEnv(self, process, current)
        if isinstance(platform, Windows):
            env["PATH"] = self.getBerkeleyDB(process, current) + ((os.pathsep + env["PATH"]) if "PATH" in env else "")
        return env

    def getBerkeleyDB(self, process, current):
        if isinstance(platform, Darwin):
            if os.path.exists("/usr/local/opt/ice/libexec/lib"):
                return "/usr/local/opt/ice/libexec/lib"
            else:
                return "/usr/local/opt/berkeley-db@5.3/lib"
        elif isinstance(platform, Windows):
            return os.path.join(toplevel, "java", "packages", "berkeley.db.java7.5.3.28.1", "build", "native", "bin",
                                current.config.buildPlatform)
        else:
            return "/usr/{0}".format("lib/x86_64-linux-gnu" if platform.linuxId in ["ubuntu", "debian"] else "lib64")

Mapping.mappings.clear()
Mapping.add("ice/cpp", CppMapping(path = os.path.join(toplevel, "ice", "cpp")))
Mapping.add("ice/java", JavaMapping(path = os.path.join(toplevel, "ice", "java")))
Mapping.add("freeze/cpp", FreezeCppMapping(path = os.path.join(toplevel, "cpp")))
Mapping.add("freeze/java", FreezeJavaMapping(path = os.path.join(toplevel, "java")))
