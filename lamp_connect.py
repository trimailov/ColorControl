import serial
import time

ser = serial.Serial()
ser.port = '/dev/tty.LUME20R_130426-DevB'
ser.timeout = 1

ser.open()

print ser

if ser.isOpen():
    ser.write(':0104 0000 0000 0000 0000\r\n')
    print ser.readline()
    time.sleep(1)
    for r in range(18):
        for g in range(18):
            for b in range(18):
                for a in range(18):
                    string = ':0104 %i %i %i %i\r\n' % (r * 500 + 1000,
                                                        g * 500 + 1000,
                                                        b * 500 + 1000,
                                                        a * 500 + 1000)
                    ser.write(string)
                    print string

                    # characters per second
                    cps = float(ser.baudrate / len(string))
                    time.sleep(1.0 / cps)
    ser.close()
