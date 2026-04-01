from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Alex")

    # Create pets
    dog = Pet(name="Milo", species="Dog", age=4)
    cat = Pet(name="Luna", species="Cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks to pets (out of order)
    cat.add_task(Task(id="t3", description="Play session", duration=20, priority=4, scheduled_time=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0), frequency="daily"))
    dog.add_task(Task(id="t2", description="Give meds", duration=10, priority=10, scheduled_time=datetime.now().replace(hour=12, minute=0, second=0, microsecond=0), frequency="daily"))
    dog.add_task(Task(id="t1", description="Morning walk", duration=30, priority=5, scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0), frequency="daily"))
    dog.add_task(Task(id="t4", description="Brush teeth", duration=15, priority=3, scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0), frequency="daily"))  # Same time as walk

    # Initialize scheduler
    scheduler = Scheduler(owner=owner)

    # Demonstrate sorting and filtering
    all_tasks = scheduler.retrieve_all_tasks()
    print("All pending tasks (unsorted):")
    for task in all_tasks:
        print(f"  {task.description} at {task.scheduled_time.strftime('%H:%M') if task.scheduled_time else 'N/A'}")

    sorted_tasks = scheduler.sort_by_time(all_tasks)
    print("\nTasks sorted by time:")
    for task in sorted_tasks:
        print(f"  {task.description} at {task.scheduled_time.strftime('%H:%M') if task.scheduled_time else 'N/A'}")

    dog_tasks = owner.filter_tasks(pet_name="Milo")
    print("\nTasks for Milo:")
    for task in dog_tasks:
        print(f"  {task.description}")

    pending_tasks = owner.filter_tasks(completed=False)
    print(f"\nTotal pending tasks: {len(pending_tasks)}")

    # Generate plan
    schedule = scheduler.generate_plan()

    # Check for conflicts
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("\n⚠️  Scheduling Conflicts Detected:")
        for conflict_type, messages in conflicts.items():
            print(f"  {conflict_type.upper()}:")
            for msg in messages:
                print(f"    - {msg}")
    else:
        print("\n✅ No conflicts detected")

    print("\nToday's Schedule")
    print("-----------------")
    print(schedule.display())
    print("-----------------")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
