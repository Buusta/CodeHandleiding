import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
import math

# I2C-initialisatie
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=1000000)
sensor = MPU9250(i2c)

alpha = 0.98  # Complementary filter constant
dt = 0.01  # Tijdstap (10 ms)

angle_x = 0
angle_y = 0

def read_angles():
    global angle_x, angle_y

    # Lees sensordata
    gx, gy, gz = sensor.gyro  # Rotatiesnelheid (°/s of rad/s)
    ax, ay, az = sensor.acceleration  # Versnelling (m/s²)
    #print(f"gx: {gx}")
    
    #gx_offset = sum([sensor.gyro[0] for _ in range(100)]) / 100  # Gemiddelde bias
    #gx -= gx_offset
    
    # Bereken de hoek met de accelerometer
    accel_angle_x = math.atan2(ay, az) * (180 / math.pi)
    
    accel_angle_y = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
    #print(f"accelx = {accel_angle_x}")
    # Bereken de hoek met de gyroscoop (integreren over tijd)
    angle_x = alpha * (angle_x + gx * dt) + (1 - alpha) * accel_angle_x
    angle_y = alpha * (angle_y + gy * dt) + (1 - alpha) * accel_angle_y

    return angle_x, angle_y

if __name__ == "__main__":
    while True:
        angle_x, angle_y = read_angles()
        print(f"Angle X: {angle_x:.2f}, Angle Y: {angle_y:.2f}")
        utime.sleep_ms(10)
