import serial

class QSerial(serial.Serial):
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout):
        try:
            super(QSerial, self).__init__()
            self.port = port
            self.baudrate = baudrate
            self.bytesize = bytesize
            self.parity = parity
            self.stopbits = stopbits
            self.timeout = timeout
            self.open()
            print(" Connect to %s, %d, %d, %s, %d, %d", port, baudrate, bytesize, parity, stopbits, timeout)
        except:
            print(" Connect to %s, %d, %d, %s, %d, %d error !", port, baudrate, bytesize, parity, stopbits, timeout)

    # def __del__(self):
    #     self.close()
    #     print(" Serial closed")
        
    def send(self, wdata):
        return self.write(wdata.encode("UTF-8"))
        
    def recv(self, nbyte):
        return self.read(nbyte)
