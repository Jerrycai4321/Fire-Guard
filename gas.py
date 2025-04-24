import time
import M5 
from hardware import I2C, Pin, ADC
from unit import ENVPROUnit
import neopixel
import network
from umqtt import MQTTClient

# ————— Wi-Fi & MQTT Setup —————
ssid = 'ACCD'
password = 'tink1930'
aio_user_name = 'jerrycai15'
aio_password = 'aio_quNI14btONorG9L3V8ZrfdnXvjk2'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
while not wifi.isconnected():
    time.sleep_ms(100)

mqtt_client = MQTTClient(
    'testclient-' + aio_user_name,
    'io.adafruit.com',
    port=1883,
    user=aio_user_name,
    password=aio_password,
    keepalive=3000
)
mqtt_client.connect(clean_session=True)
mqtt_client.subscribe(aio_user_name + '/feeds/Temp_Feed', lambda data: None)

# ————— Hardware Init —————
M5.begin()

# NeoPixel strip on pin 5
LED_PIN = Pin(5, Pin.OUT)
NUM_PIXELS = 30
np_strip = neopixel.NeoPixel(LED_PIN, NUM_PIXELS)

# EnvPRO sensor over I²C
i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
envpro = ENVPROUnit(i2c0)

# Reflective IR on pin 7, Light sensor on pin 1
adc_ir    = ADC(Pin(7));   adc_ir.atten(ADC.ATTN_11DB)
adc_light = ADC(Pin(1));   adc_light.atten(ADC.ATTN_11DB)

def compute_fire_aqi(gas, temp, hum, ir, light):
    # 1. Normalize to 0–1
    g = max(0, min(gas, 50000)) / 50000
    t = max(0, min(temp, 50))   / 50
    h = max(0, min(hum, 100))   / 100
    i = max(0, min(ir, 255))    / 255
    l = max(0, min(light, 255)) / 255

    # 2. Invert where lower values imply worse air
    gas_score   = 1 - g
    hum_score   = 1 - h
    light_score = 1 - l

    # 3. Weighted sum (weights sum to 1)
    w_gas   = 0.30
    w_temp  = 0.25
    w_hum   = 0.20
    w_ir    = 0.15
    w_light = 0.10

    aqi_norm = (
        gas_score   * w_gas
      + t           * w_temp
      + hum_score   * w_hum
      + i           * w_ir
      + light_score * w_light
    )

    # 4. Scale to 0–500
    return int(aqi_norm * 500)

def update_led(fire_aqi):
    """Light up the NeoPixel strip red if fire_aqi > 300 and print '1' once."""
    if fire_aqi > 300:
        # turn all LEDs red
        for i in range(NUM_PIXELS):
            np_strip[i] = (255, 0, 0)
        np_strip.write()
        print("1")
    else:
        # turn all LEDs off
        for i in range(NUM_PIXELS):
            np_strip[i] = (0, 0, 0)
        np_strip.write()

def loop():
    M5.update()
    
    # Read EnvPRO
    gas  = envpro.get_gas_resistance()
    hum  = envpro.get_humidity()
    temp = envpro.get_temperature()
    
    # Read ADC sensors (0–1023 → approx. 0–511)
    ir_val    = adc_ir.read()    // 2
    light_val = adc_light.read() // 2
    
    # Compute synthetic Fire AQI
    fire_aqi = compute_fire_aqi(gas, temp, hum, ir_val, light_val)
    
    # Update LEDs (and print "1" if above threshold)
    update_led(fire_aqi)
    
    mqtt_client.check_msg()
    time.sleep(1)

if __name__ == '__main__':
    # Ensure LEDs start off
    for i in range(NUM_PIXELS):
        np_strip[i] = (0, 0, 0)
    np_strip.write()
    
    try:
        while True:
            loop()
    except (Exception, KeyboardInterrupt):
        pass
