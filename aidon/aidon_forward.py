#!/usr/bin/python

import serial, time, sys, argparse
from aidon.hass_influx import *
from aidon.aidon_obis import *

def aidon_callback(fields):
	ts = time.time()

	if 'p_act_in' in fields:
		hi.post("aidon", "power", "%.03f" % (fields['p_act_in']/1000.0), hass_name="Effekt", hass_unit="kW", ts=ts)

	if 'ul1' in fields:
		hi.post("aidon", "voltage_1", "%.03f" % (fields['ul1']), hass_name="Spenning", hass_unit="V", ts=ts)
	if 'ul2' in fields:
		hi.post("aidon", "voltage_2", "%.03f" % (fields['ul2']), hass_name="Spenning", hass_unit="V", ts=ts)
	if 'ul3' in fields:
		hi.post("aidon", "voltage_3", "%.03f" % (fields['ul3']), hass_name="Spenning", hass_unit="V", ts=ts)

	if ('il1' in fields) and args.influx_host:
		hi.post_influx("voltage", "aidon_p1", "%.01f" % fields['ul1'], ts=ts)
		hi.post_influx("voltage", "aidon_p2", "%.01f" % fields['ul2'], ts=ts)
		hi.post_influx("voltage", "aidon_p3", "%.01f" % fields['ul3'], ts=ts)
		hi.post_influx("current", "aidon_p1", "%.01f" % fields['il1'], ts=ts)
		hi.post_influx("current", "aidon_p2", "%.01f" % fields['il2'], ts=ts)

	if 'energy_act_in' in fields:
		hi.post("aidon", "energy", "%.02f" % fields['energy_act_in'], hass_name="Energi", hass_unit="kWh", ts=ts)

def main():
	parser = argparse.ArgumentParser(description='Forward Aidon data to Home Assistant and InfluxDB')
	parser.add_argument('serial_port')
	parser.add_argument('--influx_host')
	parser.add_argument('--influx_db')
	parser.add_argument('--hass_host')
	parser.add_argument('--hass_token')
	args = parser.parse_args()

	# Class used to forward data to Home Assistant and InfluxDB
	hi = hass_influx(
		inf_host=args.influx_host,
		inf_db=args.influx_db,
		hass_host=args.hass_host,
		hass_token=args.hass_token)

	ser = serial.Serial(args.serial_port, 115200, timeout=0.05, parity=serial.PARITY_NONE)

	a = aidon(aidon_callback)

	while(1):
		while ser.inWaiting():
			a.decode(ser.read(1))
		time.sleep(0.01)

if __name__ == "__main__":
	main()