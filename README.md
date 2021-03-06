# Coastal Monitoring at the University of Manoa

Source code for Beaglebone/RPi -based data loggers, shore base-stations and web server.
Software developed for the Coastal Environment Monitoring project at SOEST of the University of Hawaii at Manoa.

Project website: https://grogdata.soest.hawaii.edu/project_info/

In addition to communication and control logic, it contains Python driver/parser for these sensors/loggers:

- Aanderaa 3835 (oxygen optode)
- Aanderaa 4330F (oxygen optode)
- Aanderaa 4531D (oxygen optode)
- Aanderaa 4319A (conductivity/salinity sensor)
- Seabird CTD 16plusV2
- SeaFET pH sensor
- WET Labs ECO FLNTUS (Turbidity/Fluorescence sensor)
- MS5803-14BA (Water pressure and temperature)
- BMP280 (Barometric pressure and temperature)
- BME280 (Barometric pressure, temperature and humidity; code from Adafruit)
- BMP180 (Barometric pressure and temperature; code from Adafruit)
- Atlas Scientific EZO series sensors
  - Electrical Conductivity
  - Dissolved Oxygen
  - pH
  - Oxidation Reduction Potential
- Si1145 (IR/UV/visible light sensor)
- TSL2591 (high dynamic range IR/visible light sensor)
- TCS34725 (RGB light sensor)
- 20x4 LCD display with PCF8574T I2C I/O expander
- HTU21D (Humidity/Temperature sensor; code from Adafruit)
- MCP9808 (Temperature sensor; code from Adafruit)
- ... as well as several custom AVR-based sensors.
