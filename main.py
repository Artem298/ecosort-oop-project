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
    
class WasteType(Enum):
    RECYCLABLE = "1"
    ORGANIC = "2"
    HAZARDOUS = "3"

class WasteBin:
    """Waste bin with weight capacity constraints.

    All internal state is private. External code must use the public
    methods/properties below — never reach into _capacity, _current_weight,
    or _contents directly.
    """

    def __init__(self, capacity: float):
        self._capacity = capacity
        self._current_weight = 0.0
        self._contents: List[Waste] = []

    @property
    def capacity(self) -> float:
        """Read-only access to capacity. No setter: capacity is fixed at creation."""
        return self._capacity

    @property
    def current_weight(self) -> float:
        """Read-only access to current weight. Cannot be set directly from outside."""
        return self._current_weight

    @property
    def free_space(self) -> float:
        return self._capacity - self._current_weight

    @property
    def item_count(self) -> int:
        return len(self._contents)

    def add_waste(self, waste: Waste) -> None:
        """Add a waste item to the bin.

        Raises:
            BinOverflowError: if adding this item would exceed capacity.
        """
        if self._current_weight + waste.weight > self._capacity:
            raise BinOverflowError(
                f"Cannot add '{waste.name}' ({waste.weight} kg): "
                f"only {self.free_space:.2f} kg of free space left."
            )
        self._contents.append(waste)
        self._current_weight += waste.weight

    def empty_bin(self) -> List[Waste]:
        """Remove and return all contents, resetting the bin to empty."""
        contents = self._contents
        self._contents = []
        self._current_weight = 0.0
        return contents

    def describe_contents(self) -> str:
        """Human-readable summary of what's currently inside the bin."""
        if not self._contents:
            return "The bin is currently empty."
        lines = [f"  {idx}. {w.name} ({w.weight} kg)"
                  for idx, w in enumerate(self._contents, start=1)]
        return "\n".join(lines)