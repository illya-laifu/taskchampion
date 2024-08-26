from taskchampion import Replica, Status, WorkingSet
from pathlib import Path
import pytest
import uuid

import ipdb


@pytest.fixture
def working_set(tmp_path: Path):
    ipdb.set_trace()
    r = Replica(str(tmp_path), True)
    ops = []
    result = r.create_task(str(uuid.uuid4()))
    assert result is not None
    task, op = result
    ops.append(op)

    result = r.create_task(str(uuid.uuid4()))
    assert result is not None
    task, op = result
    ops.append(op)
    r.commit_operations(ops)

    return r.working_set()


def test_len(working_set: WorkingSet):
    assert len(working_set) == 2


def test_largest_index(working_set: WorkingSet):
    assert working_set.largest_index() == 2


def test_is_empty(working_set: WorkingSet):
    assert not working_set.is_empty()


def test_by_index(working_set: WorkingSet):
    assert working_set.by_index(1) is not None


@pytest.mark.skip()
def test_iter(working_set: WorkingSet):
    assert iter(working_set)


@pytest.mark.skip()
def test_next(working_set: WorkingSet):
    assert next(working_set)[0] == 1
    assert next(working_set)[0] == 2
    with pytest.raises(OSError):
        next(working_set)
