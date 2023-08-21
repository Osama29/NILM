# NILM
Non-Intrusive Load Monitoring Device

This is a simplified version of the NILM devices where it implement Raspberry PI 4B and PZEM-004t which is current and voltage sensor. where it works as electical monitor that have a website deployed from the Raspberry Pi, it use machine learning to understand the behaviour of the appliance and give predictions based on it.

Firstly, you have to setup the raspberry pi 
## Configuring and using the pins

Update and upgrade to the latest version of `Raspbian` using the following commands

```powershell
sudo apt-get update
sudo apt-get upgrade
```

if you dont have the GPIO package installed, you simply install it by running the following command.
```powershell
sudo apt-get install rpi.gpio
```

## Configuring Raspberry Pi I2C

Setting up the I2C pins on the raspberry Pi is super easy and will only take a couple of minutes to do.
Secondly, go to the Raspi-config tool by entering the following command.

![alt text here](https://pimylifeup.com/wp-content/uploads/2015/09/Raspberry-Pi-SPI-and-I2C.png)

```powershell
sudo raspi-config
```

in here go to `Interface Options` and then to `I2c`, enable I2c by selecting `Yes`

The Pi should now alert you that I2c will be enabled after reboot. It will then ask if you want it to be loaded by default. Select `Yes` if you plan on using I2c everytime the raspberry pi boots up.

now we want to make sure it has successfully enabled the necessary modules. To this, enter the following command.

```powershell
lsmod | grep i2c_
```

***
## Raspberry Pi Wiring and configuration

To connect the Raspberry Pi to the PZEM-004t correctly to collect the measurements of the appliances such as voltage, current, power, e4nergy, frequency, power factor.

#### the wiring goes like:
| Raspberry PI GPIO | PZEM-004t |
| ----------------- | --------- |
| 5V ( GPIO 2)      | 5v        |
| GND ( GPIO 6)     | GND       |
| TX (GPIO 14)      | RX        | 
|RX (GPIO 15)       | TX        | 


![alt text here](https://github.com/Osama29/NILM/blob/main/Images/Screenshot%202023-08-19%20193237.png?raw=true)

***
## Download Modbus Library

 In order to have a functioning code, you will need to download Modbus-tk which is the serial communication encoding that is used between the PZEM-004t and Raspberry Pi. to download it, just type the following code in the terminal in your Raspberry Pi:

 ```powershell
sudo pip3 install modbus-tk
```

then run the python code under the name: `PZEM-004t Raspberry Pi.py` which must run effortlessly. 

*** 
## Clone the Repository on your Raspberry Pi
you can download the files using the simple command:
```powershell
git clone https://github.com/Osama29/NILM
```

***
## Extra Features

### Implementation of UART to TTL USB module
Incase you were using a TTL to UART Module which use the USB port of the Raspberry Pi, then all you have to do is connect the USB Module and then change the following code in the `PZEM-004t Raspberry Pi.py`:

```python
if __name__ == '__main__':
  try:
      serial_port = serial.Serial(
                                  port '/dev/ttyS0',
                                  baudrate = 9600,
                                  bytesize= 8,
                                  parity='N',
                                  stopbits=1,
                                  xonxoff=0
                                  )
```

Change the code to the following code:

```python
if __name__ == '__main__':
  try:
      serial_port = serial.Serial(
                                  port '/dev/ttyUSB0',
                                  baudrate = 9600,
                                  bytesize= 8,
                                  parity='N',
                                  stopbits=1,
                                  xonxoff=0
                                  )
```
by that you will gain the ability to use the USB module to connect to the PZEM-004t by connecting the TTL to UART Module., you hbave to make sure that the wiring and the hardware are connected correctly.

***
## Troubleshooting

### No Module named 'modbus_tk'
if you were trying to run `PZEM-004t Raspberry Pi.py` and it showed the following error:
```powershell
Traceback (most recent call last):
  File "/home/raspberrypi/PZEM-004t Raspberry Pi.py", line 4, in <module>
     import modbus_tk.defines as cst
ModuleNotFouundError: No module named 'modbus_tk'

------------------
(program exited with code: 1)
Press return to continue
```
Then all you have to do is to run this comand in the terminal:
```powershell
sudo pip3 install modbus-tk
```

### No Module named "serial"
if you were trying to run `PZEM-004t Raspberry Pi.py` and it showed the following error:

```powershell
Traceback (most recent call last):
  File "PZEM-004t Raspberry Pi.py", line 3, in <module>
    import serial
ImportError: No module named serial


------------------
(program exited with code: 1)
Press return to continue
```

you can solve this issue by applying these steps:

1. Open your terminal on Raspberry Pi and type:
```powershell
sudo raspi-config
```

2. after access the menu which will look like this
   
![alt text here](https://pimylifeup.com/wp-content/uploads/2015/09/Raspberry-Pi-SPI-and-I2C.png)

head to `3 Interface Options`

3.  Press on `I6 Serial Port` and clcik `Yes` on the two option to enable the Serial port and avoid the error.

