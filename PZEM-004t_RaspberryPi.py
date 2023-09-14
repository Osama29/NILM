import time
import csv
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import json
import statistics

def print_error_message():
    print("The extension cord is not connected to the main line.")

if __name__ == '__main__':
    try:
        # Connect to the slave
        serial_port = serial.Serial(port='/dev/ttyS0', baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)

        master = modbus_rtu.RtuMaster(serial_port)
        master.set_timeout(2.0)
        master.set_verbose(True)

        dict_payload = dict()
        measurements_per_second = 15
        interval = 1 / measurements_per_second
        sample_count = 0 # Initialize the sample count to zero

        while True:
            try:
                voltage_list, current_list, power_list, energy_list, frequency_list, power_factor_list, alarm_list = [], [], [], [], [], [], []

                for _ in range(measurements_per_second):
                    data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

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
                    power_factor_list.append(power_factor)
                    alarm_list.append(alarm)

                    

                # Calculate the average values
                avg_voltage = round(sum(voltage_list) / len(voltage_list), 2)
                avg_current = round(sum(current_list) / len(current_list), 2)
                avg_power = round(sum(power_list) / len(power_list), 2)
                avg_energy = round(sum(energy_list) / len(energy_list), 2)
                avg_frequency = round(sum(frequency_list) / len(frequency_list), 2)
                avg_power_factor = round(sum(power_factor_list) / len(power_factor_list))
                avg_alarm = round(sum(alarm_list) / len(alarm_list), 2)

                # Calculate the standard deviation values
                std_voltage = round(statistics.stdev(voltage_list), 2)
                std_current = round(statistics.stdev(current_list), 2)
                std_power = round(statistics.stdev(power_list), 2)
                std_energy = round(statistics.stdev(energy_list), 2)
                std_frequency = round(statistics.stdev(frequency_list), 2)
                std_power_factor = round(statistics.stdev(power_factor_list), 2)
                std_alarm = round(statistics.stdev(alarm_list), 2)      

                sample_count += 1 # Increment the sample count woth each successful measurement

                time_hour = time.strftime("%H:%M:%S")

                dict_payload["Time"] = time_hour
                dict_payload["voltage"] = avg_voltage
                dict_payload["current"] = avg_current
                dict_payload["power"] = avg_power
                dict_payload["energy"] = avg_energy
                dict_payload["frequency"] = avg_frequency
                dict_payload["power_factor"] = avg_power_factor
                dict_payload["alarm"] = avg_alarm

                dict_payload["std_voltage"] = std_voltage
                dict_payload["std_current"] = std_current
                dict_payload["std_power"] = std_power
                dict_payload["std_energy"] = std_energy
                dict_payload["std_frequency"] = std_frequency
                dict_payload["std_power_factor"] = std_power_factor
                dict_payload["std_alarm"] = std_alarm

                dict_payload["sample_count"] = sample_count

                str_payload = json.dumps(dict_payload, indent=2)
                print(str_payload)

                date = time.strftime("%Y-%m-%d")

                # Store data in the CSV file
                with open('power_meter_data.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
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
                                     std_alarm]
                                     )
            except Exception as e:
                print_error_message()
                print(f"Error: {str(e)}")
                time.sleep(2) # Wait for 2 seconds before retrying

    except KeyboardInterrupt:
        print('Exiting Script')
    finally:
        # Close connection and resources                                
        master.close()

    