from dataclasses import dataclass
from typing import Optional

@dataclass
class Mutation:
    type: str  # substitution, insertion, deletion
    reference_position: int
    query_position: int
    reference_sequence: str
    query_sequence: str
    alignment_position: Optional[int] = None
