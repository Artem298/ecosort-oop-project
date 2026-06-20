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
    
class RecyclingCenter:
    """Recycling Center that processes the contents of waste bins."""

    @staticmethod
    def process_bin(waste_bin: WasteBin) -> str:
        wastes = waste_bin.empty_bin()
        if not wastes:
            return "The bin is empty. Nothing to process."

        lines = ["🚛 Garbage truck arrived. Sorting and processing the bin..."]
        for waste in wastes:
            lines.append(waste.process())
        lines.append("✨ Waste processing completed successfully!")
        return "\n".join(lines)


WASTE_CATALOG: List[tuple] = [
    # name, weight, material (None if not recyclable), type
    ("Cola Bottle", 0.5, "Plastic", WasteType.RECYCLABLE),
    ("TV Cardboard Box", 2.5, "Cardboard", WasteType.RECYCLABLE),
    ("Old Newspaper", 0.3, "Paper", WasteType.RECYCLABLE),
    ("Glass Jar", 0.4, "Glass", WasteType.RECYCLABLE),
    ("Aluminum Can", 0.1, "Aluminum", WasteType.RECYCLABLE),
    ("Apple Core", 0.1, None, WasteType.ORGANIC),
    ("Banana Peel", 0.15, None, WasteType.ORGANIC),
    ("Eggshells", 0.05, None, WasteType.ORGANIC),
    ("Leftover Pizza", 0.4, None, WasteType.ORGANIC),
    ("Used Tea Bag", 0.1, None, WasteType.ORGANIC),
    ("AA Battery", 0.02, None, WasteType.HAZARDOUS),
    ("Old Smartphone", 0.2, None, WasteType.HAZARDOUS),
    ("Mercury Thermometer", 0.1, None, WasteType.HAZARDOUS),
    ("CFL Light Bulb", 0.15, None, WasteType.HAZARDOUS),
    ("Old Paint Can", 1.2, None, WasteType.HAZARDOUS),
]


def create_waste_from_catalog_entry(entry: tuple) -> Waste:
    """Factory function: builds the correct Waste subclass from a catalog row."""
    name, weight, material, waste_type = entry
    if waste_type == WasteType.RECYCLABLE:
        return RecyclableWaste(name, weight, material)
    elif waste_type == WasteType.ORGANIC:
        return OrganicWaste(name, weight)
    else:
        return HazardousWaste(name, weight)