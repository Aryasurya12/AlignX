import pytest
from anchoralign.alignment.selector import select_strategy
from anchoralign.models.gap import Gap
from anchoralign.config import AnchorAlignConfig

def test_short_matched():
    config = AnchorAlignConfig(band_width=5)
    gap = Gap("g1", 0, 5, 0, 5, 5, 5, 0, 0.0)
    gap.classification = "short_length_matched"
    strategy, reason, params = select_strategy(gap, config)
    assert strategy == "banded_dp"
    assert params["band_width"] == 5
    assert "Short gap" in reason

def test_long_mismatched():
    config = AnchorAlignConfig()
    gap = Gap("g1", 0, 50, 0, 50, 50, 50, 0, 0.0)
    gap.classification = "long_or_length_mismatched"
    strategy, reason, params = select_strategy(gap, config)
    assert strategy == "full_dp"
    assert "Gap is long" in reason
