import os
import time

from pathlib import Path

class domlogger():
    def __init__(self, *args, logRoot = None, outFile = "latest.log", **kwargs):
        self._internalName = f"{self.__class__.__name__}"
        self._name = kwargs.get("name", self._internalName)
        
        # logroot is the path where all log files will be written by default
        self.logRoot : Path
        if not logRoot:
            self.logRoot = Path.joinpath(Path.cwd(), "logs") 
        else:
            self.logRoot = Path.joinpath(logRoot).absolute()
        
        self._fileCheck(self.logRoot, "dir")

        if not outFile:
            self.outFile : Path = self.logRoot.joinpath("latest.log")
        else:
            self.outFile : Path = self.logRoot.joinpath(outFile)
        
        self._fileCheck(self.outFile)

        # -1 debug
        # 0 information
        # 1 warning
        # 2 error
        # 3 critical
        # anything else will default to information

        self.level = 0 # default level if none is selected
        self.debug = -1
        self.info = 0
        self.warn = 1
        self.error = 2
        self.fatal = 3

    def SetLogLevel(self, level : int):
        
        if not isinstance(level, int, float):
            raise TypeError(F"level is not a supported value")

        level = int(level)

        if not (self.debug < level and level < self.fatal):
            level = self.info
        
        self.level = level
    
    def _fileCheck(self, fp : str | Path, typ : str = "file", cifn : bool = True) -> str | None:

        if not fp:
            raise ValueError(f"fp has no value")
        
        if type(fp) == str:
            fp : Path = Path.joinpath(fp).absolute()
        if fp.is_dir():                
            return "dir"
        elif fp.is_file():
            return "file"
        else:
            if typ == "file":
                self._createFile(fp,)
            if typ == "dir":
                fp.mkdir()
            return None
        
    def _createFile(self, fp : Path, typ : str = "file") -> bool:
        if not fp:
            raise ValueError(f"fp has no value")
        
        if not fp.exists():
            if typ == "dir":
                fp.mkdir()
            if typ == "file":
                self._writeToFile(fp,"")

    def _writeToFile(self, fp : Path, content : str, mode : str = "a") -> bool:
        if not fp:
            raise ValueError(f"fp has no value")
        
        if isinstance(fp, str):
            fp : Path = Path.joinpath(fp)

        if mode in ["a","w"]:
            with fp.open(mode) as f:
                f.write(content)
        else:
            raise ValueError(f"Can't write with mode {mode}")
        
    def writeLog(self, content : str, level : int = None, *args, **kwargs) -> bool:

        if not content or (level and level < self.level):
            return False
        
        if not "\n" in content or content[len(content) - 1 ] != "\n": # if newline is not in, or newline is not the last character in the string.
            content = f"{content}\n"
        
        try:
            # string building
            msg = f"[{self.levelConverter(level)}] {self.getTimeStamp()} > {content}"
                
            self._writeToFile(self.outFile, msg)
            
        
        except PermissionError as e:
            msg = f"Logger does not have permission to write to current log file {self.outFile}"
            print(msg)

    def levelConverter(self, level = None) -> str:
        if not level:
            level = self.level
        
        levelChar = None
        match level:
            case self.fatal: levelChar = "F"
            case self.error: levelChar = "E"
            case self.warn: levelChar = "W"
            case self.info: levelChar = "I"
            case _: levelChar = "I"

        return f"{levelChar}"

    def getLocalTimeStamp(self, ts="%Y-%d-%m %H:%M:%S") -> str:           
        return self.getTimeStamp(ts, time.localtime())

    def getTimeStamp(self, ts="%Y-%d-%m %H:%M:%S", tm=time.localtime()) -> str:
        # check for types
        if not isinstance(tm, (int, float, time.struct_time)):
            raise TypeError(F"Logger cannot use types other than float and time.struct_time to create a timestamp")
        
        if isinstance(tm, int):
            tm = float(tm)
        if isinstance(tm,float):
            tm = time.gmtime(tm)
        
        timestamp = time.strftime(ts, tm)
        return timestamp

    def internalError(self, message, exc = Exception):
        try:
            self.Error(f"{message}")
            raise exc(f"{message}")
        except Exception as e:
            self.Error(f"intError.. errored out.. ironic ::: {e}")
        else:
            return True
    

    def Debug(self, content : str, *args, **kwargs):
        self.writeLog(f"{content}", level=self.debug, *args, **kwargs)

    def Info(self, content : str, *args, **kwargs):
        self.writeLog(f"{content}", level=self.info, *args, **kwargs)

    def Warn(self, content : str, *args, **kwargs):
        self.writeLog(f"{content}", level=self.warn, *args, **kwargs)

    def Error(self, content : str, *args, **kwargs):
        self.writeLog(f"{content}", level=self.error, *args, **kwargs)

    def Fatal(self, content : str, *args, **kwargs):
        self.writeLog(f"{content}", level=self.fatal, *args, **kwargs)

if __name__ == "__main__":
    print("   _-_   ")
