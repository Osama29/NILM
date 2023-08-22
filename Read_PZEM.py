import time
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

serial = serial.Serial(
                        port= '/dev/ttyS0',
                        baudrate=9600,
                        bytesize= 8,
                        parity= 'N',
                        stopbits= 1,
                        xonxoff=0
)

master = modbus_rtu.RtuMaster(serial)
master.set_timeout(2.0)
master.set_verbose(True)

while True:
    data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
    voltage = data[0] / 10.0
    current = (data[1] + (data[2] << 16)) / 1000.0
    power = (data[3] + (data[4] << 16)) / 10.0
    energy = data[5] + (data[6] << 16)
    frequency = data[7] / 10.0
    powerFactor = data[8] / 100.0
    alarm = data[9]

    print('Voltage : ', voltage)
    print('Current : ', current)
    print('Power : ', power)
    print('Frequency : ', frequency)
    print('Power factor : ', powerFactor)
    print("---------------------")

    time.sleep(1)