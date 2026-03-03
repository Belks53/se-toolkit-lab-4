"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_returns_empty_list_when_no_matches():
    """Test that filter returns empty list when no interactions match the item_id"""
    from app.routers.interactions import _filter_by_item_id
    from app.models.interaction import InteractionLog
    
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=2, kind="attempt"),
        InteractionLog(id=2, learner_id=2, item_id=3, kind="attempt"),
    ]
    
    result = _filter_by_item_id(interactions, item_id=1)
    
    assert len(result) == 0
    assert result == []


def test_filter_handles_empty_input_list():
    """Test that filter handles empty input list gracefully"""
    from app.routers.interactions import _filter_by_item_id
    
    interactions = []
    
    result = _filter_by_item_id(interactions, item_id=1)
    
    assert len(result) == 0
    assert result == []


def test_filter_returns_all_when_item_id_is_none():
    """Test that filter returns all interactions when item_id is None"""
    from app.routers.interactions import _filter_by_item_id
    from app.models.interaction import InteractionLog
    
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=1, kind="attempt"),
        InteractionLog(id=2, learner_id=2, item_id=2, kind="attempt"),
    ]
    
    result = _filter_by_item_id(interactions, item_id=None)
    
    assert len(result) == 2
    assert result == interactions


def test_filter_preserves_interaction_order():
    """Test that filter preserves the original order of interactions"""
    from app.routers.interactions import _filter_by_item_id
    from app.models.interaction import InteractionLog
    
    interactions = [
        InteractionLog(id=3, learner_id=1, item_id=1, kind="attempt"),
        InteractionLog(id=1, learner_id=2, item_id=2, kind="attempt"),
        InteractionLog(id=4, learner_id=3, item_id=1, kind="attempt"),
        InteractionLog(id=2, learner_id=4, item_id=3, kind="attempt"),
    ]
    
    result = _filter_by_item_id(interactions, item_id=1)
    
    assert len(result) == 2
    assert result[0].id == 3  # Первый подходящий
    assert result[1].id == 4  # Второй подходящий


def test_filter_works_with_different_item_types():
    """Test that filter works correctly with different item_id types"""
    from app.routers.interactions import _filter_by_item_id
    from app.models.interaction import InteractionLog
    
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=1, kind="attempt"),
        InteractionLog(id=2, learner_id=2, item_id=999, kind="attempt"),
        InteractionLog(id=3, learner_id=3, item_id=1000, kind="attempt"),
    ]
    
    result = _filter_by_item_id(interactions, item_id=999)
    
    assert len(result) == 1
    assert result[0].id == 2