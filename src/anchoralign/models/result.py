from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .anchor import Anchor
from .gap import Gap
from .alignment import AlignmentResult
from .mutation import Mutation
from ..config import AnchorAlignConfig

@dataclass
class FinalResult:
    reference_length: int
    query_length: int
    anchors: List[Anchor] = field(default_factory=list)
    gaps: List[Gap] = field(default_factory=list)
    alignments: List[AlignmentResult] = field(default_factory=list)
    mutations: List[Mutation] = field(default_factory=list)
    compound_events: List[Any] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    timings: Dict[str, float] = field(default_factory=dict)
    configuration: Optional[AnchorAlignConfig] = None
    final_alignment: Optional[AlignmentResult] = None
