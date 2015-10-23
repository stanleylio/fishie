from Adafruit_HTU21D import HTU21D

class HTU21D_sl(HTU21D):
    def __init__(self):
        HTU21D.__init__(self)

    def read(self):
        t = self.readTemperatureData()
        rh = self.readHumidityData()
        return {'t':t,'rh':rh}

    def readTemperatureData(self):
        tmp = -255
        while -255 == tmp:
            tmp = super(HTU21D_sl,self).readTemperatureData()
        return round(tmp*1e2)/1e2

    def readHumidityData(self):
        tmp = -255
        while -255 == tmp:
            tmp = super(HTU21D_sl,self).readHumidityData()
        return round(tmp*1e2)/1e2


if '__main__' == __name__:
    import time
    htu = HTU21D_sl()

    while True:
        print htu.read()
        time.sleep(1)

