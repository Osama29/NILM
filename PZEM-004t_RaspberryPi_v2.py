import time
import serial
import json
import statistics
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import csv

CSV_FILE_NAME= "Fridge.csv"

serial = serial.Serial(
                        port= '/dev/ttyUSB0',
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

                # Calculate the average values
                avg_voltage= round(sum(voltage_list) / len(voltage_list), 2)
                avg_current= round(sum(current_list) / len(current_list), 2)
                avg_power= round(sum(power_list) / len(power_list), 2)
                avg_energy= round(sum(energy_list) / len(energy_list), 2)
                avg_frequency= round(sum(frequency_list) / len(frequency_list), 2)
                avg_power_factor= round(sum(powerFactor_list) / len(powerFactor_list), 2)
                avg_alarm= round(sum(alarm_list) / len(alarm_list), 2)

                # Calculate thge standard deviation values
                std_voltage= round(statistics.stdev(voltage_list), 2)
                std_current= round(statistics.stdev(current_list), 2)
                std_power= round(statistics.stdev(power_list), 2)
                std_energy= round(statistics.stdev(energy_list), 2)
                std_frequency=- round(statistics.stdev(frequency_list), 2)
                std_power_factor= round(statistics.stdev(powerFactor_list), 2)
                std_alarm= round(statistics.stdev(alarm_list), 2)
            
                dict_payload["Time"]= time_hour
                dict_payload["voltage"]= avg_voltage
                dict_payload["current"]= avg_current
                dict_payload["power"]= avg_power
                dict_payload["energy"]= avg_energy
                dict_payload["frequency"]= avg_frequency
                dict_payload["powerFactor"]= avg_power_factor

                dict_payload["std_voltage"]= std_voltage
                dict_payload["std_current"]= std_current
                dict_payload["std_power"]= std_power
                dict_payload["std_energy"]= std_energy
                dict_payload["std_frequency"]= std_frequency
                dict_payload["std_powerFactor"]= std_power_factor

                str_payload = json.dump(dict_payload, indent= 2)
                print(str_payload)

                date= time.strftime("%Y-%m-%d")

                # Store data in the CSV File
                with open(CSV_FILE_NAME, 'a', newline='') as file:
                    writer= csv.writer(file)
                    writer.writerow([date, 
                                     time_hour,
                                     avg_voltage,
                                     avg_current,
                                     avg_power,
                                     avg_energy,
                                     avg_frequency,
                                     avg_power_factor,
                                     avg_alarm,
                                     std_voltage,
                                     std_current,
                                     std_power,
                                     std_energy,
                                     std_frequency,
                                     std_power_factor,
                                     std_alarm])



            except Exception as e:
                print(f"Error: {str(e)}")
                print_error_message()
                time.sleep(2)

    except KeyboardInterrupt:
        print('Exiting Script')
    finally:
        master.close()
