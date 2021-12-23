from datetime import datetime
from typing import Union

class TimeLock:
    def __init__(self, interval_secs: Union[int, float]):
        self.__time = datetime.now()
        self.__interval_secs = interval_secs
    def acquire(self) -> bool:
        time = datetime.now()
        if (time - self.__time).total_seconds() >= self.__interval_secs:
            self.__time = time
            return True