# raven-cosm

A library to connect a Rainforest Automation RAVEn Smart Meter interface to a cosm.com feed
and also to the weMonitor servers.

## TODO

TODO:

Figure out source (and solution) for this error, which turns up only rarely:

```python
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python2.7/threading.py", line 552, in __bootstrap_inner
    self.run()
  File "/usr/lib/python2.7/threading.py", line 505, in run
    self.__target(*self.__args, **self.__kwargs)
  File "/home/r/Projects/raven-cosm/lib/usbio.py", line 38, in run
    self.notify(line)
  File "/home/r/Projects/raven-cosm/lib/subject.py", line 10, in notify
    observer.update(self, message)
  File "/home/r/Projects/raven-cosm/lib/skipper.py", line 17, in update
    self.notify(message)
  File "/home/r/Projects/raven-cosm/lib/subject.py", line 10, in notify
    observer.update(self, message)
  File "/home/r/Projects/raven-cosm/lib/xml_fragment_collector.py", line 45, in update
    self.notify(m.group(1) + "\n")
  File "/home/r/Projects/raven-cosm/lib/subject.py", line 10, in notify
    observer.update(self, message)
  File "/home/r/Projects/raven-cosm/lib/we_monitor_writer.py", line 32, in update
    r = requests.post(self.API_PREFIX, data=data)
  File "/usr/local/lib/python2.7/dist-packages/requests/api.py", line 88, in post
    return request('post', url, data=data, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/requests/api.py", line 44, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/requests/sessions.py", line 456, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python2.7/dist-packages/requests/sessions.py", line 559, in send
    r = adapter.send(request, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/requests/adapters.py", line 375, in send
    raise ConnectionError(e, request=request)
ConnectionError: HTTPSConnectionPool(host='app.wemonitorhome.com', port=443): Max retries exceeded with url: /api/rainforest-eagle (Caused by <class 'socket.gaierror'>: [Errno -2] Name or service not known)
```


