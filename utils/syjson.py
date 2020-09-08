import threading, os, json

class SyJsonObj:
    def __init__(self):
        raise Exception('Abstract Class')
    
    def __getitem__(self,key):
        raise Exception('Abstract Class')

    def _no_sync(self,key):
        raise Exception('Abstract Class')
    
    def var(self):
        raise Exception('Abstract Class')
    
    def _get_synced_item(self,key,v):
        if type(v) in (list,tuple):
            return SyncedList(self,key)
        elif type(v) in (dict,):
            return SyncedDict(self,key)
        return v

    def _get_desynced_item(self,v):
        if issubclass(v.__class__,SyJsonObj):
            return v.var()
        return v

class SyJson(SyJsonObj):
    def __init__(self,path:str):
        self.file_path = os.path.abspath(path)
        if not os.path.exists(self.file_path):
            open(self.file_path,'wt').write('')
        self.f_lock = threading.Lock()
        self.wait_for_save = False
    
    def _read(self):
        self.f_lock.acquire()
        try:
            f = open(self.file_path,'rt').read()
            if f != '': return json.loads(f)
            else: return {}
        finally:
            self.f_lock.release()

    def _write(self,dic:dict):
        self.f_lock.acquire()
        try:
            open(self.file_path,'wt').write(json.dumps(dic))
        finally:
            self.f_lock.release()

    def var(self):
        return self._read()
    
    def __str__(self):return self.var().__str__()

    def _no_sync(self,key):
        return self._read()[key]

    def __getitem__(self,key):
        d = self._read()
        if key in d.keys():
            return self._get_synced_item(key,d[key])
        raise KeyError('Not valid key')
        
    def __setitem__(self, key, value):
        value = self._get_desynced_item(value)
        d = self._read()
        d[key] = value
        self._write(d)

    def keys(self):return self.var().keys()
    def items(self):return self.var().items()
    def values(self):return self.var().values()

class InnerIterObject(SyJsonObj):
    def __init__(self,root:SyJsonObj,key):
        self.root = root
        self.root_key = key

    def var(self):
        return self.root.var()[self.root_key]

    def sync(self,var):
        self.root[self.root_key] = var

    def __str__(self):return self.var().__str__()

    def _no_sync(self,key):
        return self.root._no_sync(self.root_key)[key]

    def __getitem__(self,key):
        return self._get_synced_item(key,self.var()[key])

    def __setitem__(self, key, value):
        value = self._get_desynced_item(value)
        val = self.var() 
        val[key] = value
        self.sync(val)

class SyncedList(InnerIterObject):
    def __init__(self,root:SyJsonObj,key):
        InnerIterObject.__init__(self,root,key)

    def append(self,v):
        v = self._get_desynced_item(v)
        val = self.var()
        res = val.append(v)
        self.sync(val)
        return res

    def __delitem__(self,name):
        val = self.var()
        del val[name]
        self.sync(val)

    def pop(self,num=-1):
        val = self.var()
        res = val.pop(num)
        res = self._get_desynced_item(res)
        self.sync(val)
        return res

    def index(self,arg):return self.var().index(arg)

class SyncedDict(InnerIterObject):
    def __init__(self,root:SyJsonObj,key):
        InnerIterObject.__init__(self,root,key)
        
    def keys(self):return self.var().keys()
    def values(self):return self.var().values()
    def items(self):return self.var().items()

