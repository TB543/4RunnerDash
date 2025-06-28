todo add hardware list here and hardware installation guide 
# 4RunnerDash Setup Guide for Raspberry Pi 5

## Prerequisites
- Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

## Flashing the Raspberry Pi OS Lite (64-bit)
1. Open Raspberry Pi Imager.
2. Select **Raspberry Pi 5** as the device.
3. Choose OS:
   - Select **Raspberry Pi OS (Other)** -> **Raspberry Pi OS Lite (64-bit)**.
4. Select the storage device to flash to.
5. Modify settings:
   - Create your username and password.
   - Configure Wireless LAN settings.
   - Other options can be left as default.
6. Wait for the flashing process to complete.

## Initial Boot and Configuration
1. Boot the Raspberry Pi and wait for the initial setup to finish.
2. Log in using the username and password you set during flashing.
3. Run the configuration tool:
    ```bash
    sudo raspi-config
    ```
4. Navigate to **System Options** -> **Auto Login** and enable it.
5. Optionally you can also disable screen sleeping after 10 mins in **Display Options -> Screen Blanking**

> **Note:** Sometimes you may need to change the WLAN Country and reconnect to Wi-Fi for proper internet connectivity, even if it was set during flashing. This can be done in **Localization Options -> WLAN Country** and **System Options -> Wireless LAN**

## Installing and Running 4RunnerDash
1. Install Git:
    ```bash
    sudo apt install -y git
    ```
2. Clone the 4RunnerDash repository:
    ```bash
    git clone https://github.com/TB543/4RunnerDash
    ```
3. Change into the resources directory:
    ```bash
    cd 4RunnerDash/resources
    ```
4. Run the setup script:
    ```bash
    ./setup.sh
    ```
5. When the setup is finished it will display a list of connected devices like so:
    ```bash
    N: Name="pwr_button"
    N: Name="QDTECH̐MPI700 MPI7002"
    N: Name="vc4-hdmi-0"
    N: Name="vc4-hdmi-0 HDMI Jack"
    N: Name="vc4-hdmi-1"
    N: Name="vc4-hdmi-1 HDMI Jack"
    ```
    It will ask you to copy and paste the device for the touch screen. So in my case it would be **QDTECH̐MPI700 MPI7002**.

6. The Raspberry Pi will automatically reboot and start the program.
