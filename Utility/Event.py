from typing import Any, Callable, Dict, Generic, List, TypeVar
import threading
import uuid

class ListenerId:
    def __init__(self):
        self.__uuid = uuid.uuid4()
        self.__uuid_int = self.__uuid.int
    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)
    def __hash__(self) -> int:
        return self.__uuid_int

class Event:
    def __init__(self):
        self.__listener_map: Dict[ListenerId, Callable[[], None]] = {}
        self.__lock = threading.RLock()
    def add_listener(self, callback: Callable[[], None]) -> ListenerId:
        listener_id = ListenerId()
        with self.__lock:
            assert(listener_id not in self.__listener_map)
            self.__listener_map[listener_id] = callback
    def notify(self):
        with self.__lock:
            for callback in self.__listener_map.values():
                callback()
    def del_listener(self, listener_id: ListenerId):
        with self.__lock:
            assert(listener_id in self.__listener_map)
            del self.__listener_map[listener_id]
    @classmethod
    def Of(cls, type):
        return ArgEvent[type]()

T = TypeVar('T')
class ArgEvent(Generic[T]):
    def __init__(self):
        self.__listener_map: Dict[ListenerId, Callable[[T], None]] = {}
        self.__lock = threading.RLock()
    def add_listener(self, callback: Callable[[T], None]) -> ListenerId:
        listener_id = ListenerId()
        with self.__lock:
            assert(listener_id not in self.__listener_map)
            self.__listener_map[listener_id] = callback
    def notify(self, arg: T):
        with self.__lock:
            for callback in self.__listener_map.values():
                callback(T)
    def del_listener(self, listener_id: ListenerId):
        with self.__lock:
            assert(listener_id in self.__listener_map)
            del self.__listener_map[listener_id]