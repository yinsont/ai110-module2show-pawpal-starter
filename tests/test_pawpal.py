from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler


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


def test_sort_no_scheduled_time():
    scheduler = Scheduler(Owner("Test"))
    task_with_time = Task(id="t1", description="Timed", duration=10, priority=1, scheduled_time=datetime(2026, 4, 1, 8, 0))
    task_no_time = Task(id="t2", description="No time", duration=10, priority=1)
    sorted_tasks = scheduler.sort_by_time([task_no_time, task_with_time])
    assert sorted_tasks[0] == task_with_time
    assert sorted_tasks[1] == task_no_time


def test_sort_chronological():
    scheduler = Scheduler(Owner("Test"))
    task1 = Task(id="t1", description="Early", duration=10, priority=1, scheduled_time=datetime(2026, 4, 1, 8, 0))
    task2 = Task(id="t2", description="Mid", duration=10, priority=1, scheduled_time=datetime(2026, 4, 1, 12, 0))
    task3 = Task(id="t3", description="Late", duration=10, priority=1, scheduled_time=datetime(2026, 4, 1, 15, 0))
    sorted_tasks = scheduler.sort_by_time([task3, task1, task2])
    assert sorted_tasks == [task1, task2, task3]


def test_recurring_daily():
    pet = Pet(name="Milo", species="Dog", age=4)
    time = datetime(2026, 4, 1, 8, 0)
    task = Task(id="walk", description="Morning walk", duration=30, priority=5, scheduled_time=time, frequency="daily")
    pet.add_task(task)
    assert len(pet.tasks) == 1

    pet.mark_task_complete("walk")
    assert task.completed is True
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert "20260402" in next_task.id
    assert next_task.scheduled_time.day == 2


def test_recurring_no_frequency():
    pet = Pet(name="Luna", species="Cat", age=2)
    task = Task(id="play", description="Play", duration=20, priority=4)
    pet.add_task(task)
    pet.mark_task_complete("play")
    assert task.completed is True
    assert len(pet.tasks) == 1  # No new task


def test_conflict_same_pet():
    owner = Owner("Alex")
    pet = Pet(name="Milo", species="Dog", age=4)
    owner.add_pet(pet)
    time = datetime(2026, 4, 1, 8, 0)
    task1 = Task(id="t1", description="Walk", duration=30, priority=5, scheduled_time=time)
    task2 = Task(id="t2", description="Brush", duration=15, priority=3, scheduled_time=time)
    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_plan()
    conflicts = scheduler.detect_conflicts()
    assert "same_pet" in conflicts
    assert len(conflicts["same_pet"]) > 0
    assert "Milo" in conflicts["same_pet"][0] and "overlapping" in conflicts["same_pet"][0]


def test_conflict_different_pet():
    owner = Owner("Alex")
    pet1 = Pet(name="Milo", species="Dog", age=4)
    pet2 = Pet(name="Luna", species="Cat", age=2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    time = datetime(2026, 4, 1, 8, 0)
    task1 = Task(id="t1", description="Walk", duration=30, priority=5, scheduled_time=time)
    task2 = Task(id="t2", description="Play", duration=20, priority=4, scheduled_time=time)
    pet1.add_task(task1)
    pet2.add_task(task2)

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_plan()
    conflicts = scheduler.detect_conflicts()
    assert conflicts == {}  # No conflicts for different pets


def test_filter_no_matches():
    owner = Owner("Alex")
    pet = Pet(name="Milo", species="Dog", age=4)
    owner.add_pet(pet)
    task = Task(id="t1", description="Walk", duration=30, priority=5)
    pet.add_task(task)

    filtered = owner.filter_tasks(pet_name="Nonexistent")
    assert len(filtered) == 0

    filtered = owner.filter_tasks(completed=True)
    assert len(filtered) == 0


def test_empty_schedule():
    owner = Owner("Alex")
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_plan()
    conflicts = scheduler.detect_conflicts()
    assert conflicts == {}
