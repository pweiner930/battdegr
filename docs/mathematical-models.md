# Mathematical Models for Battery Degradation and Cell Life Assessment

## Overview

This document describes the mathematical formulations used in mechanistic and semi-empirical battery degradation models for cell life assessment. The models are based on fundamental electrochemical principles and validated against experimental cycling data.

## Mechanistic Model: SEI Layer Growth

### SEI Formation and Growth

The solid-electrolyte interphase (SEI) layer grows according to a parabolic law (diffusion-limited growth):

```
δ_SEI(t) = δ_SEI,0 + k_SEI * sqrt(t)
```

Where:
- `δ_SEI`: SEI layer thickness (m)
- `δ_SEI,0`: Initial SEI thickness (typically 10-50 nm)
- `k_SEI`: SEI growth rate constant (m/s^0.5)
- `t`: Time (s)

### Temperature Dependence (Arrhenius)

The SEI growth rate follows Arrhenius kinetics:

```
k_SEI(T) = k_SEI,ref * exp(-Ea_SEI/R * (1/T - 1/T_ref))
```

**Parameters:**
- `Ea_SEI`: Activation energy for SEI growth (typically 0.3-0.5 eV)
- `R`: Gas constant (8.314 J/mol·K or 8.617e-5 eV/K)
- `T`: Absolute temperature (K)
- `T_ref`: Reference temperature (typically 298 K)

### SoC Dependence of SEI Growth

The SEI growth rate depends on electrode potential (related to SoC):

```
k_SEI(SoC) = k_SEI,ref * exp(β_SEI * (SoC - SoC_ref))
```

Where:
- `β_SEI`: SoC sensitivity coefficient (typically 1-3)
- `SoC_ref`: Reference state of charge (typically 0.5)

### Capacity Loss from SEI Growth

The capacity loss due to lithium inventory loss (LLI) from SEI formation:

```
Q_loss_SEI(t) = (n_Li_consumed / n_Li_total) * 100%
```

Where:
```
n_Li_consumed = A_electrode * δ_SEI * ρ_SEI / M_SEI
```

- `A_electrode`: Electrode active area (m²)
- `ρ_SEI`: SEI layer density (kg/m³)
- `M_SEI`: Molar mass of SEI components (kg/mol)

## Active Material Loss (LAM) Model

### Mechanical Stress-Induced Degradation

Active material loss occurs through particle cracking, isolation, and dissolution:

```
Q_loss_LAM(N, ΔU) = k_LAM * N^α * f_stress(ΔU) * exp(-Ea_LAM/RT)
```

**Parameters:**
- `Q_loss_LAM`: Capacity loss from active material loss (%)
- `N`: Number of cycles
- `α`: Power law exponent for cycling (typically 0.5-0.75)
- `ΔU`: Voltage swing during cycling (V)
- `k_LAM`: LAM rate constant
- `Ea_LAM`: Activation energy for LAM (typically 0.4-0.8 eV)

### Stress Function (DoD and C-rate Dependence)

```
f_stress(DoD, C_rate) = (DoD)^p * (1 + q * (C_rate - 1))
```

Where:
- `p`: DoD stress exponent (typically 1.5-2.5)
- `q`: C-rate stress coefficient (typically 0.3-0.7)
- DoD: Depth of discharge (0-1)

### Cathode-Specific LAM

For different cathode chemistries:

**NMC/NCA:**
```
Q_LAM_NMC = k_LAM * N^0.6 * DoD^2 * exp(-0.6eV / kT)
```

**LFP:**
```
Q_LAM_LFP = k_LAM * N^0.5 * DoD^1.5 * exp(-0.8eV / kT)
```

LFP shows higher activation energy due to stable olivine structure.

### Lithium Plating Model

Lithium plating occurs at low temperature or high C-rate charging:

```
Q_plating = k_pl * N * max(0, I - I_lim(T))^2
```

