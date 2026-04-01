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

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def is_due(self, now: datetime) -> bool:
        """Check if the task is due at the given time."""
        if self.scheduled_time is None:
            return False
        return now >= self.scheduled_time and not self.completed

    def reschedule(self, new_time: datetime) -> None:
        """Update the scheduled time of the task."""
        self.scheduled_time = new_time

    def update_duration(self, minutes: int) -> None:
        """Set a new duration for the task."""
        self.duration = minutes

    def calculate_urgency(self) -> float:
        """Compute a simple urgency score for the task."""
        return float(self.priority)


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
        """Fetch all pending tasks from the owner."""
        return self.owner.get_pending_tasks()

    def generate_plan(self, target_date: Optional[date] = None) -> Schedule:
        """Generate a schedule plan for the target date."""
        if target_date is None:
            target_date = date.today()
        self.schedule = Schedule(date=target_date)
        tasks = sorted(self.retrieve_all_tasks(), key=lambda t: (-t.priority, t.scheduled_time or datetime.max))
        current_time = datetime.combine(target_date, time(hour=8))
        for task in tasks:
            start = current_time
            end = start + timedelta(minutes=task.duration)
            self.schedule.add_event(ScheduledEvent(task=task, start=start, end=end))
            current_time = end
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

