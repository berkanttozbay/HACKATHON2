import numpy as np
from laser import Laser
from detector import Detector
from channel_model import ChannelModel
from weather import Weather

def simulate(bit_rate, distance, visibility, initial_laser_power, detector_type, bandwidth):
    print(f"Simulate: bit_rate={bit_rate}, distance={distance}, visibility={visibility}, initial_laser_power={initial_laser_power}, detector_type={detector_type}, bandwidth={bandwidth}")  # Debugging
    laser = Laser()
    laser.adjust_power(visibility)
    detector = Detector(detector_type)
    channel_model = ChannelModel()

    data = np.random.randint(0, 2, 100)
    laser_output = laser.modulate(data, initial_laser_power)
    transmitted_signal = channel_model.calculate_total_attenuation(distance, visibility, laser.wavelength * 1e9) * laser_output
    received_signal = detector.detect(transmitted_signal, bandwidth, noise_power=0.1)
    signal_loss = laser_output - transmitted_signal  # Signal loss calculation

    return laser_output, transmitted_signal, received_signal, signal_loss
