from abc import ABC, abstractmethod


class Log:
    """
    A composite chain of responsibility design pattern Logger
    """

    class LogInterface(ABC):
        @abstractmethod
        def log(self, msg: str) -> int:
            raise NotImplementedError("log Method not implemented")

    loggers: LogInterface = []

    def logAll(self, msg: str):
        for log_ in self.loggers:
            log_.log(msg)

    def __init__(self, *loggers: LogInterface):
        self.loggers = loggers

    class DBLog(LogInterface):
        def log(self, msg: str):
            print('DB ' + msg)

    class FileLog(LogInterface):
        def log(self, msg: str):
            print('FILE ' + msg)


if __name__ == "__main__":
    log = Log(Log.DBLog(), Log.FileLog())
    log.logAll('logging')
