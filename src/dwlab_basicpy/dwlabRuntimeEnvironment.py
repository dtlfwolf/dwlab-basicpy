import inspect
from pathlib import Path
import platform

if platform.system() == "Windows":
    # On Windows, use something like C:\dwlab or from environment
    __DWLAB_HOME__ = Path("C:/dwlab").resolve()
else:
    # On Unix-like, use absolute /opt/dwlab
    __DWLAB_HOME__ = Path("/opt/dwlab").resolve()

import socket 
import sys

import logging
from dwlab_basicpy import dwlabLogger as dwlabLogger
dwlabLogger.setup_logging()
logger=logging.getLogger(__name__)


class dwlabRuntimeEnvironment:
    def __init__(
            self,
            dwlab_src_home=None,
            dwlab_package_home=None,
            dwlab_package=None,
            hostname=None,
            fqdn=None,
            hostIP=None
       ):
        function_name = sys._getframe().f_code.co_name
        class_name=self.__class__.__name__
        function_name=class_name+"."+function_name
        logger.debug("Entering function "+str(function_name))

        stack=inspect.stack()
        callerFrame=stack[1]
        callingModule=callerFrame.filename
        if dwlab_src_home is not None:
            self._dwlab_src_home=dwlab_src_home
        else:
            self._dwlab_src_home=Path(callingModule).resolve().parent
        logger.debug("DW-Lab: dwlab_src_home="+str(self._dwlab_src_home))

        if dwlab_package_home is not None:
            self._dwlab_package_home=dwlab_package_home
        else:
            self._dwlab_package_home=Path(self._dwlab_src_home).parent
        logger.debug("DW-Lab: dwlab_package_home="+str(self.dwlab_package_home))
        
        if dwlab_package is not None:
            self._dwlab_package=dwlab_package
        else:
            if self._dwlab_package_home.is_dir():
                self._dwlab_package=Path(self._dwlab_package_home).name
            else:
                logger.error("Cannot determine dwlab_package from dwlab_package_home.")
                raise RuntimeError("Cannot determine dwlab_package from dwlab_package_home.")
        logger.debug("DW-Lab: dwlab_package="+str(self._dwlab_package))

        self._dwlab_home=Path(self._dwlab_package_home).parent
        if self._dwlab_home != __DWLAB_HOME__:
            logger.warning("Given dwlab_home does not match actual __DWLAB_HOME__.")
            logger.warning("Given dwlab_home: "+str(self._dwlab_home))
            logger.warning("Expected dwlab_home: "+str(__DWLAB_HOME__))
            logger.warning("Using expected __DWLAB_HOME__.")
            logger.warning("Please check your client code location.")
            logger.warning("Expecting settings in "+str(__DWLAB_HOME__) + "<PackageName>/etc/*.yaml")
            self._dwlab_home=__DWLAB_HOME__
            #raise RuntimeError("Given dwlab_home does not match actual dwlab_home.")
        logger.debug("DW-Lab: dwlab_home="+str(self._dwlab_home))

        self._hostname=socket.gethostname()
        if hostname is not None:
            if self._hostname != hostname:
                logger.error("Given hostname does not match actual hostname.")
                logger.error("Given hostname: "+str(hostname))
                logger.error("Actual hostname: "+str(self._hostname))
                logger.error("Using actual hostname.")
                logger.error("Please check your code.")
                raise RuntimeError("Given hostname does not match actual hostname.")
        logger.debug("DW-Lab: hostname="+str(self.hostname))

        self._fqdn=socket.getfqdn()
        if fqdn is not None:
            if self._fqdn != fqdn:
                logger.error("Given fqdn does not match actual fqdn.")
                logger.error("Given fqdn: "+str(fqdn))
                logger.error("Actual fqdn: "+str(self._fqdn))
                logger.error("Using actual fqdn.")
                logger.error("Please check your code.")
                raise RuntimeError("Given fqdn does not match actual fqdn.")
        logger.debug("DW-Lab: fqdn="+str(self.fqdn))
        
        self._hostIP=socket.gethostbyname(self._hostname)
        if hostIP is not None:
            if self._hostIP != hostIP:
                logger.error("Given hostIP does not match actual hostIP.")
                logger.error("Given hostIP: "+str(hostIP))
                logger.error("Actual hostIP: "+str(self._hostIP))
                logger.error("Using actual hostIP.")
                logger.error("Please check your code.")
                raise RuntimeError("Given hostIP does not match actual hostIP.")

        logger.debug("Leaving function "+str(function_name))

    @property
    def dwlab_src_home(self):
        return self._dwlab_src_home
    @property
    def dwlab_package_home(self):
        return self._dwlab_package_home
    @property
    def dwlab_package(self):
        return self._dwlab_package
    @property
    def dwlab_home(self):
        return self._dwlab_home
    @property
    def hostname(self):
        return self._hostname
    @property
    def fqdn(self):
        return self._fqdn
    @property
    def hostIP(self):
        return self._hostIP

    def to_dict(self):
        function_name = sys._getframe().f_code.co_name
        class_name=self.__class__.__name__
        function_name=class_name+"."+function_name
        logger.debug("Entering function "+str(function_name))

        return {
            "dwlab_src_home":str(self._dwlab_src_home),
            "dwlab_package_home":str(self._dwlab_package_home),
            "dwlab_package":self._dwlab_package,
            "dwlab_home":str(self._dwlab_home),
            "hostname":self._hostname,
            "fqdn":self._fqdn,
            "hostIP":self._hostIP
        }
    
    @classmethod
    def from_dict(cls, env_dict):
        function_name = sys._getframe().f_code.co_name
        class_name="dwlabRuntimeEnvironment"
        function_name=class_name+"."+function_name
        logger.debug("Entering function "+str(function_name))

        
        dwlab_src_home=Path(env_dict["dwlab_src_home"])
        dwlab_package_home=Path(env_dict["dwlab_package_home"])
        dwlab_package=env_dict["dwlab_package"]
        hostname=env_dict["hostname"]
        fqdn=env_dict["fqdn"]
        hostIP=env_dict["hostIP"]

        logger.debug("Leaving function "+str(function_name))
        return cls(
            dwlab_src_home=dwlab_src_home,
            dwlab_package_home=dwlab_package_home,
            dwlab_package=dwlab_package,
            hostname=hostname,
            fqdn=fqdn,
            hostIP=hostIP
        )