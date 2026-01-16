"""
Stress factor analysis tools
"""

import numpy as np
import matplotlib.pyplot as plt


class StressFactorAnalysis:
    """
    Analyze the impact of different stress factors on battery degradation.
    """
    
    def __init__(self, model):
        """
        Initialize with a degradation model.
        
        Parameters:
        -----------
        model : BaseDegradationModel
            Degradation model instance
        """
        self.model = model
    
    def temperature_sweep(self, temp_range: np.ndarray,
                         time_years: float = 10,
                         cycles_per_day: float = 1.0,
                         **kwargs):
        """
        Analyze temperature impact on degradation.
        
        Parameters:
        -----------
        temp_range : array
            Temperature range to analyze [°C]
        time_years : float
            Analysis time period [years]
        cycles_per_day : float
            Cycles per day
        **kwargs : dict
            Additional parameters
        """
        time_days = np.array([time_years * 365])
        cycles = np.array([time_years * 365 * cycles_per_day])
        
        fades = []
        for temp in temp_range:
            fade = self.model.predict_fade(time_days, cycles, temp, **kwargs)[0]
            fades.append(fade)
        
        # Plot results
        plt.figure(figsize=(10, 6))
        plt.plot(temp_range, fades, 'o-', linewidth=2, markersize=8)
        plt.xlabel('Temperature (°C)', fontsize=12, fontweight='bold')
        plt.ylabel(f'Capacity Fade after {time_years} years (%)', 
                  fontsize=12, fontweight='bold')
        plt.title('Temperature Impact on Battery Degradation', 
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        return temp_range, np.array(fades)
    
    def dod_sweep(self, dod_values: np.ndarray,
                  temperature: float = 25,
                  time_years: float = 10,
                  cycles_per_day: float = 1.0,
                  **kwargs):
        """
        Analyze DoD impact on degradation.
        """
        time_days = np.array([time_years * 365])
        cycles = np.array([time_years * 365 * cycles_per_day])
        
        fades = []
        for dod in dod_values:
            fade = self.model.predict_fade(time_days, cycles, temperature,
                                          dod=dod, **kwargs)[0]
            fades.append(fade)
        
        plt.figure(figsize=(10, 6))
        plt.plot(dod_values * 100, fades, 's-', linewidth=2, markersize=8)
        plt.xlabel('Depth of Discharge (%)', fontsize=12, fontweight='bold')
        plt.ylabel(f'Capacity Fade after {time_years} years (%)', 
                  fontsize=12, fontweight='bold')
        plt.title('DoD Impact on Battery Degradation', 
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        return dod_values, np.array(fades)
    
    def crate_sweep(self, c_rates: np.ndarray,
                   temperature: float = 25,
                   time_years: float = 10,
                   cycles_per_day: float = 1.0,
                   **kwargs):
        """
        Analyze C-rate impact on degradation.
        """
        time_days = np.array([time_years * 365])
        cycles = np.array([time_years * 365 * cycles_per_day])
        
        fades = []
        for c_rate in c_rates:
            fade = self.model.predict_fade(time_days, cycles, temperature,
                                          c_rate=c_rate, **kwargs)[0]
            fades.append(fade)
        
        plt.figure(figsize=(10, 6))
        plt.plot(c_rates, fades, '^-', linewidth=2, markersize=8)
        plt.xlabel('C-rate', fontsize=12, fontweight='bold')
        plt.ylabel(f'Capacity Fade after {time_years} years (%)', 
                  fontsize=12, fontweight='bold')
        plt.title('C-rate Impact on Battery Degradation', 
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        return c_rates, np.array(fades)


class ModelValidator:
    """
    Tools for validating models against experimental data.
    """
    
    def __init__(self, model):
        self.model = model
    
    def calculate_rmse(self, predicted: np.ndarray, 
                      actual: np.ndarray) -> float:
        """Calculate root mean square error."""
        return np.sqrt(np.mean((predicted - actual) ** 2))
    
    def calculate_mape(self, predicted: np.ndarray,
                      actual: np.ndarray) -> float:
        """Calculate mean absolute percentage error."""
        return np.mean(np.abs((predicted - actual) / actual)) * 100
