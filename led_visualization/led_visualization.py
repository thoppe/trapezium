#!/usr/bin/python
from led_strip import LEDStrip
from led_animation import LEDAnimation
from sensor_data_processor import SensorDataProcessor

#led_animation = LEDAnimation()
#led_animation.draw_animation('data/test.mp4')

sensor_data_processor = SensorDataProcessor()
sensor_data_processor.load_data('../data_collection/travis_walking_indoor_test5.dat', 0)
sensor_data_processor.generate_animation_accel_meter('data/accel_meter.mp4')
	
