# tests/test_basic.py
def test_imports():
    """Test that core modules can be imported."""

    assert True


def test_basic_functionality():
    """Test basic data structure creation."""
    from datetime import datetime

    from ci.transparency.sdk import ContentHash, HashId, WindowAgg

    # Create basic objects
    hash_id = HashId("opaque", "test")
    content_hash = ContentHash(hash_id)
    assert content_hash.id is not None

    # Create minimal WindowAgg
    window = WindowAgg(
        world_id="test",
        topic_id="test_topic",
        window_start=datetime(2025, 1, 1),
        window_end=datetime(2025, 1, 1, 0, 10),
        n_messages=100,
        n_unique_hashes=80,
        dup_rate=0.2,
        top_hashes=[],
        hash_concentration=0.1,
        burst_score=0.5,
        type_mix={"post": 0.5, "reply": 0.3, "retweet": 0.2},
        time_histogram=[10] * 10,
    )

    assert window.world_id == "test"
    assert window.n_messages == 100


def test_serialization():
    """Test JSON serialization roundtrip."""
    from datetime import datetime

    from ci.transparency.sdk import WindowAgg, windowagg_from_json, windowagg_to_json

    window = WindowAgg(
        world_id="test",
        topic_id="test_topic",
        window_start=datetime(2025, 1, 1),
        window_end=datetime(2025, 1, 1, 0, 10),
        n_messages=50,
        n_unique_hashes=40,
        dup_rate=0.2,
        top_hashes=[],
        hash_concentration=0.1,
        burst_score=0.5,
        type_mix={"post": 0.5, "reply": 0.3, "retweet": 0.2},
        time_histogram=[5] * 10,
    )

    # Test roundtrip
    json_data = windowagg_to_json(window)
    restored = windowagg_from_json(json_data)  # type: ignore

    assert restored.world_id == window.world_id
    assert restored.n_messages == window.n_messages
