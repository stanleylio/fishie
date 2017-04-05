from __future__ import division
import smbus,time,struct


class SensorNotFoundException(Exception):
    pass


class BME280:
    def __init__(self,address=0x76,bus=1):
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.reset()

        if not self.check_ID():
            raise SensorNotFoundException

        self._read_compensation_parameters()
        # t: osr 2x; p: osr 2x; normal mode
        self.bus.write_byte_data(self.address,0xF4,0b01001011)  # see P.27

    def check_ID(self):
        return 0x60 == self.bus.read_byte_data(self.address,0xD0)

    def set_osr_p(self,osr=None):
        ctrl_meas = self.bus.read_byte_data(self.address,0xF4)

        if osr is None:
            osrs_p = {1:1,2:2,3:4,4:8,5:16}
            return osrs_p.get((ctrl_meas & 0b00011100) >> 2,16)
        else:
            osrs_p = {1:1,2:2,4:3,8:4,16:5}
            if osr not in osrs_p:
                raise ValueError('Valid oversampling rate: {1,2,4,8,16}')
            osrs_p = osrs_p[osr] << 2
            ctrl_meas = (ctrl_meas & 0b11100011) + osrs_p
            self.bus.write_byte_data(self.address,0xF4,ctrl_meas)
        
    def set_osr_t(self,osr=None):
        ctrl_meas = self.bus.read_byte_data(self.address,0xF4)

        if osr is None:
            osrs_t = {1:1,2:2,3:4,4:8,5:16}
            return osrs_t.get((ctrl_meas & 0b11100000) >> 5,16)
        else:
            osrs_t = {1:1,2:2,4:3,8:4,16:5}
            if osr not in osrs_t:
                raise ValueError('Valid oversampling rate: {1,2,4,8,16}')
            osrs_t = osrs_t[osr] << 5
            ctrl_meas = (ctrl_meas & 0b00011111) + osrs_t
            self.bus.write_byte_data(self.address,0xF4,ctrl_meas)

    def set_osr_h(self,osr=None):
        ctrl_meas = self.bus.read_byte_data(self.address,0xF2)

        if osr is None:
            osrs_h = {1:1,2:2,3:4,4:8,5:16}
            return osrs_h.get(ctrl_meas & 0b00000111,16)    # "others"
        else:
            osrs_h = {1:1,2:2,4:3,8:4,16:5}
            if osr not in osrs_h:
                raise ValueError('Valid oversampling rate: {1,2,4,8,16}')
            osrs_h = osrs_h[osr]
            ctrl_meas = (ctrl_meas & 0b11111000) | osrs_h
            self.bus.write_byte_data(self.address,0xF2,ctrl_meas)

    def set_filter(self,coef=None):
        config = self.bus.read_byte_data(self.address,0xF5)

        if coef is None:
            filter_coef = {0:0,1:2,2:4,3:8,4:16}
            return filter_coef[(config & 0b00011100) > 2]
        else:
            filter_coef = {0:0,2:1,4:2,8:3,16:4}
            if coef not in filter_coef:
                raise ValueError('Valid filter coefficient: {0(no filter),2,4,8,16}')
            filter_coef = filter_coef[coef] << 2
            config = (config & 0b11100011) + filter_coef
            self.bus.write_byte_data(self.address,0xF5,config)
    
    def read(self):
        for i in range(1000):
            status = self.bus.read_byte_data(self.address,0xF3)
            if not (status & (1 << 3)):
                #print i
                break
            else:
                time.sleep(0.001)
        C = [self.bus.read_byte_data(self.address,i) for i in range(0xF7,0xFC+1)]
        adc_P = ((C[0] << 16) + (C[1] << 8) + C[2]) >> 4
        adc_T = ((C[3] << 16) + (C[4] << 8) + C[5]) >> 4
        C = [self.bus.read_byte_data(self.address,i) for i in range(0xFD,0xFE+1)]
        adc_H = (C[0] << 8) + C[1]
        #print adc_P,adc_T,adc_H

        var1 = (adc_T/16384 - self.dig_T1/1024)*self.dig_T2
        var2 = (adc_T/131072 - self.dig_T1/8192)*(adc_T/131072 - self.dig_T1/8192)*self.dig_T3
        t_fine = var1 + var2
        T = round(t_fine/5120,3)

        var1 = t_fine/2 - 64000
        var2 = var1*var1*self.dig_P6/32768
        var2 = var2 + var1*self.dig_P5*2
        var2 = var2/4 + self.dig_P4*65536
        var1 = (self.dig_P3*var1*var1/524288 + self.dig_P2*var1)/524288
        var1 = (1 + var1/32768)*self.dig_P1
        p = 1048576 - adc_P
        p = (p - var2/4096)*6250/var1
        var1 = self.dig_P9*p*p/2147483648
        var2 = p*self.dig_P8/32768
        p = p + (var1 + var2 + self.dig_P7)/16
        P = round(p/1e3,3)

        #print self.dig_H1,self.dig_H2,self.dig_H3,self.dig_H4,self.dig_H5,self.dig_H6

        var_H = t_fine - 76800
        var_H = (adc_H - (self.dig_H4 * 64 + self.dig_H5/16384*var_H)) *\
                (self.dig_H2/65536 * (1.0 + self.dig_H6/67108864.0*var_H *\
                                               (1.0 + self.dig_H3/67108864.0*var_H)))
        var_H = var_H * (1.0 - self.dig_H1*var_H/524288.0)
        if var_H > 100:
            var_H = 100
        elif var_H < 0:
            var_H = 0
        RH = round(var_H,3)

        return {'t':T,'p':P,'rh':RH}    # Deg.C, kPa, %

    def reset(self):
        self.bus.write_byte_data(self.address,0xE0,0xB6)

    def _read_status(self):
        return self.bus.read_byte_data(self.address,0xF3)

    # if you are careful you can probably unpack the whole thing in one line...
    def _read_compensation_parameters(self):
        tmp = [self.bus.read_byte_data(self.address,i) for i in range(0x88,0x9F+1)]
        C = struct.unpack('<HhhHhhhhhhhh',''.join([chr(c) for c in tmp]))
        self.dig_T1 = C[0]
        self.dig_T2 = C[1]
        self.dig_T3 = C[2]
        
        self.dig_P1 = C[3]
        self.dig_P2 = C[4]
        self.dig_P3 = C[5]
        self.dig_P4 = C[6]
        self.dig_P5 = C[7]
        self.dig_P6 = C[8]
        self.dig_P7 = C[9]
        self.dig_P8 = C[10]
        self.dig_P9 = C[11]

        self.dig_H1 = self.bus.read_byte_data(self.address,0xA1)
        self.dig_H2 = self.bus.read_word_data(self.address,0xE1)
        self.dig_H3 = self.bus.read_byte_data(self.address,0xE3)

        e4 = self.bus.read_byte_data(self.address,0xE4)
        e5 = self.bus.read_byte_data(self.address,0xE5)
        self.dig_H4 = (e4 << 4) | (e5 & 0xF)

        #e5 = self.bus.read_byte_data(self.address,0xE5)
        e6 = self.bus.read_byte_data(self.address,0xE6)
        self.dig_H5 = ((e5 >> 4) & 0xF) | (e6 << 8)

        self.dig_H6 = self.bus.read_byte_data(self.address,0xE7)
        #return C


if '__main__' == __name__:
    
    b = BME280(bus=2)
    b.set_osr_p(4)
    b.set_osr_t(4)
    b.set_osr_h(4)
    b.set_filter(2)
    
    try:
        while True:
            print b.read()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print 'user interrupted'