Where:
- `I`: Charging current (A)
- `I_lim(T)`: Temperature-dependent current limit
```
I_lim(T) = I_ref * exp(-Ea_ct/R * (1/T - 1/T_ref))
```

Plating leads to irreversible lithium loss and accelerated capacity fade.

## Semi-Empirical Combined Model

### Weighted Superposition

The total capacity fade combines multiple degradation mechanisms:

```
Q_fade_total = Q_SEI + Q_LAM + Q_plating + Q_interaction
```

### Calendar-Cycle Interaction

Realistic models include non-linear interaction between calendar and cycle aging:

```
Q_total(t, N) = w_cal * Q_cal(t) + w_cyc * Q_cyc(N) + w_int * Q_cal(t) * Q_cyc(N)
```

Where weights sum to unity: `w_cal + w_cyc + w_int = 1`

### General Semi-Empirical Form

A widely-used general model structure:

```
Q_fade(t, N, T, SoC, DoD, C) = A * t^z * N^p * exp(-Ea/RT) * f(SoC) * g(DoD) * h(C)
```

**Stress Factor Functions:**

```
f(SoC) = exp(k_soc * SoC)                    # SoC stress
g(DoD) = DoD^m                                # DoD stress  
h(C) = C^n                                    # C-rate stress
```

Typical parameter ranges:
- `z`: 0.5-0.75 (time exponent, from SEI diffusion)
- `p`: 0.5-0.8 (cycle exponent, from LAM)
- `Ea`: 0.3-0.7 eV (combined activation energy)
- `m`: 1.5-2.5 (DoD exponent)
- `n`: 0.5-1.5 (C-rate exponent)

### Resistance Growth Model

Power fade due to impedance increase:

```
R_increase(t, N, T) = R_SEI(t) + R_contact(N) + R_electrolyte(t, T)
```

**SEI Resistance:**
```
R_SEI(t) = R_SEI,0 + k_R * sqrt(t) * exp(-Ea_R / RT)
```

**Contact Resistance from LAM:**
```
R_contact(N) = R_c,0 * (1 + k_c * N^α)
```

## Advanced Modeling Approaches

### Differential Equation System

Complete electrochemical model with coupled degradation:

```
dC/dt = -k_SEI(T, V) * sqrt(t) - k_LAM(T) * (dN/dt)
dR/dt = α_R * dδ_SEI/dt + β_R * dLAM/dt
dδ_SEI/dt = k_SEI(T, V) / (2 * sqrt(t))
```

Where:
- `C`: Remaining capacity
- `R`: Internal resistance
- `δ_SEI`: SEI layer thickness
- `V`: Electrode potential (function of SoC)

### State-Space Degradation Model

For online estimation and prediction:

**State vector:**
```
x = [C, R, δ_SEI, LAM]^T
```

**State equations:**
```
x[k+1] = f(x[k], u[k], w[k])
y[k] = h(x[k], v[k])
```

**Inputs:**
```
u = [I, T, SoC]^T
```

**Measurements:**
```
y = [C_measured, R_measured]^T
```

This enables Kalman filtering for real-time state estimation.

### Probabilistic Degradation Model

Accounts for cell-to-cell variation:

```
Q_fade ~ Normal(μ(t, N, T), σ²(t, N))
```

Where mean and variance evolve according to:
```
μ(t) = μ_0 + k_mean * t^z * N^p
σ²(t) = σ²_0 + k_var * t
```

### Bayesian Parameter Estimation

Update model parameters with new data:

```
p(θ | D) ∝ p(D | θ) * p(θ)
```

Where:
- `θ`: Model parameters
- `D`: Experimental data
- `p(θ)`: Prior distribution
- `p(D | θ)`: Likelihood
- `p(θ | D)`: Posterior distribution

## Model Parameters by Chemistry

### LFP/Graphite Parameters

