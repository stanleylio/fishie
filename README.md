# fishie

Source code for Beaglebone/RPi -based data loggers, shore base-stations and web server.
Software developed for the Coastal Environment Monitoring project at SOEST of the University of Hawaii at Manoa.

In addition to the logger core logic, it contains Python driver/parser for various sensors and devices:

- Aanderaa 3835 (lab grade oxygen optode)
- Aanderaa 4330f (lab grade oxygen optode)
- WET Labs ECO FLNTU (Turbidity/Fluorescence sensor)
- MS5803-14BA (Water Pressure/Temperature)
- BMP180 (Barometric Pressure/Temperature; code from Adafruit)
- BME280 (Barometric Pressure/Temperature/Humidity; code from Adafruit)
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
