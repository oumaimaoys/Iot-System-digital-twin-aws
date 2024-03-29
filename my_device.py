import json
import time
import random
import paho.mqtt.client as mqtt

class IoTGardeningSystem:
    def __init__(self, client_id, endpoint, topic):
        #time reference
        self.time = 0

        # Initialize the AWS IoT Core settings
        self.client_id = client_id
        self.endpoint = endpoint
        self.topic = topic
        
        # Create MQTT client and connect
        self.client = mqtt.Client(client_id)
        self.client.connect(endpoint, 8883)

        # Initialize sensor objects
        self.temperature_sensor = TemperatureSensor()
        self.humidity_sensor = HumiditySensor()
        self.light_sensor = LightSensor()
        self.moisture_sensor = MoistureSensor()

        # initialize actuators
        self.humidifier = Humidifier()
        self.sprinkler = Sprinkler()
        self.led_light = LEDlight()
        self.fan = Fan()

    def track_parameters(self):
        # Simulate sensor data
        temperature = self.temperature_sensor.get_temperature(self.time)
        humidity = self.humidity_sensor.get_humidity(self.time)
        light_condition = self.light_sensor.get_light_condition(self.time)
        moisture = self.moisture_sensor.get_moisture(self.time)

        # actuators states
        humidifier_state = self.humidifier.get_state()
        sprinkler_state = self.sprinkler.get_state()
        led_light_state = self.led_light.get_state()
        fan_state = self.fan.get_state()


        # Format data as JSON
        payload = {
            "device_id": self.client_id,
            "sensors": {
                "temperature_sensor": {"temperature": temperature},
                "humidity_sensor": {"humidity": humidity},
                "light_sensor": {"light_condition": light_condition},
                "moisture_sensor": {"moisture": moisture}
            },
            "actuators": {
                "humidifier": {"humidifier_state": humidifier_state},
                "sprinkler": {"sprinkler_state": sprinkler_state},
                "LED_light": {"led_light_state": led_light_state},
                "fan": {"fan_state": fan_state}
            }
        }

        # Publish data to AWS IoT Core
        self.client.publish(self.topic, json.dumps(payload), qos=1)

        # Process the sensor data and take actions
        if temperature > 30:
            self.fan.turn_on()
        else :
            self.fan.turn_off()

        if humidity < 40:
            self.fan.turn_on()
            self.humidifier.turn_on()
        else : 
            self.fan.turn_off()
            self.humidifier.turn_off()

        if light_condition < 50 and self.light_sensor.is_daytime(self.time) == True:
            self.led_light.turn_on()
        else :
            self.led_light.turn_off()
            
        if moisture < 20:
            # Take action based on low moisture
            self.sprinkler.turn_on()
        else:
            self.sprinkler.turn_off()

    def run(self):
        while True:
            self.track_parameters()
            self.time += 1
            time.sleep(5)


class Sensor():
    def is_daytime(self, time_reference):
        # Assuming day starts at 6:00 and ends at 18:00
        hour = time_reference
        return 6 <= hour < 18
    
class TemperatureSensor(Sensor):
    def get_temperature(self, time_reference):
        # Simulate temperature data between 20 and 40 degrees Celsius
        if self.is_daytime(time_reference):
            # Daytime temperature may vary between 25 and 35 degrees Celsius
            return random.uniform(25, 35)
        else:
            # Nighttime temperature may vary between 20 and 25 degrees Celsius
            return random.uniform(20, 25)


class HumiditySensor(Sensor):
    def get_humidity(self, time_reference):
        # Simulate humidity data between 30 and 70 percent (vapour per volume)
        if self.is_daytime(time_reference):
            # Daytime humidity may vary between 40 and 60 percent
            return random.uniform(40, 60)
        else:
            # Nighttime humidity may vary between 30 and 40 percent
            return random.uniform(30, 40)

class LightSensor(Sensor):
    def get_light_condition(self, time_reference):
        # Simulate light condition data between 0 and 100 intensity
        if self.is_daytime(time_reference):
            # Daytime light intensity may vary between 50 and 100
            return random.randint(50, 100)
        else:
            # Nighttime light intensity may vary between 0 and 50
            return random.randint(0, 50)

    
class MoistureSensor(Sensor):
    def get_moisture(self, time_reference):
        # Simulate moisture data between 0 and 100 (usually from 0 -1023 but mapped to %)
        if self.is_daytime(time_reference):
            # Daytime moisture may vary between 60 and 80 percent
            return random.randint(60, 80)
        else:
            # Nighttime moisture may vary between 40 and 60 percent
            return random.randint(40, 60)

class Actuator:
    def __init__(self):
        self.state = False

    def turn_on(self) -> bool:
        # Code to turn on the actuator
        self.state = True
        return self.state

    def turn_off(self) -> bool:
        # Code to turn off the actuator
        self.state = False
        return self.state
    
    def get_state(self) -> bool:
        return self.state

class Humidifier(Actuator):
    pass

class Sprinkler(Actuator):
    pass

class LEDlight(Actuator):
    pass

class Fan(Actuator):
    pass


# Create an instance of the IoTGardeningSystem class
my_device = IoTGardeningSystem(
    client_id="my_gardening_system",
    endpoint="a1jxj0z3x3q3y-ats.iot.us-west-2.amazonaws.com",
    topic="garden/parameters"
)
my_device