| Parameter | Value | Units | Source/Notes |
|-----------|-------|-------|--------------|
| k_SEI,ref | 1-5 × 10^-14 | m/s^0.5 | SEI growth rate at 25°C |
| Ea_SEI | 0.3-0.4 | eV | SEI formation activation energy |
| β_SEI | 1.5-2.5 | - | SoC sensitivity |
| k_LAM | 1-10 × 10^-5 | %/cycle^α | LAM rate constant |
| α_LAM | 0.5-0.6 | - | Cycle exponent for LAM |
| Ea_LAM | 0.7-0.9 | eV | LAM activation energy (high due to stable structure) |
| p_DoD | 1.2-1.5 | - | DoD stress exponent |

### NMC/Graphite Parameters

| Parameter | Value | Units | Source/Notes |
|-----------|-------|-------|--------------|
| k_SEI,ref | 2-8 × 10^-14 | m/s^0.5 | SEI growth rate at 25°C |
| Ea_SEI | 0.4-0.5 | eV | SEI formation activation energy |
| β_SEI | 2.0-3.5 | - | SoC sensitivity (higher than LFP) |
| k_LAM | 5-20 × 10^-5 | %/cycle^α | LAM rate constant |
| α_LAM | 0.6-0.75 | - | Cycle exponent for LAM |
| Ea_LAM | 0.4-0.6 | eV | LAM activation energy (lower than LFP) |
| p_DoD | 2.0-2.5 | - | DoD stress exponent (more sensitive) |

### NCA/Graphite Parameters

| Parameter | Value | Units | Source/Notes |
|-----------|-------|-------|--------------|
| k_SEI,ref | 3-10 × 10^-14 | m/s^0.5 | SEI growth rate at 25°C |
| Ea_SEI | 0.45-0.55 | eV | SEI formation activation energy |
| β_SEI | 2.5-4.0 | - | SoC sensitivity (highest) |
| k_LAM | 8-25 × 10^-5 | %/cycle^α | LAM rate constant |
| α_LAM | 0.65-0.8 | - | Cycle exponent for LAM |
| Ea_LAM | 0.35-0.55 | eV | LAM activation energy |
| p_DoD | 2.2-3.0 | - | DoD stress exponent |

### Universal Constants

```python
# Physical constants
R_gas = 8.314  # J/(mol·K)
R_gas_eV = 8.617e-5  # eV/K
F = 96485  # C/mol (Faraday constant)

# SEI properties
rho_SEI = 1600  # kg/m³ (SEI density)
M_SEI = 0.162  # kg/mol (effective molar mass)
delta_SEI_0 = 10e-9  # m (initial SEI thickness, ~10 nm)

# Typical ranges
T_ref = 298.15  # K (25°C reference)
SoC_ref = 0.5  # Reference state of charge
```

## Model Validation

### Goodness of Fit Metrics

1. **Root Mean Square Error (RMSE)**:
   ```
   RMSE = sqrt(mean((y_pred - y_actual)²))
   ```

2. **Mean Absolute Percentage Error (MAPE)**:
   ```
   MAPE = mean(|y_pred - y_actual| / y_actual) * 100%
   ```

3. **R-squared**:
   ```
   R² = 1 - SS_res / SS_tot
   ```

### Cross-Validation Approach

- K-fold cross validation (k=5)
- Train/validation/test split (60/20/20)
- Time-series aware splitting for temporal data

## Implementation Notes

### Numerical Considerations

1. **Time Step Selection**: 
   - Daily time steps for calendar aging
   - Cycle-based updates for cycle aging

2. **Convergence Criteria**:
   - Relative tolerance: 1e-6
   - Maximum iterations: 1000

3. **Boundary Conditions**:
   - Temperature limits: -20°C to 80°C
   - SoC limits: 0% to 100%
   - DoD limits: 0% to 100%

### Computational Complexity

- Calendar aging: O(1) per time step
- Cycle aging: O(1) per cycle
- Combined model: O(n) where n is number of time steps

---

For implementation examples, see [../examples/](../../examples/) directory.