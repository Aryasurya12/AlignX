from dataclasses import dataclass
from typing import Optional

@dataclass
class Gap:
    id: str
    reference_start: int
    reference_end: int
    query_start: int
    query_end: int
    reference_length: int
    query_length: int
    length_difference: int
    mismatch_ratio: float
    classification: Optional[str] = None
    selected_strategy: Optional[str] = None
