from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional
 
 
# --- CUSTOM EXCEPTIONS ---
 
class BinOverflowError(Exception):
    """Raised when adding waste would exceed the bin's weight capacity."""
    pass
