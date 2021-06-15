import board
import busio
import adafruit_ccs811
import threading
import time
from datetime import datetime
from subprocess import call, check_output
import board
import neopixel
import spidev
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from RPi import GPIO
from smbus import SMBus

from repositories.DataRepository import DataRepository

# id_devices
id_luchtkwaliteitssensor = (DataRepository.get_id_device(
    "luchtkwaliteitssensor"))["id_device"]
id_rotary = (DataRepository.get_id_device("rotary encoder"))["id_device"]
id_neopixel = (DataRepository.get_id_device("neopixel"))["id_device"]
id_trilmotor = (DataRepository.get_id_device("trilmotor"))["id_device"]
id_buzzer = (DataRepository.get_id_device("buzzer speaker"))["id_device"]


# region hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# I2C
i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus, address=0x5B)
# i2c = SMBus()
# i2c.open(1)

# i2c.write_byte_data(0x5B, 0xF4, 0)
# i2c.write_byte_data(0x5B, 0x01, 0b00010000)


# i2c.write_byte_data(0x5B, 0x00, 0x01)
# i2c.write_i2c_block_data(0x5B, 0xFF, [0x11, 0xE5, 0x72, 0x8A])


# def getPPM():
#     register1 = waarde_i2c[0]
#     register2 = waarde_i2c[1]

#     register1 = register1 << 8
#     result = register1 | register2
#     print((result))


# while True:
#     waarde_i2c = i2c.read_i2c_block_data(0x5B, 0x02, 8)
#     print(waarde_i2c)
#     getPPM()
#     time.sleep(2)

# BUZZER
buzzer = 10

# neopixel
neopixel_input = 4
pixels = neopixel.NeoPixel(board.D18, 8)

# VIBRATION MOTOR
vib_motor = 21
# ROTARY ENCODER
clk = 22
dt = 27
counter = 1
re_btn = 11

# BUTTON
button = 13

# PIR SENSOR
PIR = 17

# SPI BUS
# spi = spidev.SpiDev()
# spi.open(0, 0)
# spi.max_speed_hz = 100000

# LCD DISPLAY
rs = 20
e = 16
backlight = 9
databits = [26, 19, 6, 5, 23, 24, 25, 12]

