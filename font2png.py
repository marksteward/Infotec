#!/usr/bin/env python

import sys, struct, string
import Image

if len(sys.argv) <= 1:
  print 'Usage: %s font.bin font.png' % sys.argv[0]
  sys.exit(1)

f = open(sys.argv[1], 'rb')

def tobitarray(bs):
  bits = ''.join(bin(ord(b))[2:].zfill(8) for b in bs)
  return map(int, bits)

header = f.read(6)
w, h, start, end, u1, u2 = map(ord, header)

hbytes = h / 8

n = 0
data = []
charws = []

while True:
  charw = f.read(1)
  if len(charw) == 0:
    break
  charws.append(ord(charw))

  for i in range(w):
    col = reversed(f.read(hbytes))
    data += tobitarray(col)
    n += 1

  # gap
  data += [0] * 8 * hbytes
  n += 1

img = Image.new('1', (8 * hbytes, n))
img.putdata(data)
img = img.rotate(90)
img.save(sys.argv[2], 'PNG')

print 'Bitmap size: %dx%d' % (w, h)
print 'Characters: %s-%s' % (start, end)
print 'Unknown: %d, %d' % (u1, u2)
print 'Widths: %s' % charws

