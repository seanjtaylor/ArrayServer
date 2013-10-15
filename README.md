ArrayServer
===========

**Serves Numpy Arrays Persistently from Memory Mapped Files**

Ever wanted to store large numpy arrays persistently, but using something faster than disk? Well here you go.  The server process holds a handle to a memory mapped file containing a binary representation of a numpy array.  When the client requests the array, the server returns the filename and the client can access the memory mapped array without having to read from disk.

Starting the server
-------------------

```bash
$ python -m arrayserver
```

Storing a large array
---------------------

```python
>>> from arrayserver import ArrayClient
>>> import numpy as np
>>> c = ArrayClient()
>>> myarray = np.random.random(500000)
>>> myarray.sum()
249876.10611505382
>>> c['myarray'] = myarray
>>> quit() # the array is still in memory in the server process
```


Accessing the array later (look ma, no disk!)
---------------------------------------------

```python
>>> from arrayserver import ArrayClient

>>> c = ArrayClient()
>>> myarray = c['myarray']
>>> myarray.shape
(500000,)
>>> myarray.sum()
memmap(249876.10611505382)
```
