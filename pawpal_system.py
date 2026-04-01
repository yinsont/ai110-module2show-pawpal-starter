from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional


@dataclass
class Task:
    id: str
    description: str
    duration: int
    priority: int
    scheduled_time: Optional[datetime] = None
    frequency: Optional[str] = None
    completed: bool = False
    notes: Optional[str] = None
    last_completed: Optional[datetime] = None

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.last_completed = datetime.now()

    def is_due_today(self, today: date) -> bool:
        """Check if the task is due today, considering frequency."""
        if self.frequency is None:
            return self.scheduled_time and self.scheduled_time.date() == today
        if self.frequency == "daily":
            return self.last_completed is None or (datetime.now().date() - self.last_completed.date()).days >= 1
        # For simplicity, assume other frequencies not due daily
        return False

    def reschedule(self, new_time: datetime) -> None:
        """Update the scheduled time of the task."""
        self.scheduled_time = new_time

    def update_duration(self, minutes: int) -> None:
        """Set a new duration for the task."""
        self.duration = minutes

    def calculate_urgency(self) -> float:
        """Compute a simple urgency score for the task."""
        base_urgency = float(self.priority)
        if self.scheduled_time:
            # Increase urgency if scheduled time is approaching
            now = datetime.now()
            hours_until = (self.scheduled_time - now).total_seconds() / 3600
            if hours_until < 24:
                base_urgency += max(0, (24 - hours_until) / 24) * 2  # Boost for near-term tasks
        return base_urgency


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    health_conditions: Dict[str, str] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by id."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def needs_today(self) -> List[Task]:
        """Return tasks that are due today and not completed."""
        now = datetime.now()
        return [task for task in self.tasks if task.is_due(now) and not task.completed]

    def is_urgent(self, task: Task) -> bool:
        """Determine whether a task is urgent."""
        return task.calculate_urgency() > 5.0

    def mark_task_complete(self, task_id: str) -> None:
        """Mark a task complete and create next occurrence if recurring.

        Args:
            task_id (str): The ID of the task to mark complete.

        For daily/weekly tasks, creates a new Task instance for the next
        occurrence with updated scheduled_time and unique ID.
        """
        for task in self.tasks:
            if task.id == task_id:
                task.mark_complete()
                if task.frequency == "daily" and task.scheduled_time:
                    next_time = task.scheduled_time + timedelta(days=1)
                    new_task = Task(
                        id=f"{task.id}_{next_time.strftime('%Y%m%d')}",
                        description=task.description,
                        duration=task.duration,
                        priority=task.priority,
                        scheduled_time=next_time,
                        frequency=task.frequency,
                        completed=False,
                        notes=task.notes
                    )
                    self.add_task(new_task)
                elif task.frequency == "weekly" and task.scheduled_time:
                    next_time = task.scheduled_time + timedelta(weeks=1)
                    new_task = Task(
                        id=f"{task.id}_{next_time.strftime('%Y%m%d')}",
                        description=task.description,
                        duration=task.duration,
                        priority=task.priority,
                        scheduled_time=next_time,
                        frequency=task.frequency,
                        completed=False,
                        notes=task.notes
                    )
                    self.add_task(new_task)
                break


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove an owner pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all pets."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.

        Args:
            completed (Optional[bool]): If True, return only completed tasks;
                if False, only pending; if None, ignore completion status.
            pet_name (Optional[str]): If provided, return only tasks belonging
                to the pet with this name.

        Returns:
            List[Task]: Filtered list of tasks matching the criteria.
        """
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if any(p.name == pet_name for p in self.pets if t in p.tasks)]
        return tasks

    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks for a specific pet."""
        pet = next((p for p in self.pets if p.name == pet_name), None)
        return pet.get_tasks() if pet else []

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [task for task in self.get_all_tasks() if task.completed == completed]


@dataclass
class ScheduledEvent:
    task: Task
    start: datetime
    end: datetime


