from dataclasses import dataclass
from typing import Optional

@dataclass
class Anchor:
    """
    Represents an exact match region between Reference and Query.
    Coordinates follow zero-based, half-open indexing: [start, end).
    """
    reference_start: int
    reference_end: int
    query_start: int
    query_end: int
    length: int
    source_algorithm: str
    metadata: Optional[dict] = None
