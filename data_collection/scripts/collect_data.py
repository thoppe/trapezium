#!/usr/bin/python
import sys
import serial, struct

def run_collect(device, filename):
	ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)

	try:
		h = open('output.dat', 'w')
		while 1:
			s = ser.read(10)
			#print s, len(s)
			a = struct.unpack('Ihhh', s)
			if ((a[0] >> 24) & 0xFF) != 0xD1:
				ser.read(1)
			else:
				h.write('%d %u % 08d % 08d % 08d % 08d % 08d % 08d\n' % (0, a[0] >> 8, a[1], a[2], a[3], 0, 0, 0))
				print '%08x % 08d % 08d % 08d' % (a[0], a[1], a[2], a[3])

	except Exception as e:
		print(e)
		ser.close()
		h.close()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage:'
		print '\t./run_collect device filename'

	else:
		run_collect(sys.argv[1], sys.argv[2])
