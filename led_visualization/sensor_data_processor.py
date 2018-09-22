#!/usr/bin/python
from led_animation import LEDAnimation
from math import *
import csv

class SensorDataProcessor:
	def __init__(self):
		self.device = []
		self.timestamps = []
		self.ax = []
		self.ay = []
		self.az = []
		self.gx = []
		self.gy = []
		self.gz = []

		self.accel = []

	# Generation animations
	def generate_animation_accel_meter(self, filename):
		print 'Generating accelartion magnitudes...'
		self.generate_accel_mag()

		# Down-sample and scale accel magnitude
		print 'Down-sampling/scaling acceleration magnitudes...'
		down_sample_factor = 40
		scale_factor = 1.0 / (sqrt(3.0) * (2.0**15))
		accel_ds = [0] * int(len(self.accel) / down_sample_factor)

		h = open('data/accel_mag_down_sample_scale.dat', 'w')
		for n in range(0, len(accel_ds)):
			accel_ds[n] = scale_factor * sum(self.accel[(n*down_sample_factor):((n+1)*down_sample_factor)]) / float(down_sample_factor)
			h.write('%.8f\n' % accel_ds[n])

		h.close()

		# Generate animation
		print 'Generating animation...'
		led_count = 50
		led_animation = LEDAnimation(led_count = led_count, frame_count = len(accel_ds))

		for n in range(0, len(accel_ds)):
			print 'Generating frame %d/%d' % (n, len(accel_ds))
			lit_count = int(float(led_count) * accel_ds[n])

			for k in range(0, led_count):
				if k <= lit_count:
					led_animation.led_strip_list[n].led_list[k] = [ 0xFF, 0xFF, 0xFF ]

				else:
					led_animation.led_strip_list[n].led_list[k] = [ 0x00, 0x00, 0x00 ]

		led_animation.draw_animation(filename)

	# File i/o
	def load_data(self, filename, device_number = None):
		h = open(filename, 'r')
		csv_handle = csv.reader(h, delimiter=' ')
		
		for row in csv_handle:
			if device_number != None and int(row[0]) != device_number:
				continue

			self.device.append(int(row[0]))
			self.timestamps.append(int(row[1]))
			self.ax.append(int(row[2]))
			self.ay.append(int(row[3]))
			self.az.append(int(row[4]))
			self.gx.append(int(row[5]))
			self.gy.append(int(row[6]))
			self.gz.append(int(row[7]))

	# Signal processing
	def generate_accel_mag(self):
		self.accel = [0] * len(self.ax)

		for n in range(0, len(self.ax)):
			self.accel[n] = sqrt(self.ax[n]**2 + self.ay[n]**2 + self.az[n]**2)


	# Debugging functions
	def __repr__(self):
		return "SensorDataProcessor"
