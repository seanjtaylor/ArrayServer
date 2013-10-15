import os
import json

from tornado.web import RequestHandler

import numpy as np

arrays = {}

class ArrayHandler(RequestHandler):
    def get(self, name):
        """Return only the metadata, not the handle itself"""
        if name not in arrays:
            raise HTTPError(404)
        meta = {k: v for k, v in arrays[name].iteritems() if k != 'obj'}
        self.write(json.dumps(meta))
        

    def put(self, name):
        """Store the metadata for this vector and open a handle to the file."""
        meta = json.loads(self.request.body)
        
        meta['obj'] = np.memmap(
            meta['filename'],
            dtype=meta['dtype'],
            mode='r',
            shape=tuple(meta['shape'])
            )

        arrays[name] = meta
        self.write(json.dumps({'success': 1}))

    def delete(self, name):
        """Delete the memory mapped file and remove the handle"""
        if name not in arrays:
            raise HTTPError(404)

        meta = arrays[name]
        os.path.unlink(meta['filename'])
        del arrays[name]
        self.write(json.dumps({'success': 1}))
