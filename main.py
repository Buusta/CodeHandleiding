import machine
import time
import ReadSensor  # Zorg ervoor dat ReadSensor correct werkt
import uio  # Gebruik uio voor bestandsbeheer op de Pico

# PID-parameters
Kp = 100  # Lagere proportionele gain voor minder agressieve correctie
Ki = 0.39  # Lagere integrale gain voor minder oscillaties
Kd = 0.1  # Lagere differentiële gain met filter

# Servo-instellingen
servo = machine.PWM(machine.Pin(0))  # Servo aangesloten op GP0
servo.freq(50)  # 50Hz is standaard voor servo's

# PID-variabelen
prev_error = 0.0
integral = 0.0
prev_derivative = 0.0  # Voor het filteren van de afgeleide term
dt = 0.01  # Tijdstap in seconden (10 ms)

# Doelwaarde van de hoek (0 graden = verticale positie)
setpoint = 0.0

# Maak een CSV-bestand aan en schrijf de header
with open("pid_log.csv", "w") as f:
    f.write("time,error,integral,derivative,output,setpoint,measured_value,angle_x,angle_y,control_signal,speed\n")

def set_speed(speed):
    """Schaalt -80 tot 80 naar 1ms tot 2ms PWM-signaal."""
    pulse_width_ms = 1.5 + (speed / 100) * 0.5  # 1.0ms (-100) tot 2.0ms (100)
    duty = int((pulse_width_ms / 20) * 65535)  # Omrekenen naar duty cycle
    servo.duty_u16(duty)
    return duty

def pid_controller(setpoint, measured_value):
    """Berekent de PID-regeling voor de servo."""
    global prev_error, integral, prev_derivative

    error = setpoint - measured_value
    integral += error * dt
    integral = max(-50, min(50, integral))  # Anti-windup beperking

    derivative = (error - prev_error) / dt

    # Low-pass filter voor de afgeleide term om ruis te verminderen
    alpha = 0.2
    derivative = alpha * derivative + (1 - alpha) * prev_derivative
    prev_derivative = derivative

    prev_error = error

    output = (Kp * error) + (Ki * integral) + (Kd * derivative)
    output = max(-80, min(80, output))  # Begrens de output
    
    return output, error, integral, derivative

# Wacht even voor stabiliteit
time.sleep(2)

start_time = time.ticks_ms()  # Starttijd loggen

while True:
    try:
        # Lees sensorwaarden
        angle_x, angle_y = ReadSensor.read_angles()
        control_signal, error, integral, derivative = pid_controller(setpoint, angle_y)
        speed = set_speed(control_signal)
        
        # Tijdstempel
        current_time = time.ticks_diff(time.ticks_ms(), start_time) / 1000  # in seconden
        
        # Log data naar CSV
        with open("pid_log.csv", "a") as f:
            f.write(f"{current_time},{error},{integral},{derivative},{control_signal},{setpoint},{angle_y},{angle_x},{angle_y},{control_signal},{speed}\n")
        
        time.sleep(dt)  # Kleine vertraging voor stabiliteit
    except Exception as e:
        print("Fout:", e)
        time.sleep(1)