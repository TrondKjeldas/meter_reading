#!/usr/bin/python

import serial, time, sys
from aidon_obis import *

def aidon_callback(fields):
	print (fields)

a = aidon(aidon_callback)

bb = b'\x7e\x01\x00\x7d\x5e\x00\x7d\x5e\x00\x00\x00\x7e'
for i in range(0,len(bb)):
	b = bb[i].to_bytes(1,'big')
	print(type(b))
	a.decode(b)