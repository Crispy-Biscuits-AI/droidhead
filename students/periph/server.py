from fastapi import FastAPI
import os, time, json
from smbus2 import SMBus
import paho.mqtt.client as mqtt
app = FastAPI(title="Peripherals Student")
I2C_BUS = os.getenv("I2C_BUS", "/dev/i2c-1")
BATTERY_ADDR = int(os.getenv("BATTERY_ADDR", "0x36"), 16)
BATTERY_MONITOR = os.getenv("BATTERY_MONITOR","max17048")
MQTT_HOST = os.getenv("MQTT_HOST","mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT","1883"))
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"droidhead-periph-{int(time.time())}")
try:
    mqttc.connect(MQTT_HOST, MQTT_PORT, 60); mqttc.loop_start()
except Exception: pass
def read_max17048_voltage(bus: SMBus, addr: int) -> float:
    data = bus.read_word_data(addr, 0x02); msb = data & 0xFF; lsb = (data >> 8) & 0xFF
    raw = (msb << 4) | (lsb >> 4); return raw * 1.25e-3
def read_ina219_voltage(bus: SMBus, addr: int) -> float:
    data = bus.read_word_data(addr, 0x02); msb = (data >> 8) & 0xFF; lsb = data & 0xFF
    raw = ((msb << 8) | lsb) >> 3; return raw * 0.004
@app.get("/battery")
def battery():
    try:
        with SMBus(int(I2C_BUS.split("-")[-1])) as bus:
            if BATTERY_MONITOR == "max17048": v = read_max17048_voltage(bus, BATTERY_ADDR)
            elif BATTERY_MONITOR == "ina219": v = read_ina219_voltage(bus, BATTERY_ADDR)
            else: v = 3.85
        payload = {"voltage": round(v, 3), "ts": time.time()}
    except Exception as e:
        payload = {"error": str(e), "ts": time.time()}
    try: mqttc.publish("droidhead/periph/battery", json.dumps(payload), qos=0)
    except Exception: pass
    return payload
