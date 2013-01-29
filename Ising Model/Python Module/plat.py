import sys
import os

def determine():
    if os.name=='posix':
        return 'OS X'
    elif sys.platform=='linux2':
        return 'Linux'
    else:
        return 'Windows'