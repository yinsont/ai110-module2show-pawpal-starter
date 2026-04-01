from datetime import datetime

from pawpal_system import Pet, Task


def test_task_mark_complete():
    task = Task(id="t1", description="Test task", duration=15, priority=3, scheduled_time=datetime.now())
    assert task.completed is False

    task.mark_complete()
    assert task.completed is True


def test_pet_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog", age=5)
    assert len(pet.tasks) == 0

    task = Task(id="t2", description="Feed", duration=10, priority=2, scheduled_time=datetime.now())
    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task
