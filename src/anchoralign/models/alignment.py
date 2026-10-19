from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AlignmentResult:
    aligned_reference: str
    aligned_query: str
    score: float
    strategy: str
    band_width: int
    boundary_touched: bool
    decision_metadata: Optional[Dict[str, Any]] = None
    cells_evaluated: int = 0