# SETUP
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(e, GPIO.OUT)
GPIO.setup(re_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(vib_motor, GPIO.OUT)
for bit in databits:
    GPIO.setup(bit, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk, GPIO.IN)
GPIO.setup(dt, GPIO.IN)
GPIO.setup(backlight, GPIO.OUT)
pwm = GPIO.PWM(backlight, 1000)
pwm.start(100)

# region display functies


def send_instruction(value):
    # rs laag: voor instruction
    GPIO.output(rs, GPIO.LOW)
    # enable hoog
    GPIO.output(e, GPIO.HIGH)
    set_data_bits(value)
    # enable terug laag
    GPIO.output(e, GPIO.LOW)
    time.sleep(0.01)


def send_character(character):
    # rs hoog: voor data
    GPIO.output(rs, GPIO.HIGH)
    # enable hoog
    GPIO.output(e, GPIO.HIGH)
    # data klaarzetten
    set_data_bits(character)
    # enable laag
    GPIO.output(e, GPIO.LOW)
    # wait
    time.sleep(0.002)


def set_data_bits(byte):
    mask = 0x80
    for i in range(8):
        GPIO.output(databits[i], byte & (mask >> i))


def write_message(message):
    for char in message[0:16]:
        send_character(ord(char))
    for char in message[16:]:
        move_screen()
        send_character(ord(char))


def init_LCD():
    # set datalengte op 8 bit (= DB4 hoog), 2 lijnen (=DB3), 5x7 display (=DB2).
    send_instruction(0b00111000)
    # display on (=DB2), cursor on (=DB1), blinking on (=DB0)
    send_instruction(0b00001111)
    # clear display en cursor home (DB0 hoog)
    send_instruction(0b00000001)


def set_cursor(row, col):
    # byte maken: row (0 of 1) = 0x0* voor rij 0 of 0x4* voor rij 1. col = 0x*0 - 0x*F
    byte = row << 6 | col
    # byte | 128 want DB7 moet 1 zijn
    send_instruction(byte | 128)


def move_screen():
    send_instruction(0b00011000)


# endregion
init_LCD()

# region hardware functies


def tone(frequentie, boolean):
    if boolean == True:
        for i in range(1000):
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(frequentie/1000000)
            GPIO.output(buzzer, GPIO.LOW)
            time.sleep(frequentie/1000000)
            i += 1

    for i in range(100):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(frequentie/1000000)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(frequentie/1000000)
        i += 1


def MOTION(PIR):
    if GPIO.event_detected(PIR):
        value_pir = 1
        id_pir = 3
        socketio.emit('B2F_update_bureauactiviteit')
        DataRepository.add_sensorwaarde(
            id_pir, datetime.now(), value_pir)
        print("PIR sensor naar database")


GPIO.add_event_detect(PIR, GPIO.RISING, callback=MOTION)


def showIP(re_btn):
    if GPIO.event_detected(re_btn):
        ips = str(check_output(['hostname', '--all-ip-addresses']))
        print(ips)
        deel1_kabel_wifi = ips[18:]
        deel1_wifi = ips[2:]
        ip_kable_wifi = deel1_kabel_wifi[:-3]
        ip_wifi = deel1_wifi[:-3]
        pwm.ChangeDutyCycle(30)
        send_instruction(0b00000001)
        if len(ips) > 21:
            write_message(ip_kable_wifi)
        else:
            write_message(ip_wifi)
        time.sleep(10)
        send_instruction(0b00000001)
        pwm.start(100)


GPIO.add_event_detect(re_btn, GPIO.RISING, callback=showIP)


def ifpushbtn(pin):
    if GPIO.event_detected(button):
        print("click")
        nieuwste_melding = DataRepository.get_melding()
        if nieuwste_melding["tijd_afdrukken_melding"] == None:
            volgnummer = nieuwste_melding["volgnummer_melding"]
            DataRepository.update_afdrukken_melding(datetime.now(), volgnummer)
            print("De melding is correct afgedrukt")
            pwm.ChangeDutyCycle(30)
            send_instruction(0b00000001)
            write_message("Wachten op")
            set_cursor(1, 0)
            write_message("volgende melding")
            socketio.emit('B2F_update_historiekmelding')
            socketio.emit('B2F_ongelezen_melding')
            vibration_motor(False)
            tone(600, False)
            pixels.fill((0, 0, 0))
            time.sleep(3)
            send_instruction(0b00000001)
            pwm.ChangeDutyCycle(100)

        else:
            print("De melding is al afgedrukt")


def clk_dt_read(pin):
    global counter

    if GPIO.event_detected(clk):
        if GPIO.input(clk) and GPIO.input(dt):
            counter += 1
            if counter > 3:
                counter = 1
            elif counter < 1:
                counter = 3
            print(counter)
            DataRepository.add_sensorwaarde(
                id_rotary, datetime.now(), counter)
            socketio.emit('B2F_update_status_melding')
            print("rotary naar database")
            verschillende_modus_display()
        elif GPIO.input(clk) and GPIO.input(dt) == 0:
            counter -= 1
            if counter > 3:
                counter = 1
            elif counter < 1:
                counter = 3
            print(counter)
            DataRepository.add_sensorwaarde(
                id_rotary, datetime.now(), counter)
            socketio.emit('B2F_update_status_melding')
            print("rotary naar database")
            verschillende_modus_display()


def verschillende_modus_display():
    if counter == 1:
        pwm.ChangeDutyCycle(30)
        DataRepository.update_status_device(1, id_neopixel)
        DataRepository.update_status_device(0, id_trilmotor)
        DataRepository.update_status_device(0, id_buzzer)
        pixels.fill((255, 0, 0))
        write_message("Modus : stil")
        time.sleep(1)
        send_instruction(0b00000001)
        pixels.fill((0, 0, 0))
        pwm.ChangeDutyCycle(100)

    elif counter == 2:
        pwm.ChangeDutyCycle(30)
        DataRepository.update_status_device(1, id_neopixel)
        DataRepository.update_status_device(1, id_trilmotor)
        DataRepository.update_status_device(0, id_buzzer)
        pixels.fill((125, 0, 125))
        vibration_motor(True)
        time.sleep(0.2)
        vibration_motor(False)
        write_message("Modus : trillen")
        time.sleep(1)
        send_instruction(0b00000001)
        pixels.fill((0, 0, 0))
        pwm.ChangeDutyCycle(100)

    elif counter == 3:
        pwm.ChangeDutyCycle(30)
        DataRepository.update_status_device(1, id_neopixel)
        DataRepository.update_status_device(1, id_trilmotor)
        DataRepository.update_status_device(1, id_buzzer)
        pixels.fill((0, 0, 255))
        vibration_motor(True)
        tone(600, False)
        time.sleep(0.2)
        vibration_motor(False)
        write_message("Modus : luid")
        time.sleep(1)
        send_instruction(0b00000001)
        pixels.fill((0, 0, 0))
        pwm.ChangeDutyCycle(100)


def vibration_motor(bool):
    if bool == True:
        GPIO.output(vib_motor, GPIO.HIGH)
    elif bool == False:
        GPIO.output(vib_motor, GPIO.LOW)


def getPPM():
    waarde_i2c = i2c.read_i2c_block_data(0x5B, 0x02, 8)
    print(waarde_i2c)
    register1 = waarde_i2c[0]
    register2 = waarde_i2c[1]

    register1 = register1 << 8
    result = register1 | register2
    return result


def statusActuators(status):
    print(status)
    if status == 1:
        pixels.fill((0, 200, 100))
    elif status == 2:
        pixels.fill((0, 200, 100))
        vibration_motor(True)
    elif status == 3:
        pixels.fill((0, 200, 100))
        vibration_motor(True)
        GPIO.output(buzzer, GPIO.HIGH)
        # buzzer(true)

# endregion
# endregion


# Code voor Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*",
                    logger=False, engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

# region THREADING

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.


def co2_inlezen():
    while True:
        try:
            luchtkwaliteit = ccs811.eco2
            if(luchtkwaliteit < 8000):
                DataRepository.add_sensorwaarde(
                    id_luchtkwaliteitssensor, datetime.now(), luchtkwaliteit)
                socketio.emit('B2F_update_luchtkwaliteit')
            print(luchtkwaliteit)
            time.sleep(10)
        except:
            print("error")
        time.sleep(0.5)
        # DataRepository.add_sensorwaarde(
        #    id_luchtkwaliteitssensor, datetime.now(), getPPM())
        socketio.emit('B2F_update_historieksensor')
        # time.sleep(60)


thread_co2 = threading.Timer(10, co2_inlezen)
thread_co2.start()


def rotary_inlezen():
    GPIO.add_event_detect(clk, GPIO.BOTH, callback=clk_dt_read, bouncetime=1)
    while True:
        time.sleep(1)
        # pot value schrijven naar database


thread_rotary = threading.Thread(target=rotary_inlezen)
thread_rotary.start()


def button_push():
    GPIO.add_event_detect(button, GPIO.BOTH,
                          callback=ifpushbtn, bouncetime=300)
    while True:
        time.sleep(1)
        # alarm afleggen
        # updaten tijd_afdrukken in historiek_melding
        # misschien met socket iets versturen naar frontend dat het alarm is afgedrukt


thread_btn = threading.Thread(target=button_push)
thread_btn.start()

# endregion

print("**** Program started ****")

# API ENDPOINTS
endpoint = '/api/v1'


@app.route(endpoint + '/melding', methods=['POST'])
def add_meldingen():
    gegevens = DataRepository.json_or_formdata(request)
    nieuw_id = DataRepository.add_melding(
        datetime.now(), None, gegevens['bericht'], gegevens['status_bericht'])
    return jsonify(bericht=nieuw_id), 201


@app.route(endpoint + '/devices', methods=['GET'])
def get_historiek_devices():
    s = DataRepository.get_sensorhistoriek()
    # print(s)
    return jsonify(s), 200


@app.route(endpoint + '/bureau_activiteit', methods=['GET'])
def get_bureau_activiteit():
    s = DataRepository.get_bureau_activiteit()
    # print(s)
    return jsonify(s), 200


@app.route(endpoint + '/meldingen', methods=['GET'])
def get_meldingen_historiek():
    s = DataRepository.get_meldingen()
    # print(s)
    return jsonify(s), 200


@app.route(endpoint + '/luchtkwaliteit', methods=['GET'])
def get_luchtkwaliteit_historiek():
    s = DataRepository.get_luchtkwaliteit()
    # print(s)
    return jsonify(s), 200


@app.route(endpoint + '/melding', methods=['GET'])
def get_ongelezen_melding():
    s = DataRepository.get_melding()
    # print(s)
    return jsonify(s), 200


@app.route(endpoint + '/kamer', methods=['GET'])
def get_kamer():
    s = DataRepository.get_kamer()
    # print(s)
    return jsonify(s), 200


@app.route(endpoint + '/status_melding', methods=['GET'])
def get_status_melding():
    s = DataRepository.get_status_melding()
    # print(s)
    return jsonify(s), 200


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # historiek = DataRepository.get_sensorhistoriek()
    # print(historiek)
    # emit('B2F_historiek_devices', {
    #      'historiek_devices': historiek}, breakcast=True)


@socketio.on('F2B_change_name')
def sendName(naam):
    print(naam)
    DataRepository.update_kamer_naam(naam['voornaam'])
    socketio.emit('B2F_change_name')


@socketio.on('F2B_afsluiten')
def afsluiten():
    print("afsluiten")
    pwm.ChangeDutyCycle(30)
    send_instruction(0b00000001)
    write_message('afsluiten...')
    time.sleep(5)
    send_instruction(0b00000001)
    call("sudo poweroff", shell=True)


@socketio.on('F2B_getBericht')
def getBericht():
    pwm.ChangeDutyCycle(30)
    send_instruction(0b00000001)
    bericht = DataRepository.get_melding()
    tekst_bericht = bericht["bericht"]
    print(tekst_bericht)
    deel1 = tekst_bericht[0:16]
    deel2 = tekst_bericht[16:32]
    write_message(deel1)
    set_cursor(1, 0)
    write_message(deel2)
    statusActuators(bericht["status_melding"])

    # code schrijven voor op display te tonen en alarm laten afgaan
# ANDERE FUNCTIES


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
