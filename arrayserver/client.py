import os.path
import tempfile
from UserDict import UserDict
import json

import requests
import numpy as np

class ArrayClient(UserDict):
    """Dictionary interface to persistent memory mapped arrays"""
    
    def __init__(self, host='localhost', port=6000):
        self.host = host
        self.port = port

    def url(self, name):
        return 'http://%s:%i/%s' % (self.host, self.port, name)
            
    def __setitem__(self, name, array):
        """Stores the array in a memmap file, then pings server."""
        fn = tempfile.mktemp()
        fp = np.memmap(fn, dtype=array.dtype, mode='w+', shape=array.shape)
        fp[:] = array[:]
        
        requests.put(self.url(name), json.dumps({
            'dtype': str(array.dtype),
            'shape': list(array.shape),
            'filename': fn,
            }))
        
    def __getitem__(self, name):
        resp = requests.get(self.url(name))
        if resp.status_code == 404:
            raise KeyError

        meta = resp.json()
        
        return np.memmap(
            meta['filename'],
            dtype=meta['dtype'],
            mode='r',
            shape=tuple(meta['shape']))

    def __delitem__(self, name):
        resp = requests.delete(self.url(name))
        if resp.status_code == 404:
            raise KeyError
