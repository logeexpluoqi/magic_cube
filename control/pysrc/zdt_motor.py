import serial

class ZdtMotor(serial.Serial):
    
    def __init__(self, port, id, timeout):
        self.id = id
        try:
            super().__init__(port, 115200, 8, "N", 1, timeout)
            if self.is_open:
                self._close()
                self.is_open = False
            self.open()
            self.err = 0
            print(" Connect to %s, %d, %d, %s, %d, %d", port, self.baudrate,
                self.bytesize, self.parity, self.stopbits, self.timeout)
            
            self.ischeck = False
            self.pos = 0
            self.pul = 0
            self.ena = 0
            self.enc = 0
            self.perr = 0
            self.lock = 0
            self.zero_state = 0
        except:
            print(" serial open error !")

    def _send(self, data):
        self.write(data)

    def _recv(self, size):
        try:
            return self.read(size)
        except:
            print(" recv error !")

    def ischeck(self, state):
        self.ischeck = state

    def encoder_check(self):
        self._send(bytes([self.id, 0x06, 0x45, 0x6b]))
        if (self.ischeck == True):
            buf = self._recv(3)
            if buf[1] == 0x02:
                self.err = 0
            elif buf[1] == 0xee:
                self.err = 0xee
            else:
                self.err = 0
            
    def zero_set(self):
        self._send(bytes([self.id, 0x0a, 0x6d, 0x6b]))
        if (self.ischeck == True):
            buf = self._recv(3)
            if buf[1] == 0x02:
                self.err = 0
            elif buf[1] == 0xee:
                self.err = 0xee
            else:
                self.err = 0
        
    def relieve_lock_protect(self):
        self._send(bytes([self.id, 0x0e, 0x52, 0x6b]))
        if (self.ischeck == True):
            buf = self._recv(3)
            if buf[1] == 0x02:
                self.err = 0
            elif buf[1] == 0xee:
                self.err = 0xee
            else:
                self.err = 0
        
    def read_enc(self):
        self._send(bytes([self.id, 0x30, 0x6b]))
        try:
            data = self._recv(4)
            self.enc = (int(data[1]) << 8) | data[2]
        except:
            print(" recv error !")
        
    def read_pul(self):
        self._send(bytes([self.id, 0x33, 0x6b]))
        try:
            data = self._recv(6)
            self.pul = (int(data[1]) << 24) | (int(data[2]) << 16) | (int(data[3]) << 8) | data[4]
        except:
           print(" recv error !")
            
    def read_pos(self):
        self._send(bytes([self.id, 0x36, 0x6b]))
        try:
            data = self._recv(6)
            self.pos = (int(data[1]) << 24) | (int(data[2]) << 16) | (int(data[3]) << 8) | data[4]
        except:
            print(" recv error !")
        
    def read_perr(self):
        self._send(bytes([self.id, 0x39, 0x6b]))
        try:
            data = self._recv(4)
            self.perr = (int(data[1]) << 24) | data[2]
        except:
            print(" recv error !")
        
    def read_ena(self):
        self._send(bytes([self.id, 0x3a, 0x6b]))
        try:
            data = self._recv(3)
            self.ena = data[1]
        except:
            print(" recv error !")
        
    def read_lock(self):
        self._send(bytes([self.id, 0x3e, 0x6b]))
        try:
            data = self._recv(3)
            self.lock = data[1]
        except:
            print(" recv error !")
        
    def read_auto_zero(self):
        self._send(bytes([self.id, 0x3f, 0x6b]))
        try:
            data = self._recv(3)
            self.zero_state = data[1]
        except:
            print(" recv error !")
        
    def div_set(self, div):
        self._send(bytes([self.id, 0x84, div, 0x6b]))
        if (self.ischeck == True):
            try:
                buf = self._recv(3)
                if buf[1] == 0x02:
                    self.err = 0
                elif buf[1] == 0xee:
                    self.err = 0xee
                else:
                    self.err = 0
            except:
                print(" recv error !")
        
    def id_set(self, id):
        self._send(bytes([self.id, 0xae, id, 0x6b]))
        if (self.ischeck == True):
            try:
                buf = self._recv(3)
                if buf[1] == 0x02:
                    self.err = 0
                elif buf[1] == 0xee:
                    self.err = 0xee
                else:
                    self.err = 0
            except:
                print(" recv error !")
        
    def ena_set(self, state):
        self._send(bytes([self.id, 0xf3, state, 0x6b]))
        if (self.ischeck == True):
            try:
                buf = self._recv(3)
                if buf[1] == 0x02:
                    self.err = 0
                elif buf[1] == 0xee:
                    self.err = 0xee
                else:
                    self.err = 0
            except:
                print(" recv error !")
        
    def vel_set(self, vel, acc):
        if (vel > 1279):
            vel = 1279
        elif (vel < -1279):
            vel = -1279
        
        if (acc > 255):
            acc = 255
        elif (acc < 0):
            acc = 0
        
        if (vel < 0):
            vel = vel | 0x1000
        
        self._send(bytes([self.id, 0xf6, (vel >> 8) & 0xff, vel & 0xff, acc, 0x6b]))
        if (self.ischeck == True):
            try:
                buf = self._recv(3)
                if buf[1] == 0x02:
                    self.err = 0
                elif buf[1] == 0xee:
                    self.err = 0xee
                else:
                    self.err = 0
            except:
                print(" recv error !")
    
    def pos_set(self, pos, vel, acc):
        if (vel > 1279):
            vel = 1279
        elif (vel < -1279):
            vel = -1279
        
        if (acc > 255):
            acc = 255
        elif (acc < 0):
            acc = 0
        
        if (vel < 0):
            vel = vel | 0x1000
            
        self._send(bytes([self.id, 0xfd, (vel >> 8) & 0xff, vel & 0xff, acc, (pos >> 16) & 0xff, (pos >> 8) & 0xff, pos & 0xff, 0x6b]))
        if (self.ischeck == True):
            try:
                buf = self._recv(3)
                if buf[1] == 0x02:
                    self.err = 0
                elif buf[1] == 0xee:
                    self.err = 0xee
                else:
                    self.err = 0
            except:
                print(" recv error !")
                
    def param_state(self, state):
        if state == "clear":
            cmd = 0xca
        elif state == "store":
            cmd = 0xc8
        self._send(bytes([self.id, 0xff, cmd,0x6b]))
        if (self.ischeck == True):
            try:
                buf = self._recv(3)
                if buf[1] == 0x02:
                    self.err = 0
                elif buf[1] == 0xee:
                    self.err = 0xee
                else:
                    self.err = 0
            except:
                print(" recv error !")
        