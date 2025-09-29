# 4RunnerDash Setup Guide for Raspberry Pi 5

## Project Demo
- https://youtu.be/KCUJW72areY

## Hardware List
- [RaspBerry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/)
    - [Raspberry Pi SD Card](https://www.raspberrypi.com/products/sd-cards/) 
    - [Cooling fan](https://www.raspberrypi.com/products/active-cooler/) and [Case](https://www.raspberrypi.com/products/raspberry-pi-5-case/) recommended

- Raspberry Pi USB connections
    - [External Storage](https://www.amazon.com/BUFFALO-External-SSD-USB-%E2%80%8E%E2%80%8ESSD-PUT1-0U3B/dp/B0932C6G8Z?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&gQT=1&th=1) for map data (can buy larger storage for more map data or ignore if you bought a large enough [Raspberry Pi SD Card](https://www.raspberrypi.com/products/sd-cards/))
    - [OBD Scanner](https://www.amazon.com/dp/B005ZWM0R4?ref=ppx_yo2ov_dt_b_fed_asin_title)

- [CarPiHAT PRO 5](https://thepihut.com/products/carpihat-pro-5-car-interface-dac-for-raspberry-pi-5) with hardware:
    - [Additional Output Cable Connection](https://thepihut.com/products/4-way-molex-nano-fit-pigtail) (you will need at least 3)
    - [Ribbon Cable](https://www.amazon.com/dp/B0DQ4X6QP4?ref=ppx_yo2ov_dt_b_fed_asin_title) (only needed if you have a [cooling fan](https://www.raspberrypi.com/products/active-cooler/) and/or [case](https://www.raspberrypi.com/products/raspberry-pi-5-case/))
    - [GPIO Breakout Board](https://www.amazon.com/dp/B0DMNJ17PD?ref=ppx_yo2ov_dt_b_fed_asin_title)

- [Touch Screen Display](https://www.amazon.com/Waveshare-7inch-Capacitive-Raspberry-BeagleBone/dp/B01HPV7KL8?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A50C560NZEBBE&gQT=2)
    - [HDMI Cable](https://www.amazon.com/dp/B07R9RXWM5?ref=ppx_yo2ov_dt_b_fed_asin_title) and [Power/Data Cable](https://www.amazon.com/dp/B096YDCSCW?ref=ppx_yo2ov_dt_b_fed_asin_title) (Bent to fit in dashboard)

- [Raspberry Pi Camera](https://www.amazon.com/Arducam-Raspberry-Megapixel-Compatible-RPI-CAM-8MP/dp/B09V576TFN/ref=sr_1_8?crid=1XSXDIDRFGLJY&dib=eyJ2IjoiMSJ9.-i-FiCoFLNq2ZhrYWlV2SGi3t2xVcyp-7iol05jW6V5ktZ29SD_EA4_O4JOd0VBBrufxMJN3LXNAeirDeeI9olRw_3fytO_HNwF7YNcNHP5i3tzAFuq1n7wyWtqBYlqqMfMb6ee0AmdxSEwaxADrTVhlbAozn9iXg_6io711ITl2l5oGXCE-g2AlBb0531i-5hTVup71roAhsQqe_zwPpAxLyLNrWkK-AtvzcG_09uc.rg-oPRNfF4mJnslU996ovT4iHgtfCcFC1B-MjpvxENg&dib_tag=se&keywords=raspberry%2Bpi%2B5%2Bcamera&qid=1759162264&sprefix=raspberry%2Bpi%2B5%2Bcamera%2Caps%2C112&sr=8-8&th=1)
    - [Ribbon to HDMI](https://www.amazon.com/gp/product/B06XDNBM63/ref=ewc_pr_img_2?smid=A2IAB2RW3LLT8D&th=1) recommended for durability + longer cable

- [GPS Module](https://www.amazon.com/dp/B0F2DP1189?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) and [Antenna](https://www.amazon.com/dp/B083D59N55?ref=ppx_yo2ov_dt_b_fed_asin_title)
    - [Ground Plate](https://www.amazon.com/dp/B07PJLC74M?ref=ppx_yo2ov_dt_b_fed_asin_title) recommended

- [Compass Module](https://www.amazon.com/dp/B0C5XY3J3B?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)

- [Temperature Sensor](https://www.amazon.com/WWZMDiB-DHT11-Digital-Temperature-Humidity/dp/B0BG4DX7GD/ref=sr_1_3?dib=eyJ2IjoiMSJ9.Rm43YOiOnwbBoItkph1HMyjRnbPB7BPlljHwZ8US1Rhc74E_dDDXLAAJsshvDa_tzk3RUzZ5emO9eB8d0ij-5JexwoRfBLVWZmoRqjhfsuw9KnoK3HQLsPgTD2SxuxiSBMOT7-2G794_ZHyK6HkP-R6iD479Q5jokCLTvGTNR3o0KZWmQ8uGLZRTskWufHVGclcXXp9CfMQjG3MPAp3KJxtv5YuEstEz574yiEjEXo0.waI64ejL5yRXbRtBf1vZ6BeuLCUFCx67a5M2RJfkmrk&dib_tag=se&keywords=dht11&qid=1759161931&sr=8-3)
  - Note: this is a 3 pack, only 1 is needed

- [Volume Control Knob](https://www.amazon.com/Potentiometer-Electronic-Component-Precision-Performance/dp/B0F3373LRJ/ref=sr_1_10?crid=3NT5UM3AASOTS&dib=eyJ2IjoiMSJ9.sOk1-wHZoEsHbT9sww5-eTcs7kLURlHPQDu32Zopsp_M0nh8D1t9AphItKT4DfvBC9EjGKqu4E5ClB6qzfBEa3mF7iIAoZWCxZdNyRlBAfn4bS5LRXRSb37jxgyau72E2B2Szs1IEgCUerQgR4KJGa_SYu0yF2brxKhfVp8Buw46Aj1vfYmXYRWIHMxnS6_JBvke5gHbcZHNw0_gzfm71sq-i1wGv5bjLvDBx7Or5s_qr5y5dUqID3f8CKEqa6SY5Hbq_g8FRXflafG9ZO0EniaM0_BimHO1H-hccX30ONU.1osesHRaXaTz7vxy3QwQ4DMCBwCbhlYDmOEIRgL7lcU&dib_tag=se&keywords=hw-040+cap&qid=1759162407&s=electronics&sprefix=hw-040+cap%2Celectronics%2C75&sr=1-10)
  - Note: the KY-040 might also work and might be cheeper, but has not been tested

- [Car Amp Head Unit Connection](https://www.amazon.com/dp/B0DQTPDZK4?ref=ppx_yo2ov_dt_b_fed_asin_title)
    - **Note:** This is for a 2002 Toyota 4Runner, make sure you buy the correct connection for your car.

- Additional audio converters
    - [AUX to RCA](https://www.amazon.com/dp/B0BRYD7NJ6?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)
    - [RCA Splitters](https://www.amazon.com/dp/B0916WWN9Z?ref=ppx_yo2ov_dt_b_fed_asin_title)
    - [Ground Loop Isolator](https://www.amazon.com/dp/B019393MV2?ref=ppx_yo2ov_dt_b_fed_asin_title) (only needed if you have issues with static)

- [USB Breakout Cable](https://www.amazon.com/gp/product/B07DL2FP5C/ref=ewc_pr_img_1?smid=A2OQYP5S7I3UUC&th=1)
  - Not required, but useful if you want to connect to the Pi easily

## Software Installation Prerequisites
- Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
- Create [Spotify for Developers App](https://developer.spotify.com/dashboard)

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

>**Note:** Whatever name you give the Pi will be the name of the bluetooth connection to the Pi.

## Initial Boot and Configuration
1. Plug the SD card into the Pi, boot the Raspberry Pi and wait for the initial setup to finish.
2. Log in using the username and password you set during flashing.
3. Run the configuration tool:
    ```bash
    sudo raspi-config
    ```
4. Navigate to **System Options** -> **Auto Login** and enable it.
5. Navigate to **Interface Options** -> **Serial Port** and disable login shell over serial and enable serial hardware.
6. Navigate to **Interface Options** -> **I2C** and enable I2C.
7. Optionally you can also disable screen sleeping after 10 mins in **Display Options -> Screen Blanking**

> **Note:** Sometimes you may need to change the WLAN Country and reconnect to Wi-Fi for proper internet connectivity, even if it was set during flashing. This can be done in **Localization Options -> WLAN Country** and **System Options -> Wireless LAN**. Make sure if your internet/password ever changes you update this setting to ensure software updates and album art continues to work. 

## Software Installation
1. Install Git:
    ```bash
    sudo apt install -y git
    ```

2. Clone the latest release from the 4RunnerDash repository:
    ```bash
    git clone --branch $(curl -s https://api.github.com/repos/TB543/4RunnerDash/releases/latest | grep -Po '"tag_name": "\K.*?(?=")') https://github.com/TB543/4RunnerDash
    ```

3. Change into the resources directory:
    ```bash
    cd 4RunnerDash/resources
    ```
    
4. Run the setup script:
    ```bash
    ./setup_boot.sh
    ```

    it will display a list of connected devices like so:
    ```bash
    N: Name="pwr_button"
    N: Name="QDTECH̐MPI700 MPI7002"
    N: Name="vc4-hdmi-0"
    N: Name="vc4-hdmi-0 HDMI Jack"
    N: Name="vc4-hdmi-1"
    N: Name="vc4-hdmi-1 HDMI Jack"
    ```

    It will ask you to copy and paste the device for the touch screen. So in my case it would be **QDTECH̐MPI700 MPI7002**.

    Lastly, you will be asked for your [Spotify API](https://developer.spotify.com/dashboard) client ID and client secret. This is needed for viewing album art in the music menu.

    >**Note:** If you set up ssh keys and ssh from desktop it will be easier to copy and paste.

5. Next you will need to plug in your [External Storage](https://www.amazon.com/BUFFALO-External-SSD-USB-%E2%80%8E%E2%80%8ESSD-PUT1-0U3B/dp/B0932C6G8Z?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&gQT=1&th=1) and run:
    ```bash
    ./format_drive.sh
    ```

    This will display a list of connected drives like so:
    ```bash
    NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
    sda           8:0    0 465.8G  0 disk 
    └─sda1        8:1    0 465.8G  0 part /home/usr/4RunnerDash/src/AppData/map_data
    mmcblk0     179:0    0 119.1G  0 disk 
    ├─mmcblk0p1 179:1    0   512M  0 part /boot/firmware
    └─mmcblk0p2 179:2    0 118.6G  0 part /
    ```

    copy and paste the external drive that you will use to store your map data, for me it would be **sda1**.

    >**Note:** You can skip this step if your OS drive has enough storage for the map data (you will need about 200 GB of free space for US map data).

6. Next run the dependency install script:
    ```bash
    ./install_dependencies.sh
    ```
    it will first install rust. You can proceed with standard installation by pressing enter when prompted

7. Lastly, run the map install script:
    ```bash
    ./install_map.sh
    ```

    This will take a really long time to run (sometimes multiple weeks) as it has to download large map data files and format it but you do not to be present while it is running, just be patient. The Raspberry Pi will automatically shutdown when complete to not waste power.

    >**Note:** By default only the US map database is installed, but feel free to modify the install_map.sh file to change this.

8. The **4RunnerDash/src/AppData/__init__.py** file contains configuration settings that can be changed as needed to fit your car/hardware. These settings include:

    - Pi screen resolution
    - FPS option
    - Max volume percentage
    - Number of cached album art images
    - Album art image resolution
    - Map tile resolution
    - Data for how often various car parts/fluids should be replaced
    - Car gas tank capacity

    feel free to modify based on your needs and the dashboard will reflect these changes.

## Hardware Installation
>**Note:** Make sure software installation has completed before continuing to hardware installation.

1. Connect the [Ribbon Cable](https://www.amazon.com/dp/B0DQ4X6QP4?ref=ppx_yo2ov_dt_b_fed_asin_title) to the [RaspBerry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) and the [GPIO Breakout Board](https://www.amazon.com/dp/B0DMNJ17PD?ref=ppx_yo2ov_dt_b_fed_asin_title)

2. Connect the [Raspberry Pi Camera](https://www.amazon.com/Arducam-Raspberry-Megapixel-Compatible-RPI-CAM-8MP/dp/B09V576TFN/ref=sr_1_8?crid=1XSXDIDRFGLJY&dib=eyJ2IjoiMSJ9.-i-FiCoFLNq2ZhrYWlV2SGi3t2xVcyp-7iol05jW6V5ktZ29SD_EA4_O4JOd0VBBrufxMJN3LXNAeirDeeI9olRw_3fytO_HNwF7YNcNHP5i3tzAFuq1n7wyWtqBYlqqMfMb6ee0AmdxSEwaxADrTVhlbAozn9iXg_6io711ITl2l5oGXCE-g2AlBb0531i-5hTVup71roAhsQqe_zwPpAxLyLNrWkK-AtvzcG_09uc.rg-oPRNfF4mJnslU996ovT4iHgtfCcFC1B-MjpvxENg&dib_tag=se&keywords=raspberry%2Bpi%2B5%2Bcamera&qid=1759162264&sprefix=raspberry%2Bpi%2B5%2Bcamera%2Caps%2C112&sr=8-8&th=1) to the [RaspBerry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) via the [Ribbon to HDMI](https://www.amazon.com/gp/product/B06XDNBM63/ref=ewc_pr_img_2?smid=A2IAB2RW3LLT8D&th=1) and an HDMI cable
    - [Heres a video to help](https://www.youtube.com/watch?v=lAbpDRy-gc0)

3. Connect the [GPS Module](https://www.amazon.com/dp/B0F2DP1189?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) to the [GPIO Breakout Board](https://www.amazon.com/dp/B0DMNJ17PD?ref=ppx_yo2ov_dt_b_fed_asin_title):
    - VCC -> [GPIO-4](https://pinout.xyz/pinout/5v_power)
    - Ground -> [GPIO-6](https://pinout.xyz/pinout/ground)
    - TX -> [GPIO-10](https://pinout.xyz/pinout/pin10_gpio15/)
    - RX connection is not needed

4. Connect the [Volume Control Knob](https://www.amazon.com/Potentiometer-Electronic-Component-Precision-Performance/dp/B0F3373LRJ/ref=sr_1_10?crid=3NT5UM3AASOTS&dib=eyJ2IjoiMSJ9.sOk1-wHZoEsHbT9sww5-eTcs7kLURlHPQDu32Zopsp_M0nh8D1t9AphItKT4DfvBC9EjGKqu4E5ClB6qzfBEa3mF7iIAoZWCxZdNyRlBAfn4bS5LRXRSb37jxgyau72E2B2Szs1IEgCUerQgR4KJGa_SYu0yF2brxKhfVp8Buw46Aj1vfYmXYRWIHMxnS6_JBvke5gHbcZHNw0_gzfm71sq-i1wGv5bjLvDBx7Or5s_qr5y5dUqID3f8CKEqa6SY5Hbq_g8FRXflafG9ZO0EniaM0_BimHO1H-hccX30ONU.1osesHRaXaTz7vxy3QwQ4DMCBwCbhlYDmOEIRgL7lcU&dib_tag=se&keywords=hw-040+cap&qid=1759162407&s=electronics&sprefix=hw-040+cap%2Celectronics%2C75&sr=1-10) to the [GPIO Breakout Board](https://www.amazon.com/dp/B0DMNJ17PD?ref=ppx_yo2ov_dt_b_fed_asin_title)
    - CLK -> [GPIO-26](https://pinout.xyz/pinout/pin37_gpio26/)
    - DT -> [GPIO-6](https://pinout.xyz/pinout/pin31_gpio6/)
    - SW -> [GPIO-5](https://pinout.xyz/pinout/pin29_gpio5/)
    - VCC -> [GPIO-17](https://pinout.xyz/pinout/3v3_power)
    - GND -> [GPIO-25](https://pinout.xyz/pinout/ground)

5. Connect the [GPIO Breakout Board](https://www.amazon.com/dp/B0DMNJ17PD?ref=ppx_yo2ov_dt_b_fed_asin_title) to the [CarPiHAT PRO 5](https://thepihut.com/products/carpihat-pro-5-car-interface-dac-for-raspberry-pi-5)

6. Connect the [Compass Module](https://www.amazon.com/dp/B0C5XY3J3B?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) to the [CarPiHAT PRO 5](https://thepihut.com/products/carpihat-pro-5-car-interface-dac-for-raspberry-pi-5) via the [Output Cable](https://thepihut.com/products/4-way-molex-nano-fit-pigtail)
   - SCL -> [CarPiHat I2C](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pin 1
   - SDA -> [CarPiHat I2C](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pin 2
   - GND -> [CarPiHat I2C](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pin 3
   - VCC -> [CarPiHat I2C](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pin 4
   - INT connection is not needed

7. Connect the [Temperature Sensor](https://www.amazon.com/WWZMDiB-DHT11-Digital-Temperature-Humidity/dp/B0BG4DX7GD/ref=sr_1_3?dib=eyJ2IjoiMSJ9.Rm43YOiOnwbBoItkph1HMyjRnbPB7BPlljHwZ8US1Rhc74E_dDDXLAAJsshvDa_tzk3RUzZ5emO9eB8d0ij-5JexwoRfBLVWZmoRqjhfsuw9KnoK3HQLsPgTD2SxuxiSBMOT7-2G794_ZHyK6HkP-R6iD479Q5jokCLTvGTNR3o0KZWmQ8uGLZRTskWufHVGclcXXp9CfMQjG3MPAp3KJxtv5YuEstEz574yiEjEXo0.waI64ejL5yRXbRtBf1vZ6BeuLCUFCx67a5M2RJfkmrk&dib_tag=se&keywords=dht11&qid=1759161931&sr=8-3) to the [CarPiHAT PRO 5](https://thepihut.com/products/carpihat-pro-5-car-interface-dac-for-raspberry-pi-5) via the [Output Cable](https://thepihut.com/products/4-way-molex-nano-fit-pigtail)
   - OUT -> [CarPiHat 1 Wire](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pin 2
   - GND -> [CarPiHat 1 Wire](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pin 3
   - VCC -> [CarPiHat 1 Wire](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pin 4

8. Remove the car radio. [Here is a guide for a 2002 Toyota 4Runner](https://www.youtube.com/watch?v=AbdoAcwrbJ8) (Only Remove the radio, not the amp)

9. Connect your [Car Amp Head Unit Connection](https://www.amazon.com/dp/B0DQTPDZK4?ref=ppx_yo2ov_dt_b_fed_asin_title) and wire everything as follows:
    - 12V const, 12V switch, ILUM and Grounds to [CarPiHAT Main Loom](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pins 3, 5, 2 and 4 respectfully
    - AMP control and Grounds to [CarPiHat 12V Output](https://cdn.shopify.com/s/files/1/0176/3274/files/Datasheet_latest.png?v=1647017344) pins 1 and 2
    - Stereo audio to AUX cable with audio cables
    - AUX Cable to to [CarPiHAT PRO 5](https://thepihut.com/products/carpihat-pro-5-car-interface-dac-for-raspberry-pi-5) DAC port

10. Plug in your [OBD Scanner](https://www.amazon.com/dp/B005ZWM0R4?ref=ppx_yo2ov_dt_b_fed_asin_title) to the OBD port on your car (usually bottom right of the steering wheel) and wire the USB connection into the slot where the radio used to be and into the [RaspBerry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) along with all of the other usb connections

11. Connect the [Antenna](https://www.amazon.com/dp/B083D59N55?ref=ppx_yo2ov_dt_b_fed_asin_title) to the [GPS Module](https://www.amazon.com/dp/B0F2DP1189?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) and mount the antenna on the [Ground Plate](https://www.amazon.com/dp/B07PJLC74M?ref=ppx_yo2ov_dt_b_fed_asin_title) and wire to the roof of the car.

12. Connect the [HDMI Cable](https://www.amazon.com/dp/B07R9RXWM5?ref=ppx_yo2ov_dt_b_fed_asin_title) and [Power/Data Cable](https://www.amazon.com/dp/B096YDCSCW?ref=ppx_yo2ov_dt_b_fed_asin_title) to the [Touch Screen Display](https://www.amazon.com/Waveshare-7inch-Capacitive-Raspberry-BeagleBone/dp/B01HPV7KL8?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=A50C560NZEBBE&gQT=2) and shove everything into the radio slot

13. Route the [USB Breakout Cable](https://www.amazon.com/gp/product/B07DL2FP5C/ref=ewc_pr_img_1?smid=A2OQYP5S7I3UUC&th=1) and [Volume Control Knob](https://www.amazon.com/Potentiometer-Electronic-Component-Precision-Performance/dp/B0F3373LRJ/ref=sr_1_10?crid=3NT5UM3AASOTS&dib=eyJ2IjoiMSJ9.sOk1-wHZoEsHbT9sww5-eTcs7kLURlHPQDu32Zopsp_M0nh8D1t9AphItKT4DfvBC9EjGKqu4E5ClB6qzfBEa3mF7iIAoZWCxZdNyRlBAfn4bS5LRXRSb37jxgyau72E2B2Szs1IEgCUerQgR4KJGa_SYu0yF2brxKhfVp8Buw46Aj1vfYmXYRWIHMxnS6_JBvke5gHbcZHNw0_gzfm71sq-i1wGv5bjLvDBx7Or5s_qr5y5dUqID3f8CKEqa6SY5Hbq_g8FRXflafG9ZO0EniaM0_BimHO1H-hccX30ONU.1osesHRaXaTz7vxy3QwQ4DMCBwCbhlYDmOEIRgL7lcU&dib_tag=se&keywords=hw-040+cap&qid=1759162407&s=electronics&sprefix=hw-040+cap%2Celectronics%2C75&sr=1-10) to the respective slots on the mount and connect to the car

>**Note:** The [Temperature Sensor](https://www.amazon.com/WWZMDiB-DHT11-Digital-Temperature-Humidity/dp/B0BG4DX7GD/ref=sr_1_3?dib=eyJ2IjoiMSJ9.Rm43YOiOnwbBoItkph1HMyjRnbPB7BPlljHwZ8US1Rhc74E_dDDXLAAJsshvDa_tzk3RUzZ5emO9eB8d0ij-5JexwoRfBLVWZmoRqjhfsuw9KnoK3HQLsPgTD2SxuxiSBMOT7-2G794_ZHyK6HkP-R6iD479Q5jokCLTvGTNR3o0KZWmQ8uGLZRTskWufHVGclcXXp9CfMQjG3MPAp3KJxtv5YuEstEz574yiEjEXo0.waI64ejL5yRXbRtBf1vZ6BeuLCUFCx67a5M2RJfkmrk&dib_tag=se&keywords=dht11&qid=1759161931&sr=8-3) and [Compass Module](https://www.amazon.com/dp/B0C5XY3J3B?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) should be routed somewhere in the cabin so that the readings can be more accurate. Additionally, make sure the compass is mounted in the correct orientation (there should be an xyz axis printed on the module. mount the x-axis to face the front of the car).

## Power Usage

The Pi will automatically boot up when the car is turned on so there is no need to worry about powering it up manually. Additionally the Pi will automatically shutdown 5 seconds after the car is turned off. This 5 second delay is to prevent a reboot when switched from car battery to engine power. When the Pi is off it will draw a negligible amount of power and will not drain the car battery.

## Software Updates

Each time the Pi is booted up and connected to the internet (in your driveway) it will automatically check the GitHub repository to see if a new update is available. If there is, there will be a notification on the main menu to install it via the settings menu. When installing the update, make sure that you stay within range of your internet router to ensure all update files can properly download. When the update is complete, the Pi will reboot and display the patch notes for the update. If an update ever adds additional hardware or breaks your current hardware you can visit this github page for more info or revert to a previous version via the command:
```bash
git checkout <version num>
```
where "version num" is the release you wish to go back to. For example "v1.0.0".

## Album Art Handling

Due to limitations in Bluetooth protocols, album art cannot be transferred directly from connected devices. As a result, this dashboard uses the **Spotify Web API** to fetch album artwork and metadata in real time.

To ensure smooth performance and offline capability:

- **Album art is cached** locally for every track played while connected to the internet and with music menu open.
- If a track is played while offline or without image data, its metadata is **queued for caching**.
- On the next internet-connected session, the app will automatically fetch and save any missing album art for previously played tracks.

This approach ensures a seamless user experience, with album visuals displayed even when the device is offline, after being seen once online.

## Maps Credits

Map data from [©OpenStreetMap](https://www.openstreetmap.org/) contributors, available under the [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/) downloaded from [GeoFabrik](https://download.geofabrik.de/).

Navigation is powered by [GraphHopper](https://www.graphhopper.com/), an open-source routing engine.

Address search is provided by [Nominatim](https://nominatim.org/).

Map tiles generated with [TileMaker](https://github.com/systemed/tilemaker) and rendered with [TileServer-GL](https://github.com/maptiler/tileserver-gl).
