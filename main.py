import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from weather import Weather
from simulate import simulate
from sinuslu import *
import numpy as np
import matplotlib.pyplot as plt
import math

# Planck constant and speed of light
h = 6.62607015e-34  # Planck constant (Joule*second)
c = 3.0e8  # Speed of light (meters/second)

# Constants for FEL calculations
euler_sayisi = math.e
speed_of_light_m_s2 = 3 * 10 ** 8

# Functions for channel capacity and energy calculations
def calculate_channel_capacity(bandwidth, signal_power, noise_power):
    capacity = bandwidth * np.log2(1 + (signal_power / noise_power))
    return capacity / 1e6  # Return in Mbps

def hesapla_enerji(frekans):
    return h * frekans

def hesapla_dalgaboyu(frekans):
    return (c / frekans) * 1e9  # Return in nanometers

def belirle_isik_turu(frekans):
    if frekans >= 3e19:
        return "Gamma Ray"
    elif 3e16 <= frekans < 3e19:
        return "X Ray"
    elif 8e14 <= frekans < 3e16:
        return "Ultraviolet Light"
    elif 4e14 <= frekans < 8e14:
        return "Visible Light"
    elif 3e11 <= frekans < 4e14:
        return "Infrared Light"
    elif 1e9 <= frekans < 3e11:
        return "Microwave"
    else:
        return "Radio Waves"

def calculate_fel_wavelength(lambda_u, electron_energy_gev = 1.0 , magnetic_field_t = 1.0):
    electron_mass_kg = 9.1 * euler_sayisi ** (-31)  # Elektron kütlesi (kg)
    electron_charge_c = 1.6 * euler_sayisi ** (-19)  # Elektron yükü (C)
    speed_of_light_m_s = 300  # Işık hızı (m/s)
    gev_to_joule = 1.6 * euler_sayisi ** (-10)  # GeV to Joule dönüşüm faktörü

    electron_energy_j = electron_energy_gev * gev_to_joule

    gamma = electron_energy_j / (electron_mass_kg * speed_of_light_m_s2)

    K = (electron_charge_c * magnetic_field_t * lambda_u) / (
            2 * math.pi * electron_mass_kg * speed_of_light_m_s)

    wavelength = (lambda_u / (2 * gamma ** 2)) * (1 + (K * 2 / 2))

    return wavelength

def guncelle_degerler(event):
    frekans = scale.get() * 1e12  # Frequency in terahertz
    enerji = hesapla_enerji(frekans)
    dalgaboyu = hesapla_dalgaboyu(frekans)
    
    signal_power = 1e-3  # 1 mW
    noise_power = 1e-6  # 1 µW
    bandwidth = frekans
    kapasite = calculate_channel_capacity(bandwidth, signal_power, noise_power)
    
    isik_turu = belirle_isik_turu(frekans)
    
    label_enerji_deger.config(text=f"{enerji:.2e} J")
    label_dalgaboyu_deger.config(text=f"{dalgaboyu:.2f} nm")
    label_kapasite_deger.config(text=f"{kapasite:.2f} Mbps")
    label_isik_turu_deger.config(text=isik_turu)
    
    update_graph(frekans)

