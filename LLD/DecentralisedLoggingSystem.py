from abc import ABC, abstractmethod

class LogProcessor(ABC):
    INFO = 1
    DEBUG = 2
    ERROR = 3

    def __init__(self, next_logger_processor=None):
        self.next_logger_processor = next_logger_processor

    def log(self, log_level, message):
        if self.next_logger_processor:
            self.next_logger_processor.log(log_level, message)

class InfoLogProcessor(LogProcessor):

    def log(self, log_level, message):
        if log_level == LogProcessor.INFO:
            DecentralizedLogger.get_instance().log_info(message)
        else:
            super().log(log_level, message)

class DebugLogProcessor(LogProcessor):

    def log(self, log_level, message):
        if log_level == LogProcessor.DEBUG:
            DecentralizedLogger.get_instance().log_debug(message)
        else:
            super().log(log_level, message)

class ErrorLogProcessor(LogProcessor):

    def log(self, log_level, message):
        if log_level == LogProcessor.ERROR:
            DecentralizedLogger.get_instance().log_error(message)
        else:
            super().log(log_level, message)


class DecentralizedLogger:
    _instance = None

    def __init__(self):
        if DecentralizedLogger._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DecentralizedLogger._instance = self
            self.log_file_path = "logs.txt"

    @staticmethod
    def get_instance():
        if DecentralizedLogger._instance is None:
            DecentralizedLogger._instance = DecentralizedLogger()
        return DecentralizedLogger._instance

    def log_info(self, message):
        self._log_to_console("INFO", message)
        self._log_to_file("INFO", message)
        self._log_to_db("INFO", message)

    def log_debug(self, message):
        self._log_to_console("DEBUG", message)
        self._log_to_file("DEBUG", message)
        self._log_to_db("DEBUG", message)

    def log_error(self, message):
        self._log_to_console("ERROR", message)
        self._log_to_file("ERROR", message)
        self._log_to_db("ERROR", message)

    def _log_to_console(self, log_type, message):
        print(f"{log_type}: {message}")

    def _log_to_file(self, log_type, message):
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"{log_type}: {message}\n")

    def _log_to_db(self, log_type, message):
        # Simulate logging to a database
        print(f"Logging {log_type} to database: {message}")
        # You would implement the actual database logging here

def main():
    log_processor = InfoLogProcessor(DebugLogProcessor(ErrorLogProcessor(None)))

    log_processor.log(LogProcessor.ERROR, "exception happens")
    log_processor.log(LogProcessor.DEBUG, "need to debug this")
    log_processor.log(LogProcessor.INFO, "just for info")

if __name__ == "__main__":
    main()
