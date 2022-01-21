import os
import psutil
import pathlib

filename: str = '.SingleInstanceChecker.tmp'
touchname: str = '.Touch.tmp'

def OtherProcessExists() -> bool:
    print('my pid:', os.getpid())
    with open(filename, 'ab+') as f:
        f.seek(0)
        c = f.read()
        def other_exists():
            if len(c) != 8:
                return False
            pid = int.from_bytes(c, 'big', signed=True)
            exists = psutil.pid_exists(pid)
            print('other pid:', pid, ', exists:', exists)
            return exists
        if other_exists():
            pathlib.Path(touchname).touch() # notify other window to raise by touching touchfile
            return True
        f.seek(0)
        f.truncate()
        f.write(os.getpid().to_bytes(8, 'big', signed=True))
        print('I\'m the only one!')
        return False
