"""
Lifetime prediction and end-of-life assessment tools
"""

import numpy as np
from typing import Tuple, Optional
import matplotlib.pyplot as plt


class LifetimePredictor:
    """
    Tools for predicting battery lifetime and end-of-life.
    """
    
    def __init__(self, model):
        """
        Initialize with a degradation model.
        
        Parameters:
        -----------
        model : BaseDegradationModel
            Any degradation model instance
        """
        self.model = model
    
    def estimate_lifetime(self, temperature: float, 
                         cycles_per_day: float = 1.0,
                         eol_threshold: float = 0.8,
                         max_years: int = 30,
                         **kwargs) -> Tuple[float, float]:
        """
        Estimate battery lifetime to reach EOL.
        
        Parameters:
        -----------
        temperature : float
            Operating temperature [°C]
        cycles_per_day : float
            Average cycles per day
        eol_threshold : float
            End-of-life capacity retention [0-1]
        max_years : int
            Maximum years to simulate
        **kwargs : dict
            Additional parameters (soc_avg, dod, c_rate, etc.)
            
        Returns:
        --------
        eol_time : float
            Time to EOL [days]
        eol_cycles : float
            Cycles to EOL
        """
        # Create time and cycle arrays
        time_days = np.linspace(0, max_years * 365, max_years * 365)
        cycles = time_days * cycles_per_day
        
        # Predict fade
        fade = self.model.predict_fade(time_days, cycles, temperature, **kwargs)
        retention = 1.0 - (fade / 100.0)
        
        # Find EOL point
        idx = np.where(retention <= eol_threshold)[0]
        if len(idx) > 0:
            eol_time = time_days[idx[0]]
            eol_cycles = cycles[idx[0]]
        else:
            eol_time = np.inf
            eol_cycles = np.inf
        
        return eol_time, eol_cycles
    
    def plot_lifetime_prediction(self, temperature: float,
                                cycles_per_day: float = 1.0,
                                eol_threshold: float = 0.8,
                                **kwargs):
        """
        Plot capacity retention over lifetime.
        """
        max_years = 25
        time_days = np.linspace(0, max_years * 365, 500)
        cycles = time_days * cycles_per_day
        
        fade = self.model.predict_fade(time_days, cycles, temperature, **kwargs)
        retention = 1.0 - (fade / 100.0)
        
        time_years = time_days / 365.0
        
        plt.figure(figsize=(10, 6))
        plt.plot(time_years, retention * 100, 'b-', linewidth=2, 
                label=f'{temperature}°C')
        plt.axhline(y=eol_threshold * 100, color='r', linestyle='--', 
                   linewidth=2, label=f'EOL ({eol_threshold*100}%)')
        
        plt.xlabel('Time (years)', fontsize=12, fontweight='bold')
        plt.ylabel('Capacity Retention (%)', fontsize=12, fontweight='bold')
        plt.title('Battery Lifetime Prediction', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(70, 105)
        
        plt.tight_layout()
        plt.show()
    
    def compare_scenarios(self, scenarios: dict,
                         cycles_per_day: float = 1.0,
                         eol_threshold: float = 0.8):
        """
        Compare lifetime under different operating scenarios.
        
        Parameters:
        -----------
        scenarios : dict
            Dictionary of {name: {'temperature': T, 'soc_avg': S, ...}}
        cycles_per_day : float
            Cycles per day
        eol_threshold : float
            EOL threshold
        """
        results = {}
        
        for name, params in scenarios.items():
            temp = params['temperature']
            kwargs = {k: v for k, v in params.items() if k != 'temperature'}
            
            eol_time, eol_cycles = self.estimate_lifetime(
                temp, cycles_per_day, eol_threshold, **kwargs
            )
            
            results[name] = {
                'eol_years': eol_time / 365.0,
                'eol_cycles': eol_cycles,
                'temperature': temp
            }
        
        # Print results
        print("Lifetime Comparison")
        print("=" * 70)
        print(f"{'Scenario':<25} {'Temperature':<15} {'EOL Years':<15} {'EOL Cycles'}")
        print("-" * 70)
        
        for name, res in results.items():
            eol_str = f"{res['eol_years']:.1f}" if np.isfinite(res['eol_years']) else ">30"
            cyc_str = f"{res['eol_cycles']:.0f}" if np.isfinite(res['eol_cycles']) else ">10000"
            print(f"{name:<25} {res['temperature']:<15.1f} {eol_str:<15} {cyc_str}")
        
        print("=" * 70)
        
        return results
