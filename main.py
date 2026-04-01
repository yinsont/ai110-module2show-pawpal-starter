from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Alex")

    # Create pets
    dog = Pet(name="Milo", species="Dog", age=4)
    cat = Pet(name="Luna", species="Cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks to pets
    dog.add_task(Task(id="t1", description="Morning walk", duration=30, priority=5, scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0), frequency="daily"))
    dog.add_task(Task(id="t2", description="Give meds", duration=10, priority=10, scheduled_time=datetime.now().replace(hour=12, minute=0, second=0, microsecond=0), frequency="daily"))
    cat.add_task(Task(id="t3", description="Play session", duration=20, priority=4, scheduled_time=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0), frequency="daily"))

    # Initialize scheduler and generate plan
    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_plan()

    print("Today's Schedule")
    print("-----------------")
    print(schedule.display())
    print("-----------------")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
