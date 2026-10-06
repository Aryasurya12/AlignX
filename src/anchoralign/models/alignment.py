from dataclasses import dataclass

@dataclass
class AlignmentResult:
    aligned_reference: str
    aligned_query: str
    score: float
    strategy: str
    band_width: int
    boundary_touched: bool
    decision_metadata: dict = None
