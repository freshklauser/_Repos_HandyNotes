
## pyshark 方法
```buildoutcfg
In[4]: [item for item in dir(pyshark) if not item.startswith('_')]
Out[4]: 
['FileCapture',
 'InMemCapture',
 'LiveCapture',
 'LiveRingCapture',
 'RemoteCapture',
 'UnsupportedVersionException',
 'capture',
 'config',
 'packet',
 'sys',
 'tshark']
```