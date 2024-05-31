import numpy as np

class Laser:
    def __init__(self, wavelength=1550e-9, threshold_current=9.784e-3, slope_efficiency=0.5):
        self.wavelength = wavelength
        self.threshold_current = threshold_current
        self.slope_efficiency = slope_efficiency

    def output_power(self, current):
        if current < self.threshold_current:
            return 0
        else:
            return self.slope_efficiency * (current - self.threshold_current)

    def modulate(self, data, bias_current):
        output = []
        for bit in data:
            if bit == 1:
                output.append(self.output_power(bias_current + 1e-3))
            else:
                output.append(self.output_power(bias_current))
        return np.array(output)

    def adjust_power(self, visibility):
        if visibility < 50:
            self.slope_efficiency *= 0.8
        elif visibility < 100:
            self.slope_efficiency *= 0.9
        else:
            self.slope_efficiency *= 1.0
