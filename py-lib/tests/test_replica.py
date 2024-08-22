import uuid
from pathlib import Path

import pytest
from taskchampion import Replica

# TODO: instantiate the in-memory replica, this will do for now


@pytest.fixture
def empty_replica(tmp_path: Path) -> Replica:
    return Replica(str(tmp_path), True)


@pytest.fixture
def replica_with_tasks(empty_replica: Replica):
    ops = []
    res = empty_replica.create_task(str(uuid.uuid4()))
    assert res is not None
    _, op = res
    ops.append(op)

    res = empty_replica.create_task(str(uuid.uuid4()))
    assert res is not None
    _, op = res
    ops.append(op)

    res = empty_replica.create_task(str(uuid.uuid4()))
    assert res is not None
    _, op = res
    ops.append(op)

    empty_replica.commit_operations(ops)

    return empty_replica


def test_constructor(tmp_path: Path):
    r = Replica(str(tmp_path), True)

    assert r is not None


def test_constructor_throws_error_with_missing_database(tmp_path: Path):
    with pytest.raises(RuntimeError):
        Replica(str(tmp_path), False)


def test_create_task(empty_replica: Replica):
    u = uuid.uuid4()
    result = empty_replica.create_task(str(u))
    assert result is not None

    _, op = result

    empty_replica.commit_operations([op])

    tasks = empty_replica.all_task_uuids()

    assert len(tasks) == 1


def test_all_task_uuids(empty_replica: Replica):
    ops = []
    result = empty_replica.create_task(str(uuid.uuid4()))
    assert result is not None
    _, op = result
    ops.append(op)

    result = empty_replica.create_task(str(uuid.uuid4()))
    assert result is not None
    _, op = result
    ops.append(op)

    result = empty_replica.create_task(str(uuid.uuid4()))
    assert result is not None
    _, op = result
    ops.append(op)

    empty_replica.commit_operations(ops)
    tasks = empty_replica.all_task_uuids()
    assert len(tasks) == 3


def test_all_tasks(empty_replica: Replica):
    ops = []
    result = empty_replica.create_task(str(uuid.uuid4()))
    assert result is not None
    _, op = result
    ops.append(op)

    result = empty_replica.create_task(str(uuid.uuid4()))
    assert result is not None
    _, op = result
    ops.append(op)

    result = empty_replica.create_task(str(uuid.uuid4()))
    assert result is not None
    _, op = result
    ops.append(op)

    empty_replica.commit_operations(ops)

    tasks = empty_replica.all_tasks()

    assert len(tasks) == 3
    keys = tasks.keys()

    for key in keys:
        assert tasks[key] != 0


def test_working_set(replica_with_tasks: Replica):
    ws = replica_with_tasks.working_set()

    assert ws is not None


# TODO: create testable and inspectable WorkingSet


def test_get_task(replica_with_tasks: Replica):
    uuid = replica_with_tasks.all_task_uuids()[0]

    task = replica_with_tasks.get_task(uuid)

    assert task is not None


@pytest.mark.skip()
def test_rebuild_working_set(replica_with_tasks: Replica):
    # TODO actually test this
    replica_with_tasks.rebuild_working_set(False)


@pytest.mark.skip()
def test_add_undo_point(replica_with_tasks: Replica):
    replica_with_tasks.add_undo_point(False)


def test_num_local_operations(replica_with_tasks: Replica):
    assert replica_with_tasks.num_local_operations() == 3

    result = replica_with_tasks.create_task(str(uuid.uuid4()))
    assert result is not None

    _, op = result

    replica_with_tasks.commit_operations([op])

    assert replica_with_tasks.num_local_operations() == 4


def test_num_undo_points(replica_with_tasks: Replica):
    assert replica_with_tasks.num_undo_points() == 3

    result = replica_with_tasks.create_task(str(uuid.uuid4()))

    assert result is not None
    _, op = result
    replica_with_tasks.commit_operations([op])

    assert replica_with_tasks.num_undo_points() == 4


@pytest.mark.skip("Skipping as gotta actually polish it")
def test_dependency_map(replica_with_tasks: Replica):
    assert replica_with_tasks.dependency_map(False) is not None
