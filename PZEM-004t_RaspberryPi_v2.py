import time
import serial
import json
import statistics
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

serial = serial.Serial(
                        port= '/dev/ttyS0',
                        baudrate= 9600,
                        bytesize= 8,
                        parity= 'N',
                        stopbits= 1,
                        xonxoff= 0
)

def print_error_message():
    print("The extension cord is not connected to the main line.")

if __name__ == '__main__':
    try:
        master = modbus_rtu.RtuMaster(serial)
        master.set_timeout(2.0)
        master.set_verbose(True)

        dict_payload = dict()
        measurements_per_second = 15
        interval = 1 / measurements_per_second

        while True:
            try:
                voltage_list, current_list, power_list, energy_list, frequency_list, powerFactor_list, alarm_list = [], [], [], [], [], [], []

                for _ in range(measurements_per_second):
                    data= master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

                    if len(data) < 10:
                        raise ValueError("Invalid data received")
                
                    voltage = data[0] / 10.0
                    current = (data[1] + (data[2] << 16)) / 1000.0
                    power = (data[3] + (data[4] << 16)) / 10.0
                    energy = data[5] + (data[6] << 16)
                    frequency = data[7] / 10.0
                    power_factor = data[8] / 100.0
                    alarm = data[9]

                    voltage_list.append(voltage)
                    current_list.append(current)
                    power_list.append(power)
                    energy_list.append(energy)
                    frequency_list.append(frequency)
                    powerFactor_list.append(power_factor)
                    alarm_list.append(alarm)

                time_hour = time.strftime("%H:%M:%S")
            
                dict_payload["Time"]= time_hour
                dict_payload["voltage"]= voltage
                dict_payload["current"]= current
                dict_payload["power"]= power
                dict_payload["energy"]= energy
                dict_payload["frequency"]= frequency
                dict_payload["powerFactor"]= power_factor

                str_payload = json.dump(dict_payload, indent= 2)
                print(str_payload)



            except Exception as e:
                print(f"Error: {str(e)}")
                print_error_message()
                time.sleep(2)

    except KeyboardInterrupt:
        print('Exiting Script')
    finally:
        master.close()