@dataclass
class Schedule:
    date: date
    events: List[ScheduledEvent] = field(default_factory=list)
    status: str = "draft"

    def add_event(self, event: ScheduledEvent) -> None:
        """Add an event to the schedule."""
        self.events.append(event)

    def remove_event(self, task_id: str) -> None:
        """Remove an event from the schedule by task id."""
        self.events = [event for event in self.events if event.task.id != task_id]

    def display(self) -> str:
        """Return a formatted string with scheduled events."""
        lines = [f"{event.start.strftime('%H:%M')} - {event.end.strftime('%H:%M')}: {event.task.description}" for event in self.events]
        return "\n".join(lines)

    def summary(self) -> Dict[str, int]:
        """Return a summary with total minutes and event count."""
        total = sum((event.end - event.start).seconds for event in self.events) // 60
        return {"total_minutes": total, "event_count": len(self.events)}

    def is_feasible(self) -> bool:
        """Check for overlapping events in the schedule."""
        sorted_events = sorted(self.events, key=lambda e: e.start)
        for i in range(1, len(sorted_events)):
            if sorted_events[i].start < sorted_events[i - 1].end:
                return False
        return True


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: Optional[Schedule] = None

    def retrieve_all_tasks(self) -> List[Task]:
        """Fetch all pending tasks from the owner, including recurring ones due today."""
        tasks = self.owner.get_pending_tasks()
        today = date.today()
        recurring_due = []
        for task in self.owner.get_all_tasks():
            if task.frequency and task.is_due_today(today):
                # Create a copy for today if not already pending
                if task not in tasks:
                    task_copy = Task(
                        id=f"{task.id}_{today.isoformat()}",
                        description=task.description,
                        duration=task.duration,
                        priority=task.priority,
                        scheduled_time=datetime.combine(today, time(hour=8)),  # Default time
                        frequency=None,  # One-time for today
                        completed=False,
                        notes=task.notes
                    )
                    recurring_due.append(task_copy)
        tasks.extend(recurring_due)
        return tasks

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by scheduled_time (earliest first).

        Args:
            tasks (List[Task]): List of tasks to sort.

        Returns:
            List[Task]: Sorted list with earliest scheduled_time first.
                Tasks without scheduled_time sort last.
        """
        return sorted(tasks, key=lambda t: t.scheduled_time or datetime.max)

    def generate_plan(self, target_date: Optional[date] = None) -> Schedule:
        """Generate a schedule plan for the target date."""
        if target_date is None:
            target_date = date.today()
        self.schedule = Schedule(date=target_date)
        tasks = self.retrieve_all_tasks()
        # Sort by scheduled_time (earliest first), then by urgency descending
        tasks.sort(key=lambda t: (t.scheduled_time or datetime.max, -t.calculate_urgency()))
        current_time = datetime.combine(target_date, time(hour=8))
        for task in tasks:
            if task.scheduled_time:
                start = task.scheduled_time
            else:
                start = current_time
            end = start + timedelta(minutes=task.duration)
            event = ScheduledEvent(task=task, start=start, end=end)
            self.schedule.add_event(event)
            if not task.scheduled_time:
                current_time = end
        # Basic conflict detection: check if feasible, raise if not
        if not self.schedule.is_feasible():
            raise ValueError("Schedule has overlapping events")
        return self.schedule

    def apply_constraints(self) -> None:
        """Apply scheduling constraints from owner/pets."""
        pass

    def optimize(self) -> None:
        """Optimize the generated schedule."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable summary of the schedule."""
        if self.schedule is None:
            return "No schedule generated yet"
        summary = self.schedule.summary()
        return f"Scheduled {summary['event_count']} task(s), {summary['total_minutes']} minutes total."

    def handle_conflicts(self) -> None:
        """Raise an error if schedule has conflicts."""
        if self.schedule is None:
            return
        if not self.schedule.is_feasible():
            raise ValueError("Schedule has overlapping events")

    def get_unscheduled_tasks(self) -> List[Task]:
        """Return tasks that were not included in the current schedule."""
        scheduled_ids = {event.task.id for event in self.schedule.events} if self.schedule else set()
        return [task for task in self.retrieve_all_tasks() if task.id not in scheduled_ids]

    def get_pet_for_task(self, task: Task) -> Optional[Pet]:
        """Find the pet that owns the given task.

        Args:
            task (Task): The task to find the owner for.

        Returns:
            Optional[Pet]: The pet that has this task, or None if not found.
        """
        for pet in self.owner.pets:
            if task in pet.tasks:
                return pet
        return None

    def detect_conflicts(self) -> Dict[str, List[str]]:
        """Detect scheduling conflicts: overall overlaps and same-pet overlaps.

        Returns:
            Dict[str, List[str]]: Dictionary with keys 'overall' and 'same_pet',
                each containing lists of conflict messages. Empty if no conflicts.
        """
        if not self.schedule:
            return {}

        conflicts = {}

        # Overall schedule conflicts (any overlapping events)
        if not self.schedule.is_feasible():
            conflicts["overall"] = ["Schedule has overlapping events"]

        # Same-pet conflicts
        events_by_pet = {}
        for event in self.schedule.events:
            pet = self.get_pet_for_task(event.task)
            if pet:
                if pet not in events_by_pet:
                    events_by_pet[pet] = []
                events_by_pet[pet].append(event)

        for pet, events in events_by_pet.items():
            sorted_events = sorted(events, key=lambda e: e.start)
            for i in range(1, len(sorted_events)):
                if sorted_events[i].start < sorted_events[i - 1].end:
                    if "same_pet" not in conflicts:
                        conflicts["same_pet"] = []
                    conflicts["same_pet"].append(f"{pet.name} has overlapping tasks: {sorted_events[i-1].task.description} and {sorted_events[i].task.description}")

        return conflicts

