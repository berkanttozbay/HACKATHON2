import numpy as np

class ChannelModel:
    def __init__(self, wavelength=1550e-9):
        self.wavelength = wavelength  # Lazer dalga boyu (metre)

    def calculate_attenuation_coefficient(self, visibility, wavelength_nm):
        if visibility > 15:
            p = 1.6
        elif 8 < visibility <= 15:
            p = 1.3
        elif 5 < visibility <= 8:
            p = 0.6 * visibility + 0.34
        elif 2 < visibility <= 5:
            p = visibility - 0.5
        else:
            p = 0
        
        sigma_a = 3.91 / visibility * (wavelength_nm / 550)**-p
        return sigma_a

    def calculate_total_attenuation(self, distance, visibility, wavelength_nm):
        sigma_a = self.calculate_attenuation_coefficient(visibility, wavelength_nm)
        tau_R = np.exp(-sigma_a * distance)
        return tau_R

    def calculate_geometric_loss(self, transmitter_diameter, receiver_diameter, distance):
        G_T = (np.pi * transmitter_diameter / self.wavelength)**2
        G_R = (np.pi * receiver_diameter / self.wavelength)**2
        L_fs = (self.wavelength / (4 * np.pi * distance))**2
        return G_T, G_R, L_fs

    def calculate_received_power(self, P_T, distance, visibility, transmitter_diameter, receiver_diameter):
        wavelength_nm = self.wavelength * 1e9  # Dalga boyunu nanometreye çevir
        tau_R = self.calculate_total_attenuation(distance, visibility, wavelength_nm)
        G_T, G_R, L_fs = self.calculate_geometric_loss(transmitter_diameter, receiver_diameter, distance)
        P_R = P_T * tau_R * G_T * G_R * L_fs
        return P_R
