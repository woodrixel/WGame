import WGame

def test_removeall():
    wg = WGame.WGame()
    wg.add(WGame.WObject())
    wg.removeall()
    assert wg.wobjs == []