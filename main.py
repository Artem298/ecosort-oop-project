from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional


# --- CUSTOM EXCEPTIONS ---

class BinOverflowError(Exception):
    """Raised when adding waste would exceed the bin's weight capacity."""
    pass


# --- BASE CLASSES (Abstraction) ---

class Waste(ABC):
    """Abstract base class for all waste types."""

    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    @abstractmethod
    def process(self) -> str:
        """Processing method to be implemented by subclasses."""
        pass


# --- SUBCLASSES (Inheritance & Polymorphism) ---

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


# --- ENUM (replaces magic strings "1"/"2"/"3") ---

class WasteType(Enum):
    RECYCLABLE = "1"
    ORGANIC = "2"
    HAZARDOUS = "3"


# --- MANAGEMENT CLASSES (Encapsulation) ---

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


# --- WASTE CATALOG (single source of truth, no duplicated magic strings) ---

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


# --- INTERACTIVE APPLICATION (menu logic kept out of free-floating script code) ---

class EcoSortApp:
    """Encapsulates the interactive console menu and ties it to the domain classes."""

    def __init__(self):
        self._bin: Optional[WasteBin] = None

    def run(self) -> None:
        print("🗑️ Welcome to EcoSort: Interactive Waste Management System!")
        self._bin = WasteBin(capacity=self._prompt_for_capacity())

        actions = {
            "1": self._handle_add_item,
            "2": self._handle_view_status,
            "3": self._handle_process_bin,
        }

        while True:
            self._show_menu()
            choice = input("Select an option (1-4): ").strip()

            if choice == "4":
                print("👋 Thank you for using EcoSort. Keep the planet clean!")
                break

            action = actions.get(choice)
            if action is None:
                print("❌ Invalid option. Please try again.")
                continue
            action()

    @staticmethod
    def _prompt_for_capacity() -> float:
        try:
            return float(input("Enter waste bin capacity limit (in kg, e.g., 15): "))
        except ValueError:
            print("Invalid input. Default capacity set to 15.0 kg.")
            return 15.0

    @staticmethod
    def _show_menu() -> None:
        print("\n=== MAIN MENU ===")
        print("1. Add an item from the Catalog (15 items)")
        print("2. View current bin status")
        print("3. Send bin to the Recycling Center")
        print("4. Exit EcoSort")

    def _handle_add_item(self) -> None:
        print("\n--- AVAILABLE ITEMS CATALOG ---")
        for idx, (name, weight, material, _) in enumerate(WASTE_CATALOG, start=1):
            mat_info = f" [{material}]" if material else ""
            print(f"{idx}. {name} ({weight} kg){mat_info}")

        try:
            item_idx = int(input("\nSelect item number (1-15): ")) - 1
        except ValueError:
            print("❌ Error: Please enter a valid number!")
            return

        if not (0 <= item_idx < len(WASTE_CATALOG)):
            print("❌ Error: Invalid item number!")
            return

        waste_item = create_waste_from_catalog_entry(WASTE_CATALOG[item_idx])
        try:
            self._bin.add_waste(waste_item)
        except BinOverflowError as e:
            print(f"❌ Error: {e}")
        else:
            print(f"✅ Added: {waste_item.name} ({waste_item.weight} kg). "
                  f"Free space: {self._bin.free_space:.2f} kg.")

    def _handle_view_status(self) -> None:
        print(f"\n📊 Bin Load: {self._bin.current_weight:.2f} / {self._bin.capacity:.2f} kg.")
        print(f"Total items inside: {self._bin.item_count}")
        print(self._bin.describe_contents())

    def _handle_process_bin(self) -> None:
        print()
        print(RecyclingCenter.process_bin(self._bin))


if __name__ == "__main__":
    EcoSortApp().run()