# Fire Guard – Fire Air-Quality Monitoring & Alert System

![Image27](https://github.com/Jerrycai4321/Fire-Guard/blob/main/Image27.png?raw=true)

[Prototype Demo Video (YouTube)](https://youtu.be/bipr-JXk_RM)  

## Project Brief
FireGuard is a wildfire detection unit engineered for extreme resilience and sustainability. It is designed to withstand remote, harsh conditions and even direct wildfire exposure. The device minimizes pollution if damaged by fire, using materials that burn cleanly or not at all, and is built for potential reuse or recycling after a fire. The diagram below outlines FireGuard’s key components, each chosen for fire-resistance and low environmental impact, along with a life-cycle pathway for recovery and reuse.

## Project Research
![Research.png](https://github.com/Jerrycai4321/Fire-Guard/blob/main/Research.png?raw=true)

## Product Design
![Material.png](https://github.com/Jerrycai4321/Fire-Guard/raw/main/Material.png?raw=true)

## Interfaces
![ui1.png](https://github.com/Jerrycai4321/Fire-Guard/raw/main/ui1.png?raw=true)

## Project Outcome
- ✅ **Real-time Fire AQI calculation & local flashing**  
- ✅ **MQTT alert published to “fire-alert-feed”**  
- ✅ **Minimal hardware footprint**  

## Flow State
![flowstate1](https://github.com/Jerrycai4321/Fire-Guard/raw/main/flowstate1.png?raw=true)  
1. **Data Acquisition**: EnvPRO + IR + Light → raw readings  
2. **AQI Computation**: normalize & weight → 0–500 scale  
3. **Threshold Check**:  
   - If AQI > 300 → enter ALERT mode  
   - Else → idle  
4. **Alert Mode**:  
   - Flash NeoPixels red  
   - Publish Alert using  MQTT to Adafruit IO

## Material Used
- **Prototyping Platform**: ESP32 M5 Stack  
- **Environmental Sensor**: EnvPRO Unit (gas, temp, humidity)  
- **Optical Sensors**: Reflective IR (GPIO 7), Light sensor (GPIO 1)  
- **LEDs**: 30× NeoPixel strip (GPIO 5)  
- **Connectivity**: Wi-Fi + Adafruit IO (MQTT)  

## Firmware
This firmware connects environmental sensing, LED signaling, and MQTT messaging into one system. It uses sensor data to compute a synthetic Fire AQI—a custom metric to detect hazardous conditions—and triggers visual alerts accordingly.

1. Wi-Fi and MQTT Setup
The system connects to a Wi-Fi network and initializes an MQTT client for cloud messaging.
This enables remote monitoring and subscription to sensor topics.

```
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
...
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
```

2. Hardware Initialization
Initializes NeoPixel LEDs, I²C communication, and ADC channels for analog sensors.

```
LED_PIN = Pin(5, Pin.OUT)
np_strip = neopixel.NeoPixel(LED_PIN, NUM_PIXELS)
...
i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
envpro = ENVPROUnit(i2c0)
...
adc_ir    = ADC(Pin(7));   adc_ir.atten(ADC.ATTN_11DB)
adc_light = ADC(Pin(1));   adc_light.atten(ADC.ATTN_11DB)
```

3. Fire AQI Algorithm
This function fuses five sensor readings into a normalized Fire AQI score (range: 0–500).
It applies min-max normalization, signal inversion, and weighted aggregation.

```
def compute_fire_aqi(gas, temp, hum, ir, light):
    # Normalize inputs
    ...
    # Invert gas, humidity, light (low values are worse)
    ...
    # Weighted sum of factors (fire risk model)
    ...
    return int(aqi_norm * 500)
```

Gas (30%), Temperature (25%), and Humidity (20%) dominate the score

Infrared (15%) and Light (10%) act as secondary indicators

The result reflects potential fire risk severity

4. LED Alert System
Uses the computed Fire AQI to light up a NeoPixel strip red if the value exceeds 300 (hazard threshold).

```
def update_led(fire_aqi):
    if fire_aqi > 300:
        for i in range(NUM_PIXELS):
            np_strip[i] = (255, 0, 0)  # Red = danger
        np_strip.write()
        print("1")  # Signal triggered
    else:
        for i in range(NUM_PIXELS):
            np_strip[i] = (0, 0, 0)    # Off = safe
        np_strip.write()

```
