"""
BattDegr: Battery Degradation Modeling for Cell Life Assessment

A comprehensive toolkit for modeling lithium-ion battery degradation using
mechanistic, semi-empirical, and data-driven approaches.
"""

__version__ = "0.1.0"
__author__ = "Paul Weiner"

from .models import (
    MechanisticModel,
    SemiEmpiricalModel,
    EmpiricalModel
)

from .analysis import (
    LifetimePredictor,
    StressFactorAnalysis,
    ModelValidator
)

__all__ = [
    "MechanisticModel",
    "SemiEmpiricalModel",
    "EmpiricalModel",
    "LifetimePredictor",
    "StressFactorAnalysis",
    "ModelValidator",
]
