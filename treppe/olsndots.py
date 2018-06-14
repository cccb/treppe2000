#!/usr/bin/env python3

import serial
import struct
from cobs import cobs
from collections import namedtuple
from enum import Enum
import time

EOP = b'\0'

#def cobs_encode(data):
#    return b''.join(bytes([len(x)+1]) + x for x in data.split(EOP))
#
#def cobs_decode(data):
#    out = b''
#    while data:
#        n, *rest = data
#        out += b'\0' + bytes(rest[:n-1])
#        data = rest[n-1:]
#    return out[1:]

def address_pkt(addr):
    return struct.pack('<I', addr)

def framebuf_pkt(data):
    return struct.pack('<32I', data)

class Driver:
    type_drivers = {}

    def __init__(self, port, devices=None, addrs=None, baudrate=500000, timeout=0.100):
        self._ser = serial.Serial(port, baudrate)
        self._ser.write(b'\0')
        self._ser.flushInput()
        self.timeout = timeout
        if addrs is not None:
            self.nodes = [ type_drivers[device_type](addr, self) for addr, device_type in addrs ]
        if devices is not None:
            for dev in devices:
                dev.driver = self
            self.nodes = devices

    def probe_devices(self):
        while True:
            self._ser.write(b'\x00')
            addr, device_type = self.recv_struct('IB', timeout=0.010)
            yield addr, device_type, self.type_drivers.get[device_type]
            time.sleep(0.010)

    def recv_struct(self, fmt, timeout=None):
        self._ser.timeout = self.timeout if timeout is None else timeout
        data = self._ser.read_until(b'\0')
        return struct.unpack('<'+fmt, cobs.decode(data[:-1]))

    def send_struct(self, fmt, *args):
        data = struct.pack('<'+fmt, *args)
        self._ser.write(cobs.encode(data)+EOP)

    @classmethod
    def register_device(drv_kls, device_type):
        def wrapper(dev_kls):
            drv_kls.type_drivers[device_type] = dev_kls
            return dev_kls
        return wrapper

@Driver.register_device(device_type=0x01)
class Olsndot:
    CMD_READ_STATUS = 0x01

    class ColorSpec(Enum):
        white            = 0X00
        single_color     = 0X01
        rgb              = 0X02
        rgbw             = 0X03
        cold_warm_white  = 0X04
        wwa              = 0x05

    def __init__(self, addr, driver=None):
        self.addr = addr
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver
        self.fetch_status()

    def send_framebuf(self, data):
        self._driver.send_struct('I', self.addr)
        self._driver.send_struct('{}{}'.format(self.nchannels, self.channel_spec), *data)

    def send_cmd(self, cmd):
        self._driver.send_struct('I', self.addr)
        self._driver.send_struct('B', cmd)

    Status = namedtuple('Status',
            ['uptime_s', 'uart_overruns', 'frame_overruns', 'invalid_frames', 'vcc_mv', 'temp_celsius'])
    def fetch_status(self):
        self.send_cmd(Olsndot.CMD_READ_STATUS)
        (self.fw_ver, self.hw_ver,
        self.nbits, chspec, cs, self.nchannels,
        uptime_s,
        uart_overruns, frame_overruns, invalid_frames,
        vcc_mv, temp_celsius) = self._driver.recv_struct('BBBBBHIIIIHH')
        self.color_spec = Olsndot.ColorSpec(cs)
        self.channel_spec = chr(chspec)
        return Olsndot.Status(uptime_s, uart_overruns, frame_overruns, invalid_frames, vcc_mv, temp_celsius)

    def __str__(self):
        st = self.fetch_status()
        return '<Olsndot {}.{}@{} {}ch*{} up {}s vcc {:4.3}V temp {}C>'.format(
                self.fw_ver, self.hw_ver, self.addr, self.nchannels, self.channel_format,
                st.uptime_s, st.vcc_mv/1000, st.temp_celsius)

    @property
    def channel_format(self):
        return '{}{}'.format(self.color_spec.name, self.nbits)

if __name__ == '__main__':
    d = Driver('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0')
    for addr, tid, drv in d.probe_devices():
        print(addr, tid, drv)
