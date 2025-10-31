# Lithium Iron Phosphate Battery Degradation Models

A comprehensive toolkit for modeling and analyzing LFP battery degradation in utility-scale energy storage applications.

## Overview

This project implements degradation models for Lithium Iron Phosphate (LFP) batteries specifically designed for utility-scale energy storage systems. The models account for both calendar aging (time-dependent degradation) and cycle aging (usage-dependent degradation) under typical grid operation conditions of one full charge-discharge cycle per day at 100% Depth of Discharge (DoD).

## Key Features

- **Comprehensive Degradation Modeling**: Combines calendar and cycling effects for accurate State of Health (SoH) predictions
- **Temperature-Dependent Analysis**: Models the critical impact of temperature on LFP battery aging
- **Utility-Scale Focus**: Optimized for grid applications with daily 100% DoD cycling
- **Multiple Model Types**: Supports both empirical and semi-empirical degradation models
- **Long-Term Predictions**: Designed for multi-year battery lifecycle analysis
- **Visualization Tools**: Generate plots and reports for capacity fade analysis

## Scientific Background

### LFP Battery Characteristics

Lithium Iron Phosphate batteries are increasingly used in utility-scale energy storage due to their:
- **Exceptional Cycle Life**: Commercial LFP/graphite cells demonstrate >5,000 full cycles at room temperature
- **Chemical Stability**: LFP's olivine cathode structure resists transition metal dissolution and lattice collapse
- **Deep Discharge Tolerance**: Lower nominal voltage (~3.3V) reduces electrolyte oxidation
- **SoC Tolerance**: Less sensitive to high State of Charge compared to NMC/NCA chemistries

### Degradation Mechanisms

The primary degradation mechanisms modeled include:

1. **Solid-Electrolyte Interphase (SEI) Growth**: The dominant mechanism causing loss of lithium inventory (LLI)
2. **Calendar Aging**: Time-dependent degradation occurring even during storage
3. **Cycle Aging**: Usage-dependent degradation from charge-discharge cycles
4. **Temperature Effects**: Accelerated aging at elevated temperatures

### Key Degradation Factors

- **Temperature**: Most influential factor - 40°C causes 1.3× faster aging, 55°C causes ~5× faster aging compared to 25°C
- **State of Charge**: High SoC accelerates SEI formation
- **Charge/Discharge Rates**: High C-rates can induce additional stress
- **Depth of Discharge**: Deep cycling effects on capacity retention

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Repository

```bash
git clone https://github.com/pweiner930/battdegr.git
cd battdegr
pip install -r requirements.txt
pip install -e .
```

### Install from PyPI (when available)

```bash
pip install battdegr
```

## Quick Start

```python
import battdegr
from battdegr.models import LFPDegradationModel
from battdegr.analysis import BatteryAnalyzer

# Initialize LFP degradation model
model = LFPDegradationModel(
    temperature=25,  # °C
    dod=100,        # % Depth of Discharge
    cycle_frequency=1  # cycles per day
)

# Predict capacity over time
time_years = [0, 1, 2, 5, 10, 15, 20]
capacity_retention = model.predict_capacity(time_years)

# Analyze results
analyzer = BatteryAnalyzer(model)
analyzer.plot_degradation_curve(time_years, capacity_retention)
analyzer.generate_report()
```

## Usage Examples

### Basic Degradation Modeling

```python
# Create model for utility-scale operation
model = LFPDegradationModel(
    initial_capacity=100,    # Ah
    temperature=30,          # °C
    dod=100,                # %
    eol_threshold=80        # % capacity for end-of-life
)

# Predict when battery reaches end-of-life
eol_years = model.calculate_eol()
print(f"Expected battery life: {eol_years:.1f} years")
```

### Temperature Sensitivity Analysis

```python
from battdegr.analysis import TemperatureAnalysis

# Compare degradation at different temperatures
temps = [20, 25, 30, 35, 40, 45]
temp_analysis = TemperatureAnalysis(temperatures=temps)
temp_analysis.run_comparison()
temp_analysis.plot_temperature_effects()
```

### Custom Degradation Parameters

```python
# Advanced model with custom parameters
advanced_model = LFPDegradationModel(
    sei_growth_rate=0.002,      # Custom SEI formation rate
    temperature_activation=0.65, # eV, activation energy
    calendar_factor=0.1,         # Calendar aging coefficient
    cycle_factor=0.05           # Cycle aging coefficient
)
```

## Project Structure

```
battdegr/
├── README.md                    # This file
├── setup.py                     # Package installation
├── requirements.txt             # Dependencies
├── src/
│   └── battdegr/
│       ├── __init__.py
│       ├── models/              # Degradation models
│       │   ├── __init__.py
│       │   ├── base_model.py
│       │   ├── lfp_model.py
│       │   └── empirical_models.py
│       ├── analysis/            # Analysis tools
│       │   ├── __init__.py
│       │   ├── analyzer.py
│       │   ├── temperature.py
│       │   └── visualization.py
│       └── utils/               # Utility functions
│           ├── __init__.py
│           ├── data_processing.py
│           └── validation.py
├── data/                        # Sample datasets
│   ├── experimental/
│   └── validation/
├── docs/                        # Documentation
│   ├── api/                     # API reference
│   ├── models/                  # Model documentation
│   └── examples/                # Usage examples
├── tests/                       # Unit tests
│   ├── test_models.py
│   ├── test_analysis.py
│   └── test_utils.py
├── examples/                    # Example scripts and notebooks
│   ├── basic_usage.py
│   ├── temperature_analysis.ipynb
│   └── utility_scale_analysis.ipynb
└── scripts/                     # Utility scripts
    ├── validate_models.py
    └── generate_reports.py
```

## Documentation

- **[API Reference](docs/api/README.md)**: Complete API documentation
- **[Model Documentation](docs/models/README.md)**: Detailed model descriptions and equations
- **[Examples](examples/)**: Jupyter notebooks and scripts demonstrating usage
- **[Research Background](docs/research.md)**: Scientific foundation and literature review

## Models Implemented

### Calendar Aging Models
- Arrhenius temperature dependence
- SoC-dependent aging rates
- SEI growth kinetics

### Cycle Aging Models
- DoD-dependent capacity fade
- C-rate effects on degradation
- Cycle counting algorithms

### Combined Models
- Superposition of calendar and cycle aging
- Temperature-SoC interaction effects
- Multi-physics degradation models

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/pweiner930/battdegr.git
cd battdegr
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this software in your research, please cite:

```bibtex
@software{battdegr,
    title={BattDegr: LFP Battery Degradation Models for Utility-Scale Applications},
    author={Weiner, P.},
    year={2025},
    url={https://github.com/pweiner930/battdegr}
}
```

## Contact

- **Author**: Paul Weiner
- **Email**: [Contact through GitHub](https://github.com/pweiner930)
- **Issues**: [GitHub Issues](https://github.com/pweiner930/battdegr/issues)

## Acknowledgments

This work builds upon extensive research in LFP battery degradation modeling. Key references and acknowledgments are provided in the [documentation](docs/research.md).

---

**Note**: This project is under active development. APIs may change in early versions.