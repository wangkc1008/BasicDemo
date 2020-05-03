# -*- encoding=utf8 -*-
import struct

bin_str = b'ABCDEFGH'
print(bin_str)
print(bin_str.decode())
res = struct.unpack('>8B', bin_str)
print(res)
res2 = struct.unpack('>4H', bin_str)
print(res2)
res3 = struct.unpack('>2L', bin_str)
print(res3)
res4 = struct.unpack('>8s', bin_str)
print(res4)