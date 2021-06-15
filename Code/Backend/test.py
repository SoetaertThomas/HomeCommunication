import time
import board
import busio
import adafruit_ccs811
i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus, address=0x5B)


while True:
    try:
        print(ccs811.eco2)
    except:
        print("error")
    time.sleep(0.5)
    

#print("TVOC: %1.0f PPM" % ccs811.tvoc)
#print("Temp: %0.1f C" % ccs811.temperature)
