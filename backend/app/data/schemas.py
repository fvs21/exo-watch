from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateFeatures(BaseModel):
    orbital_period:float      # Período Orbital
    transit_epoch:float      # Época del Tránsito
    transit_duration:float     # Duración del Tránsito
    transit_depth:float        # Profundidad del Tránsito
    planet_radius:float         # Radio Planetario
    eq_temp:float           # Temperatura de Equilibrio
    insol:float
    snr:float
    steff:float       # Temperatura Estelar Efectiva
    srad:float          # Radio Estelar
