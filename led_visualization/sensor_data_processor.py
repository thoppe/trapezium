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
	def generate_animation_delay_line(self, filename):
		# Down-sample and scale acceleration vectors
		print 'Down-sampling/scaling acceleration values...'
		down_sample_factor = 40
		scale_factor = 1.0 / (2.0**15)
		ax_ds = [0] * int(len(self.ax) / down_sample_factor)
		ay_ds = [0] * int(len(self.ay) / down_sample_factor)
		az_ds = [0] * int(len(self.az) / down_sample_factor)
		
		h = open('data/accel_downsample.dat', 'w')
		for n in range(0, len(ax_ds)):
			ax_ds[n] = abs(scale_factor * sum(self.ax[(n*down_sample_factor):((n+1)*down_sample_factor)]) / float(down_sample_factor))
			ay_ds[n] = abs(scale_factor * sum(self.ay[(n*down_sample_factor):((n+1)*down_sample_factor)]) / float(down_sample_factor))
			az_ds[n] = abs(scale_factor * sum(self.az[(n*down_sample_factor):((n+1)*down_sample_factor)]) / float(down_sample_factor))
			h.write('%.8f %.8f %.8f\n' % (ax_ds[n], ay_ds[n], az_ds[n]))
		h.close()
		
		# Filter acceleration vectors
		print 'Filtering/rectifying acceleration vectors...'
		tap_count = 10
		ax_ds_filt = [0] * len(ax_ds)
		ay_ds_filt = [0] * len(ay_ds)
		az_ds_filt = [0] * len(az_ds)
		
		ax_ds = ax_ds + ([0] * tap_count)
		ay_ds = ay_ds + ([0] * tap_count)
		az_ds = az_ds + ([0] * tap_count)
		
		h = open('data/accel_ds_filt.dat', 'w')
		for n in range(0, len(ax_ds_filt)):
			ax_ds_filt[n] = sum(map(abs, ax_ds[n:(n+tap_count-1)])) / float(tap_count)
			ay_ds_filt[n] = sum(map(abs, ay_ds[n:(n+tap_count-1)])) / float(tap_count)
			az_ds_filt[n] = sum(map(abs, az_ds[n:(n+tap_count-1)])) / float(tap_count)
			h.write('%.8f %.8f %.8f\n' % (ax_ds_filt[n], ay_ds_filt[n], az_ds_filt[n]))
		h.close()

		# Generate animation
		print 'Generating animation...'
		led_count = 50
		led_animation = LEDAnimation(led_count = led_count, frame_count = len(ax_ds_filt))

		ax_list = [ 0.0 ] * led_count
		ay_list = [ 0.0 ] * led_count
		az_list = [ 0.0 ] * led_count

		for n in range(0, len(ax_ds_filt)):
			ax_list = [ ax_ds_filt[n] ] + ax_list[0:len(ax_list)-1]
			ay_list = [ ay_ds_filt[n] ] + ay_list[0:len(ay_list)-1]
			az_list = [ az_ds_filt[n] ] + az_list[0:len(az_list)-1]
			
			#print len(ax_list)
			#print len(ay_list)
			#print len(az_list)
			
			print 'Generating frame %d/%d' % (n, len(ax_ds_filt))

			for k in range(0, led_count):
				#print n, k
				led_animation.led_strip_list[n].led_list[k] = [ int(255.0*ax_list[k]), int(255.0*ay_list[k]), int(255.0*az_list[k]) ]

		led_animation.draw_animation(filename)
		
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
