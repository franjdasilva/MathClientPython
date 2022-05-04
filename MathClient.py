import psutil, os
from ctypes import *


DLL_PATH = "MathLibrary.dll"

def GetLoadedDLLs():
    dlls = set()
    p = psutil.Process( os.getpid() )
    for dll in p.memory_maps():
        dlls.add(dll.path)
    return dlls

def GetAbsolutePath(name):
    if os.path.isabs(name):
        path = name
    else:
        path = os.path.join(os.getcwd(),name)
    if os.path.exists(path):
        return path
    else:
        return ''

def IsDLLLoaded(name):
    path = GetAbsolutePath(name)
    if path:
        return path in GetLoadedDLLs()
    else:
        return False


class Fibonacci(object):

    def __init__(self, *args, **kwargs):
        #lazy load
        try:
            if self._dll:
                isLoaded = True
            else:
                isLoaded = False
        except:
            isLoaded = False
        try:
            if not isLoaded:
                self._dll = CDLL(DLL_PATH)
        except Exception as e:
            print(e)

    def Initialize(self, f0, f1):
        try:
            f0 = c_ulong(f0)
            f1 = c_ulong(f1)
            self._dll.fibonacci_init(f0, f1)
        except Exception as e:
            print(e)

    def Next(self):
        try:
            return self._dll.fibonacci_next()
        except Exception as e:
            print(e)

    def Current(self):
        try:
            return self._dll.fibonacci_current()
        except Exception as e:
            print(e)

    def Index(self):
        try:
            return self._dll.fibonacci_index()
        except Exception as e:
            print(e)

def test_GetLoadedDLLs():
    dlls = GetLoadedDLLs()
    assert(dlls)

def test_GetAbsolutePath():
    val =GetAbsolutePath(DLL_PATH)
    assert(val)
    
def test_IsDLLLoaded():
    val =IsDLLLoaded(DLL_PATH)
    assert(not val)

def test_Fibonacci1():
    f = Fibonacci()
    assert(f)

def test_Fibonacci2():
    f = Fibonacci()
    f.Initialize(1,1)
    _val = 0
    while f.Next():
        val = f.Current()
        if val == _val:
            break
        else:
            _val = val
        print(val)
        
    print( str(f.Index() + 1) + 'Fibonacci sequence values fit in an unsigned 64-bit integer' )

if __name__ == '__main__':
    
    #test_GetLoadedDLLs()
    #test_GetAbsolutePath()
    #test_IsDLLLoaded()
    #test_Fibonacci1()
    test_Fibonacci2()
    