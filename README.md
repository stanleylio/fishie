# Coastal Monitoring at the University of Manoa

Source code for Beaglebone/RPi-based data loggers, shore internet gateways, and web server.
Software developed for the Coastal Environment Monitoring project at the University of Hawaii at Manoa.

Project website: https://grogdata.soest.hawaii.edu/project_info/

I'm using this mostly for synchronizing the software and configurations on our gateways, loggers, and servers; I'm not using this to track issues or updates. More like "Dropbox for source code" than "git for source control".

That said, the drivers/ folder does contain Python drivers/helpers for sensors commonly used in environmental/oceanographic monitoring projects that *might* be reusable:

- Oxygen optodes, salinity/conductivity, pH, plus various submersible, bulky, and/or expensive stuff
  - Aanderaa 3835 (Dissolved Oxygen)
  - Aanderaa 4330F (Dissolved Oxygen)
  - Aanderaa 4531D (Dissolved Oxygen)
  - Aanderaa 4319A (Conductivity/Salinity)
  - Seabird CTD 16plusV2
  - SeaFET/SeapHOx sensor (pH, DO, CTD)
  - WET Labs ECO FLNTUSB/FDOM (Chlorophyll/Turbidity/Fluorescent Dissolved Organic Matter)

- Temperature, humidity, pressure
  - TSYS01 (Temperature)
  - MS5803/MS5837 (Water pressure and temperature)
  - HTU21D (Humidity/Temperature sensor; code from Adafruit)
  - BMP280 (Barometric pressure and temperature)
  - BME280 (Barometric pressure, temperature and humidity; code from Adafruit)
  - BMP180 (Barometric pressure and temperature; code from Adafruit)
  - MCP9808 (Temperature; code from Adafruit)

- Light
  - VEML6030 (high dynamic range light sensor)
  - VEML6040 (RGB light sensor)
  - Si1145 (IR/UV/visible light sensor)
  - TSL2591 (high dynamic range IR/visible light sensor)
  - TCS34725 (RGB light sensor)

- Misc
  - Atlas Scientific EZO series sensors
    - Electrical Conductivity
    - Dissolved Oxygen
    - pH
    - Oxidation Reduction Potential
    - 20x4 LCD display with PCF8574T I2C I/O expander
