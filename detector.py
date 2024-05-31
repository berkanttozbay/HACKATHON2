import numpy as np

class Detector:
    def __init__(self, detector_type, sensitivity=0.8, load_resistance=100):
        self.detector_type = detector_type
        self.sensitivity = sensitivity
        self.load_resistance = load_resistance

    def output_current(self, received_power):
        return self.sensitivity * received_power

    def noise(self, bandwidth, temperature=300):
        k = 1.38e-23  # Boltzmann constant
        thermal_noise = np.sqrt(4 * k * temperature * self.load_resistance * bandwidth)
        return thermal_noise

    def detect(self, signal, bandwidth, noise_power):
        noisy_signal = signal + self.noise(bandwidth) * noise_power
        return noisy_signal
