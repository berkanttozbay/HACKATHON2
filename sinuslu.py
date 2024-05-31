import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Planck sabiti ve ışık hızı
h = 6.62607015e-34  # Planck sabiti (Joule*saniye)
c = 3.0e8           # Işık hızı (metre/saniye)

# Shannon-Hartley teoremi ile kanal kapasitesi hesaplama fonksiyonu
def calculate_channel_capacity(bandwidth, signal_power, noise_power):
    capacity = bandwidth * np.log2(1 + (signal_power / noise_power))
    return capacity / 1e6  # Mbps cinsinden döndür

# Enerji ve dalga boyu hesaplama fonksiyonları
def hesapla_enerji(frekans):
    return h * frekans

def hesapla_dalgaboyu(frekans):
    return (c / frekans) * 1e9  # Nanometre cinsinden dalga boyu

# Frekans aralığına göre ışık türünü belirleyen fonksiyon
def belirle_isik_turu(frekans):
    if frekans >= 3e19:
        return "Gamma Işını"
    elif 3e16 <= frekans < 3e19:
        return "X Işını"
    elif 8e14 <= frekans < 3e16:
        return "Morötesi Işık"
    elif 4e14 <= frekans < 8e14:
        return "Görünür Işık"
    elif 3e11 <= frekans < 4e14:
        return "Kızılötesi Işık"
    elif 1e9 <= frekans < 3e11:
        return "Mikrodalga"
    else:
        return "Radyo Dalgası"

# Kaydırma çubuğunun değerini güncelleme fonksiyonu
def guncelle_degerler(event):
    frekans = scale.get() * 1e12  # Frekansı terahertz cinsinden al
    enerji = hesapla_enerji(frekans)
    dalgaboyu = hesapla_dalgaboyu(frekans)
    
    # Kanal kapasitesini hesapla
    signal_power = 1e-3  # 1 mW
    noise_power = 1e-6   # 1 µW
    bandwidth = frekans
    kapasite = calculate_channel_capacity(bandwidth, signal_power, noise_power)
    
    isik_turu = belirle_isik_turu(frekans)
    
    label_enerji_deger.config(text=f"{enerji:.2e} J")
    label_dalgaboyu_deger.config(text=f"{dalgaboyu:.2f} nm")
    label_kapasite_deger.config(text=f"{kapasite:.2f} Mbps")
    label_isik_turu_deger.config(text=isik_turu)
    
    # Frekansı grafikte güncelle
    update_graph(frekans)

# Frekansı güncelleyen grafik fonksiyonu
def update_graph(frekans):
    t = np.linspace(0, 1, 1000)  # 1 saniyelik zaman aralığında 1000 örnek
    y = np.sin(2 * np.pi * (frekans / 1e12) * t)
    ax.clear()
    ax.plot(t, y)
    ax.set_title(f"Frekans: {frekans / 1e12:.2f} THz")
    ax.set_xlabel("Zaman (s)")
    ax.set_ylabel("Genlik")
    canvas.draw()

# Tkinter penceresi oluşturma
root = tk.Tk()
root.title("Frekans Kaydırma Çubuğu")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Frekans kaydırma çubuğu
scale = tk.Scale(frame, from_=10, to=45000, orient=tk.HORIZONTAL, length=300, label="Frekans (THz)")
scale.grid(row=0, column=0, columnspan=2)
scale.bind("<Motion>", guncelle_degerler)

# Enerji etiketi
label_enerji = ttk.Label(frame, text="Enerji:")
label_enerji.grid(row=1, column=0, sticky=tk.W)
label_enerji_deger = ttk.Label(frame, text="0 J")
label_enerji_deger.grid(row=1, column=1, sticky=tk.E)

# Dalga boyu etiketi
label_dalgaboyu = ttk.Label(frame, text="Dalga Boyu:")
label_dalgaboyu.grid(row=2, column=0, sticky=tk.W)
label_dalgaboyu_deger = ttk.Label(frame, text="0 nm")
label_dalgaboyu_deger.grid(row=2, column=1, sticky=tk.E)

# Kanal kapasitesi etiketi
label_kapasite = ttk.Label(frame, text="Kanal Kapasitesi:")
label_kapasite.grid(row=3, column=0, sticky=tk.W)
label_kapasite_deger = ttk.Label(frame, text="0 Mbps")
label_kapasite_deger.grid(row=3, column=1, sticky=tk.E)

# Işık türü etiketi
label_isik_turu = ttk.Label(frame, text="Işık Türü:")
label_isik_turu.grid(row=4, column=0, sticky=tk.W)
label_isik_turu_deger = ttk.Label(frame, text="Bilinmiyor")
label_isik_turu_deger.grid(row=4, column=1, sticky=tk.E)

# Matplotlib figürü ve ekseni oluşturma
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)
ax.set_title("Dalga Grafiği")
ax.set_xlabel("Zaman (s)")
ax.set_ylabel("Genlik")

# Pencereyi çalıştırma
