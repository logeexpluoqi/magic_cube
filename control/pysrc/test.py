import zdt_motor

motor = zdt_motor.ZdtMotor("COM16", 1, 10)

motor._send(bytes([0,1,2,4,5]))

print(motor._recv(10))

motor.close()
