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

    # loop through all colors
    for r in range(8):
        for g in range(8):
            for b in range(8):
                for a in range(8):
                    string = ':0104 %i %i %i %i\r\n' % (r * 1000 + 1000,
                                                        g * 1000 + 1000,
                                                        b * 1000 + 1000,
                                                        a * 1000 + 1000)
                    ser.write(string)

                    # serial.flush() - waits until all data is written
                    ser.flush()
                    
                    # cps - characters per second
                    # we cannot send characters faster than
                    # hardware can accept, we must enter a delay,
                    # which is set according to baudrate
                    # cps = float(ser.baudrate / (len(string) * 10))
                    # print string, ser.readline(), 1.0 / cps
                    # print string, 1.0 / cps
                    # time.sleep(1.0 / cps)
    ser.close()
