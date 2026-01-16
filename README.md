# Battery Degradation Modeling for Cell Life Assessment

A comprehensive toolkit for modeling and analyzing lithium-ion battery degradation with emphasis on mechanistic and semi-empirical approaches for cell life assessment.

## Overview

This project implements state-of-the-art battery degradation models based on electrochemical mechanisms and empirical relationships. The models combine physics-based understanding with data-driven approaches to predict capacity fade and power fade over the battery lifetime. The toolkit supports multiple chemistries including LFP, NMC, and NCA, with particular emphasis on understanding the underlying degradation mechanisms including SEI growth, active material loss, and lithium plating.

## Key Features

- **Mechanistic Degradation Models**: Physics-based models incorporating SEI growth, active material degradation, and lithium inventory loss
- **Semi-Empirical Approaches**: Data-driven models calibrated with experimental cycling data
- **Multi-Chemistry Support**: Models for LFP, NMC, NCA, and other lithium-ion chemistries
- **Capacity and Power Fade**: Tracks both capacity loss and resistance increase over lifetime
- **Stress Factor Analysis**: Temperature, C-rate, depth of discharge, and state of charge dependencies
- **Model Parameter Identification**: Tools for fitting models to experimental data
- **Comprehensive Validation**: Compare predictions against real cycling test data

## Scientific Background

### Degradation Mechanisms

The models implemented in this toolkit address the fundamental degradation mechanisms in lithium-ion batteries:

#### 1. **Loss of Lithium Inventory (LLI)**
- SEI layer formation and growth on anode surface
- Consumes cyclable lithium ions
- Time and temperature dependent (Arrhenius kinetics)
- Accelerated by high temperature and high state of charge

#### 2. **Loss of Active Material (LAM)**
- Particle cracking and isolation at cathode
- Active material dissolution
- Loss of electronic contact
- Dependent on cycling stress (C-rate, DoD)

#### 3. **Resistance Growth**
- SEI layer impedance increase
- Contact resistance at interfaces
- Electrolyte degradation
- Leads to power fade

#### 4. **Side Reactions**
- Lithium plating at low temperature/high C-rate
- Gas generation
- Electrolyte decomposition
- Accelerated at cell-level abuse conditions

### Model Categories

**Physics-Based Models**: Electrochemical models solving transport equations and reaction kinetics

**Semi-Empirical Models**: Combine mechanistic understanding with empirical stress factors

**Empirical Models**: Purely data-driven relationships for rapid assessment

### Key Stress Factors

- **Temperature**: Arrhenius-based acceleration of all degradation mechanisms
- **State of Charge**: Affects SEI growth rate and material stability
- **Depth of Discharge**: Mechanical stress on active materials
- **C-rate**: Transport limitations and lithium plating risk
- **Time**: SEI growth follows diffusion-limited kinetics (sqrt(t))

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
from battdegr.models import SemiEmpiricalModel
from battdegr.analysis import LifetimePredictor

# Initialize semi-empirical degradation model
model = SemiEmpiricalModel(
    chemistry='LFP',           # Battery chemistry
    capacity_nominal=50,       # Ah
    temperature=25,            # °C
    soc_mean=0.5,             # Average state of charge
    dod=0.8,                  # Depth of discharge
    c_rate_charge=1.0,        # Charge C-rate
    c_rate_discharge=1.0      # Discharge C-rate
)

# Predict capacity fade over time
time_days = [0, 365, 730, 1825, 3650]  # 0, 1, 2, 5, 10 years
cycles = [0, 365, 730, 1825, 3650]     # Daily cycling

# Calculate capacity retention
capacity_fade = model.predict_fade(time_days, cycles)
print(f"Capacity retention: {100 - capacity_fade}%")

# Analyze lifetime
predictor = LifetimePredictor(model)
eol_cycles, eol_time = predictor.estimate_lifetime(eol_threshold=0.8)
print(f"Expected lifetime: {eol_cycles} cycles or {eol_time/365:.1f} years")
```

## Usage Examples

### Mechanistic Model with SEI Growth

```python
from battdegr.models import MechanisticModel

# Create physics-based model
model = MechanisticModel(
    chemistry='NMC',
    capacity_nominal=50,        # Ah
    sei_layer_initial=10e-9,    # Initial SEI thickness (m)
    sei_growth_rate=1e-14,      # SEI growth rate constant
    ea_sei=0.4,                 # SEI activation energy (eV)
    ea_lam=0.6,                 # LAM activation energy (eV)
    lam_factor=5e-6             # Active material loss factor
)

# Run simulation
results = model.simulate(cycles=5000, temperature=25, dod=0.8)
print(f"Capacity after 5000 cycles: {results.capacity_retention*100:.1f}%")
print(f"Resistance increase: {results.resistance_growth:.1f}%")
```

### Model Parameter Identification

```python
from battdegr.calibration import ParameterOptimizer
import pandas as pd

# Load experimental cycling data
data = pd.read_csv('cycling_test_data.csv')

# Initialize optimizer
optimizer = ParameterOptimizer(
    model_type='semi_empirical',
    chemistry='LFP'
)

# Fit model to data
optimized_params = optimizer.fit(
    cycles=data['cycle'],
    capacity=data['capacity'],
    temperature=data['temperature']
)

print("Optimized parameters:")
for param, value in optimized_params.items():
    print(f"  {param}: {value:.6f}")
```

### Multi-Stress Degradation Analysis

```python
from battdegr.analysis import StressFactorAnalysis

# Analyze impact of different stress factors
analysis = StressFactorAnalysis(chemistry='NMC')

# Temperature sensitivity
analysis.temperature_sweep(range_c=[0, 60], cycles=3000)

# C-rate impact
analysis.crate_sweep(c_rates=[0.5, 1, 2, 3], temperature=25)

# DoD impact
analysis.dod_sweep(dod_values=[0.2, 0.5, 0.8, 1.0], temperature=25)

# Generate comprehensive report
analysis.generate_report('stress_analysis_report.pdf')
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

- **Author**: Phillip Weiner
- **Email**: [Contact through GitHub](https://github.com/pweiner930)
- **Issues**: [GitHub Issues](https://github.com/pweiner930/battdegr/issues)

## Acknowledgments

This work builds upon extensive research in LFP battery degradation modeling. Key references and acknowledgments are provided in the [documentation](docs/research.md).

---

**Note**: This project is under active development. APIs may change in early versions.