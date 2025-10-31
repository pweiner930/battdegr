# Mathematical Models for LFP Battery Degradation

## Overview

This document describes the mathematical formulations used in the LFP battery degradation models.

## Calendar Aging Model

### Basic Arrhenius-Based Model

The calendar aging capacity loss follows an Arrhenius temperature dependence:

```
Q_loss_cal(t, T, SoC) = A_cal * sqrt(t) * exp(-Ea_cal / (R*T)) * f_SoC(SoC)
```

**Parameters:**
- `Q_loss_cal`: Calendar capacity loss (%)
- `t`: Time (days or years)
- `T`: Temperature (K)
- `SoC`: State of Charge (0-1)
- `A_cal`: Pre-exponential factor
- `Ea_cal`: Activation energy for calendar aging (~0.65 eV)
- `R`: Gas constant (8.314 J/mol·K)

### SoC Dependence Function

The SoC stress factor for LFP batteries:

```
f_SoC(SoC) = 1 + α * (SoC - 0.5)²
```

Where `α` is the SoC stress coefficient (~0.3 for LFP).

## Cycle Aging Model

### Cycle-Based Capacity Loss

```
Q_loss_cyc(N, DoD, T, C_rate) = B_cyc * N^β * g_DoD(DoD) * h_T(T) * i_C(C_rate)
```

**Parameters:**
- `Q_loss_cyc`: Cycle capacity loss (%)
- `N`: Number of cycles
- `DoD`: Depth of Discharge (0-1)
- `C_rate`: Charge/discharge rate (C)
- `B_cyc`: Cycle aging coefficient
- `β`: Power law exponent (~0.5-0.8)

### DoD Stress Function

For utility-scale applications (typically 100% DoD):

```
g_DoD(DoD) = DoD^γ
```

Where `γ` is the DoD stress exponent (~1.1 for LFP).

### Temperature Function for Cycling

```
h_T(T) = exp(-Ea_cyc / (R*T))
```

With `Ea_cyc` ≈ 0.3-0.4 eV for cycle aging.

### C-rate Function

```
i_C(C_rate) = 1 + δ * max(0, C_rate - 1)
```

Where `δ` is the C-rate stress coefficient.

## Combined Model

### Superposition Approach

The total capacity loss combines calendar and cycle aging:

```
Q_total(t, N, T, SoC, DoD, C_rate) = Q_loss_cal(t, T, SoC) + Q_loss_cyc(N, DoD, T, C_rate)
```

### Interactive Model

For more accurate predictions, include interaction terms:

```
Q_total = Q_cal + Q_cyc + Q_interaction
```

Where:
```
Q_interaction = k_int * Q_cal * Q_cyc
```

## Advanced Models

### Multi-Physics Model

Incorporating SEI growth kinetics:

```
dQ/dt = k_SEI(T, SoC) * sqrt(Q_consumed) + k_cycle(T, DoD) * dN/dt
```

### State-Space Representation

For real-time applications:

```
x[k+1] = A*x[k] + B*u[k]
y[k] = C*x[k]
```

Where:
- `x`: State vector (capacity, resistance)
- `u`: Input vector (temperature, current)
- `y`: Output (measurable capacity)

## Parameter Values for LFP

### Typical Parameter Ranges

| Parameter | Value Range | Units | Notes |
|-----------|-------------|-------|-------|
| A_cal | 0.01-0.1 | %/sqrt(year) | Pre-exponential factor |
| Ea_cal | 0.6-0.8 | eV | Calendar activation energy |
| B_cyc | 1e-6 to 1e-4 | %/cycle^β | Cycle aging coefficient |
| β | 0.5-0.8 | - | Power law exponent |
| α | 0.1-0.5 | - | SoC stress coefficient |
| γ | 1.0-1.2 | - | DoD stress exponent |

### Temperature-Specific Coefficients

For different temperature ranges:

```python
# Low temperature (0-25°C)
Ea_cal_low = 0.7  # eV
A_cal_low = 0.05  # %/sqrt(year)

# Moderate temperature (25-40°C)  
Ea_cal_mod = 0.65  # eV
A_cal_mod = 0.08  # %/sqrt(year)

# High temperature (40-60°C)
Ea_cal_high = 0.6  # eV  
A_cal_high = 0.12  # %/sqrt(year)
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