# Fire Guard – Fire Air-Quality Monitoring & Alert System

## Project Brief
FireGuard is a wildfire detection unit engineered for extreme resilience and sustainability. It is designed to withstand remote, harsh conditions and even direct wildfire exposure. The device minimizes pollution if damaged by fire, using materials that burn cleanly or not at all, and is built for potential reuse or recycling after a fire. The diagram below outlines FireGuard’s key components, each chosen for fire-resistance and low environmental impact, along with a life-cycle pathway for recovery and reuse.

## Project Research
![Research.png](https://github.com/Jerrycai4321/Fire-Guard/blob/main/Research.png?raw=true)

## Product Design
![Material.png](https://github.com/Jerrycai4321/Fire-Guard/blob/main/Research.png?raw=true)



## Interfaces

### Device Interface
- **NeoPixel Alert Strip**: 30 LEDs on GPIO 5 flash red when Fire AQI > 300  
- **Serial Console**: Prints `"1"` on alert to simplify downstream logging  

### Cloud Dashboard
- **Adafruit IO** streams:
  - `Temp_Feed` – raw temperature readings  
  - `fire-alert-feed` – binary alert flag (0/1)  

> _Create these feeds under your Adafruit IO account before running firmware._

## Project Outcome
- ✅ **Real-time Fire AQI calculation & local flashing**  
- ✅ **MQTT alert published to “fire-alert-feed”**  
- ✅ **Minimal hardware footprint**  
- 🔗 [Demo Video (YouTube)](https://youtu.be/HaKyc20MGzE)  

## Flow State and Sketches
![Flow Diagram](./flowstate.png)  
1. **Data Acquisition**: EnvPRO + IR + Light → raw readings  
2. **AQI Computation**: normalize & weight → 0–500 scale  
3. **Threshold Check**:  
   - If AQI > 300 → enter ALERT mode  
   - Else → idle  
4. **Alert Mode**:  
   - Flash NeoPixels red  
   - Publish `"1"` to MQTT  

## Material Used
- **Prototyping Platform**: ESP32 M5 Stack  
- **Environmental Sensor**: EnvPRO Unit (gas, temp, humidity)  
- **Optical Sensors**: Reflective IR (GPIO 7), Light sensor (GPIO 1)  
- **LEDs**: 30× NeoPixel strip (GPIO 5)  
- **Connectivity**: Wi-Fi + Adafruit IO (MQTT)  

## Firmware
