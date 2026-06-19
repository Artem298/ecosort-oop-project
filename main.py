from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional
 
 
# --- CUSTOM EXCEPTIONS ---
 
class BinOverflowError(Exception):
    """Raised when adding waste would exceed the bin's weight capacity."""
    pass

class RecyclableWaste(Waste):
    """Recyclable waste like plastic, glass, or paper."""

    def __init__(self, name: str, weight: float, material: str):
        super().__init__(name, weight)
        self.material = material

    def process(self) -> str:
        return (f"[♻️ RECYCLE] {self.weight} kg of {self.material} "
                f"({self.name}) sent to the recycling plant.")


class OrganicWaste(Waste):
    """Organic waste like food scraps. Uses the inherited constructor as-is."""

    def process(self) -> str:
        return (f"[🌱 COMPOST] {self.weight} kg of organics "
                f"({self.name}) sent to the compost heap.")


class HazardousWaste(Waste):
    """Hazardous waste like batteries or electronics. Uses the inherited constructor as-is."""

    def process(self) -> str:
        return (f"[⚠️ HAZARDOUS] {self.weight} kg of toxic waste "
                f"({self.name}) sent to safe disposal.")
    
