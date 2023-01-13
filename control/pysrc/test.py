import qserial

ser = qserial.QSerial("COM5", 115200, 8, "N", 1, 0.5)

ser.send("asdfasdf")

print(ser.recv(5))
