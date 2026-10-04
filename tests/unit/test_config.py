from anchoralign.config import AnchorAlignConfig

def test_default_config():
    c = AnchorAlignConfig()
    assert c.L_min == 10

def test_custom_config():
    c = AnchorAlignConfig(L_min=5)
    assert c.L_min == 5
