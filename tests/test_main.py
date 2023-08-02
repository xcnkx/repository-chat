from app.main import qa


def test_qa():
    assert qa("sazabi pacingバッチについて教えてください") == 'hoge'