def update_graph(frekans):
    t = np.linspace(0, 1, 1000)
    y = np.sin(2 * np.pi * (frekans / 1e12) * t)
    ax.clear()
    ax.plot(t, y)
    ax.set_title("Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    canvas.draw()

def undulator_degisimi(deger):
    lambda_u = float(deger)  
    wavelength = calculate_fel_wavelength(lambda_u, electron_energy_gev=1.0, magnetic_field_t=1.0)
    label_wavelength.config(text=f"FEL wavelength: {wavelength:.2f} nm")

def display_weather(api_key, city):
    weather = Weather(api_key, city)
    visibility = weather.get_visibility()
    conditions = weather.get_weather_conditions()
    estimated_visibility = weather.estimate_visibility(conditions)

    print(f"Retrieved visibility: {visibility} km") 
    print(f"Weather conditions: {conditions}") 
    print(f"Estimated visibility: {estimated_visibility} km") 

    ttk.Label(mainframe, text=f"City: {city}").grid(column=1, row=1, sticky=tk.W)
    ttk.Label(mainframe, text=f"Visibility: {estimated_visibility} km (Estimated)").grid(column=1, row=2, sticky=tk.W)
    ttk.Label(mainframe, text=f"Weather Conditions: {conditions}").grid(column=1, row=3, sticky=tk.W)

    distances = [0.5, 1.0, 2.0, 5.0]
    initial_power = 10e-3
    initial_lambda_u = 1.0
    transmitter_diameter = 0.1
    receiver_diameter = 0.1

    modulated_outputs = []
    transmitted_signals = []
    detected_signals = []
    signal_losses = []

    for distance in distances:
        modulated_output, transmitted_signal, detected_signal, signal_loss = simulate(
            50e6,
            distance * 1000,
            visibility if visibility is not None else estimated_visibility,
            initial_power,
            'apd',
            1e9
        )
        modulated_outputs.append(modulated_output)
        transmitted_signals.append(transmitted_signal)
        detected_signals.append(detected_signal)
        signal_losses.append(signal_loss)

    fig2 = Figure(figsize=(10, 10), dpi=100)

    plot1 = fig2.add_subplot(411)
    for modulated_output in modulated_outputs:
        plot1.plot(modulated_output, marker='o', linestyle='-', color='b')
    plot1.set_title('Modulated Output')
    plot1.set_xlabel('Bit Index')
    plot1.set_ylabel('Power (W)')

    plot2 = fig2.add_subplot(412)
    for transmitted_signal in transmitted_signals:
        plot2.plot(transmitted_signal, marker='o', linestyle='-', color='g')
    plot2.set_title('Transmitted Signal')
    plot2.set_xlabel('Bit Index')
    plot2.set_ylabel('Power (W)')

    plot3 = fig2.add_subplot(413)
    for detected_signal in detected_signals:
        plot3.plot(detected_signal, marker='o', linestyle='-', color='r')
    plot3.set_title('Detected Signal')
    plot3.set_xlabel('Bit Index')
    plot3.set_ylabel('Power (W)')

    plot4 = fig2.add_subplot(414)
    for signal_loss in signal_losses:
        plot4.plot(signal_loss, marker='o', linestyle='-', color='m')
    plot4.set_title('Signal Loss')
    plot4.set_xlabel('Bit Index')
    plot4.set_ylabel('Power Loss (W)')

    canvas2 = FigureCanvasTkAgg(fig2, master=mainframe)
    canvas2.draw()
    canvas2.get_tk_widget().grid(column=1, row=5, columnspan=2)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)


root = tk.Tk()
root.title("Unified Interface")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))


frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

scale = tk.Scale(frame, from_=10, to=45000, orient=tk.HORIZONTAL, length=300, label="Frequency (THz)")
scale.grid(row=0, column=0, columnspan=2)
scale.bind("<Motion>", guncelle_degerler)

label_enerji = ttk.Label(frame, text="Energy:")
label_enerji.grid(row=1, column=0, sticky=tk.W)
label_enerji_deger = ttk.Label(frame, text="0 J")
label_enerji_deger.grid(row=1, column=1, sticky=tk.E)

label_dalgaboyu = ttk.Label(frame, text="Wavelength:")
label_dalgaboyu.grid(row=2, column=0, sticky=tk.W)
label_dalgaboyu_deger = ttk.Label(frame, text="0 nm")
label_dalgaboyu_deger.grid(row=2, column=1, sticky=tk.E)

label_kapasite = ttk.Label(frame, text="Channel Capacity:")
label_kapasite.grid(row=3, column=0, sticky=tk.W)
label_kapasite_deger = ttk.Label(frame, text="0 Mbps")
label_kapasite_deger.grid(row=3, column=1, sticky=tk.E)

label_isik_turu = ttk.Label(frame, text="Light Type:")
label_isik_turu.grid(row=4, column=0, sticky=tk.W)
label_isik_turu_deger = ttk.Label(frame, text="Unknown")
label_isik_turu_deger.grid(row=4, column=1, sticky=tk.E)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)
canvas.draw()

# FEL wavelength calculation section
frame_fel = ttk.Frame(root, padding="10")
frame_fel.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_lambda_u = ttk.Label(frame_fel, text="Undulator Period (m):")
label_lambda_u.grid(row=0, column=0, sticky=tk.W)
lambda_u_slider = tk.Scale(frame_fel, from_=0.01, to=1.0, orient=tk.HORIZONTAL, length=300, resolution=0.01, command=undulator_degisimi)
lambda_u_slider.set(0.3)  # Set initial value
lambda_u_slider.grid(row=0, column=1, sticky=tk.E)

label_wavelength = ttk.Label(frame_fel, text="FEL wavelength: 0 nm")
label_wavelength.grid(row=1, column=0, columnspan=2, sticky=tk.W)

# Weather and signal information display
api_key = "7af3122f7a984610bdb233022243005"
city = "Bursa"
display_weather(api_key, city)

root.mainloop()
