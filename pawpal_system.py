from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional


@dataclass
class User:
    name: str
    availability: List[tuple[time, time]] = field(default_factory=list)
    preferences: Dict[str, str] = field(default_factory=dict)
    constraints: Dict[str, int] = field(default_factory=dict)

    def is_available(self, timeslot: tuple[time, time]) -> bool:
        pass

    def update_availability(self, availability: List[tuple[time, time]]) -> None:
        pass

    def set_preferences(self, preferences: Dict[str, str]) -> None:
        pass

    def get_time_budget(self) -> int:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    health_conditions: Dict[str, str] = field(default_factory=dict)
    activity_needs: Dict[str, int] = field(default_factory=dict)
    behavior_profile: Optional[str] = None

    def needs_today(self) -> List[str]:
        pass

    def update_health_status(self, status: Dict[str, str]) -> None:
        pass

    def is_urgent(self, task_type: str) -> bool:
        pass


@dataclass
class Task:
    id: str
    type: str
    duration: int
    priority: int
    deadline: Optional[datetime] = None
    earliest: Optional[datetime] = None
    latest: Optional[datetime] = None
    repeat: Optional[str] = None
    notes: Optional[str] = None

    def is_due(self, now: datetime) -> bool:
        pass

    def reschedule(self, new_start: datetime) -> None:
        pass

    def update_duration(self, minutes: int) -> None:
        pass

    def calculate_urgency(self) -> float:
        pass


@dataclass
class ScheduledEvent:
    task: Task
    start: datetime
    end: datetime


@dataclass
class Schedule:
    date: date
    events: List[ScheduledEvent] = field(default_factory=list)
    total_duration: int = 0
    status: str = "draft"

    def add_event(self, event: ScheduledEvent) -> None:
        pass

    def remove_event(self, task_id: str) -> None:
        pass

    def display(self) -> str:
        pass

    def summary(self) -> Dict[str, int]:
        pass

    def is_feasible(self) -> bool:
        pass


class Scheduler:
    def __init__(self, user: User, pet: Pet, tasks: List[Task]):
        self.user = user
        self.pet = pet
        self.tasks = tasks
        self.schedule: Optional[Schedule] = None

    def generate_plan(self) -> Schedule:
        pass

    def apply_constraints(self) -> None:
        pass

    def optimize(self) -> None:
        pass

    def explain_plan(self) -> str:
        pass

    def handle_conflicts(self) -> None:
        pass

    def get_unscheduled_tasks(self) -> List[Task]:
        pass
