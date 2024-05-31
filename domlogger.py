import os
import time


class Logger():
    
    def __init__(self, logDir = None, logFile = "log.log", printConsole = True):
        if not logDir:
            self.logDir = os.getcwd()
        else:
            self.logDir = logDir
            
        if not os.path.isdir(self.logDir):
            if not os.path.isfile(self.logDir):
                try:
                    os.makedirs(self.logDir)
                except Exception as e:
                    print(e)
                    
        self.logFileName = f"{logFile}"
        self.logFilePath = os.path.join(self.logDir, self.logFileName)
        
        self.printConsole = printConsole
        
        # todo 
        # add init paramter for selected level
        # level SHOULD be the minimum level printed, anything below will be ignored. NOT only the default level
        
        self.level = 0 # default level if none is selected
        # -1 debug
        # 0 information
        # 1 warning
        # 2 error
        # 3 critical
        # anything else will default to information
        self.debug = -1
        
        self.information = 0
        self.info = self.information
        
        self.warning = 1
        self.warn = self.warning
        
        self.error = 2
        
        self.fatal = 3
        
        # todo
        # time
        
    def getLocalTimeStamp(self, ts="%Y-%d-%m %H:%M:%S"):           
        return self.getTimeStamp(ts, time.localtime())

    def getTimeStamp(self, ts="%Y-%d-%m %H:%M:%S", tm=time.localtime()):
        # check for types
        if not isinstance(tm, (int, float, time.struct_time)):
            raise TypeError(F"Logger cannot use types other than float and time.struct_time to create a timestamp")
        
        if isinstance(tm, int):
            tm = float(tm)
        if isinstance(tm,float):
            tm = time.gmtime(tm)
        
        timestamp = time.strftime(ts, tm)
        return timestamp

    def levelConverter(self, level) -> str:
        if not level:
            level = self.level
        
        levelChar = None
        match level:
            case self.fatal: levelChar = "F"
            case self.error: levelChar = "E"
            case self.warning: levelChar = "W"
            case self.information: levelChar = "I"
            
            case _: levelChar = "D"

        return f"{levelChar}"

    def logWrite(self, content : str, level : int = None, *args, **kwargs) -> bool:
        
        if not content or (level and level < self.level):
            return False
        
        if not level:
            level = self.level 
            
        if not "\n" in content or content[len(content) - 1 ] != "\n": # if newline is not in, or newline is not the last character in the string.
            content = f"{content}\n"
        else: # todo figure out what I wanted to do here ;)
            pass
        
        # time
        ts = ""
        if kwargs.get("skiptimestamp") in [False, None]:
            tForm = kwargs.get("ts", "%d-%m %H:%M:%S")
            try:
                ts = f" {self.getLocalTimeStamp(tForm)}"
            except TypeError:
                ts = ""
                
        
        try:
            # string building
            msg = f"[{self.levelConverter(level)}]{ts} > {content}"
                
            with open(self.logFilePath, "a") as logFile:
                logFile.write(msg)
            
            if (self.printConsole):
                print(msg)
        except PermissionError as e:
            msg = f"Logger does not have permission to write to current log file {self.logFilePath}"
            print(msg)

        return True
    
    Write = logWrite

    def Debug(self, content : str, *args, **kwargs):
        self.logWrite(f"{content}", level=self.debug, *args, **kwargs)
    
    def Information(self, content : str, *args, **kwargs):
        self.logWrite(f"{content}", level=self.information, *args, **kwargs)
        
    Info = Information
    # def Info(self, content: str):
    #     self.Information(content=f"{content}")
        
    def Warn(self, content : str, *args, **kwargs):
        self.logWrite(f"{content}", level=self.warning, *args, **kwargs)
    
    def Error(self, content : str, *args, **kwargs):
        self.logWrite(f"{content}", level=self.error, *args, **kwargs)
    
    def Fatal(self, content : str, *args, **kwargs):
        self.logWrite(f"{content}", level=self.fatal, *args, **kwargs)
            
    def internalError(self, message, exc = Exception):
        try:
            self.Error(f"{message}")
            raise exc(f"{message}")
        except Exception as e:
            self.Error(f"intError.. errored out.. ironic \n {e}")
        else:
            return True
    intError = internalError

    

if __name__ == "__main__":
    print("   _-_   ")
    
    mLog = Logger("")
    
    mLog.logWrite("heheh", 123)
    
    mLog.getTimeStamp(tm=123123)
