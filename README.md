# NILM
Non-Intrusive Load Monitoring Device

This is a simplified version of the NILM devices where it implement Raspberry PI 4B and PZEM-004t which is current and voltage sensor. 

Firstly, you have to setup the raspberry pi 
### Configuring and using the pins

Update and upgrade to the latest version of `Raspbian` using the following commands

```powershell
sudo apt-get update
sudo apt-get upgrade
```

if you dont have the GPIO package installed, you simply install it by running the following command.
```powershell
sudo apt-get install rpi.gpio
```

### Configuring Raspberry Pi I2C

Setting up the I2C pins on the raspberry Pi is super easy and will only take a couple of minutes to do.
Secondly, go to the Raspi-config tool by entering the following command.

```powershell
sudo raspi-config
```

in here go to `Interface Options` and then to `I2c`, enable I2c by selecting `Yes`

The Pi should now alert you that I2c will be enabled after reboot. It will then ask if you want it to be loaded by default. Select `Yes` if you plan on using I2c everytime the raspberry pi boots up.

now we want to make sure it has successfully enabled the necessary modules. To this, enter the following command.

```powershell
lsmod | grep i2c_
```
