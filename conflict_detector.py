"""
Schedule Conflict Detection with Interval Tree Optimization
"""

from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from datetime import time
from collections import defaultdict


@dataclass
class Schedule:
    """Represents a schedule entry"""
    id: str
    hari: str  # Day (Senin, Selasa, etc.)
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    dosen: str
    course_name: str = None
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id


@dataclass
class Conflict:
    """Represents a detected conflict"""
    conflict_type: str  # 'room_conflict', 'lecturer_conflict'
    affected_schedules: List[Schedule]
    details: Dict[str, Any]
    
    def __repr__(self):
        schedule_ids = [s.id for s in self.affected_schedules]
        return (f"Conflict(type={self.conflict_type}, "
                f"schedules={schedule_ids}, details={self.details})")


class TimeInterval:
    """Represents a time interval for efficient overlap checking"""
    
    def __init__(self, start: time, end: time):
        self.start = self._time_to_minutes(start)
        self.end = self._time_to_minutes(end)
    
    @staticmethod
    def _time_to_minutes(t: time) -> int:
        """Convert time object to minutes since midnight"""
        return t.hour * 60 + t.minute
    
    def overlaps_with(self, other: 'TimeInterval') -> bool:
        """Check if this interval overlaps with another"""
        return self.start < other.end and other.start < self.end
    
    def __repr__(self):
        return f"TimeInterval({self._minutes_to_time(self.start)} - {self._minutes_to_time(self.end)})"
    
    @staticmethod
    def _minutes_to_time(minutes: int) -> str:
        """Convert minutes to time string format"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"


class IntervalTree:
    """
    Interval Tree for efficient time overlap queries
    Used to optimize schedule conflict detection
    """
    
    def __init__(self):
        self.intervals: List[Tuple[TimeInterval, Schedule]] = []
    
    def insert(self, interval: TimeInterval, schedule: Schedule):
        """Insert an interval and its associated schedule"""
        self.intervals.append((interval, schedule))
    
    def find_overlapping(self, interval: TimeInterval) -> List[Schedule]:
        """
        Find all schedules with intervals that overlap with the given interval
        Time Complexity: O(n) where n is number of intervals
        (Could be optimized to O(log n + k) with balanced tree, k = results)
        """
        overlapping_schedules = []
        for stored_interval, schedule in self.intervals:
            if interval.overlaps_with(stored_interval):
                overlapping_schedules.append(schedule)
        return overlapping_schedules
    
    def __len__(self):
        return len(self.intervals)


class ScheduleConflictDetector:
    """
    Detects schedule conflicts using interval tree optimization
    """
    
    def __init__(self):
        self.conflicts: List[Conflict] = []
        self.processed_pairs = set()
    
    def detect_schedule_conflict(self, schedules: List[Schedule]) -> List[Conflict]:
        """
        Detect all conflicts in a list of schedules
        
        Args:
            schedules: List of Schedule objects
            
        Returns:
            List of Conflict objects with details
        """
        self.conflicts = []
        self.processed_pairs = set()
        
        # Group schedules by day for efficient processing
        schedules_by_day = defaultdict(list)
        for schedule in schedules:
            schedules_by_day[schedule.hari].append(schedule)
        
        # Check conflicts for each day
        for day, day_schedules in schedules_by_day.items():
            self._check_conflicts_for_day(day, day_schedules)
        
        return self.conflicts
    
    def _check_conflicts_for_day(self, day: str, schedules: List[Schedule]):
        """
        Check conflicts for schedules on the same day
        
        Args:
            day: Day name
            schedules: List of schedules for that day
        """
        # Build interval tree for efficient overlap checking
        interval_tree = IntervalTree()
        for schedule in schedules:
            interval = TimeInterval(schedule.jam_mulai, schedule.jam_selesai)
            interval_tree.insert(interval, schedule)
        
        # Check each schedule against others for conflicts
        for i, schedule in enumerate(schedules):
            interval = TimeInterval(schedule.jam_mulai, schedule.jam_selesai)
            overlapping = interval_tree.find_overlapping(interval)
            
            # Filter out self and already processed pairs
            for other_schedule in overlapping:
                if schedule.id == other_schedule.id:
                    continue
                
                # Create pair key (sorted to avoid duplicates)
                pair_key = tuple(sorted([schedule.id, other_schedule.id]))
                if pair_key in self.processed_pairs:
                    continue
                
                self.processed_pairs.add(pair_key)
                
                # Check conflict types
                self._check_conflict_types(schedule, other_schedule, day)
    
    def _check_conflict_types(self, schedule1: Schedule, schedule2: Schedule, day: str):
        """
        Check specific types of conflicts between two schedules
        
        Args:
            schedule1: First schedule
            schedule2: Second schedule
            day: Day name
        """
        # 1. Room Conflict: same room, same day, overlapping time
        if schedule1.ruangan == schedule2.ruangan:
            conflict = Conflict(
                conflict_type='room_conflict',
                affected_schedules=[schedule1, schedule2],
                details={
                    'day': day,
                    'room': schedule1.ruangan,
                    'schedule1_time': f"{schedule1.jam_mulai} - {schedule1.jam_selesai}",
                    'schedule2_time': f"{schedule2.jam_mulai} - {schedule2.jam_selesai}",
                    'course1': schedule1.course_name or 'Unknown',
                    'course2': schedule2.course_name or 'Unknown',
                }
            )
            self.conflicts.append(conflict)
        
        # 2. Lecturer Conflict: same lecturer, same day, overlapping time
        if schedule1.dosen == schedule2.dosen:
            conflict = Conflict(
                conflict_type='lecturer_conflict',
                affected_schedules=[schedule1, schedule2],
                details={
                    'day': day,
                    'lecturer': schedule1.dosen,
                    'schedule1_time': f"{schedule1.jam_mulai} - {schedule1.jam_selesai}",
                    'schedule2_time': f"{schedule2.jam_mulai} - {schedule2.jam_selesai}",
                    'room1': schedule1.ruangan,
                    'room2': schedule2.ruangan,
                    'course1': schedule1.course_name or 'Unknown',
                    'course2': schedule2.course_name or 'Unknown',
                }
            )
            self.conflicts.append(conflict)
    
    def get_conflict_summary(self, conflicts: List[Conflict]) -> Dict[str, Any]:
        """
        Get a summary of conflicts
        
        Args:
            conflicts: List of conflicts
            
        Returns:
            Summary dictionary
        """
        room_conflicts = [c for c in conflicts if c.conflict_type == 'room_conflict']
        lecturer_conflicts = [c for c in conflicts if c.conflict_type == 'lecturer_conflict']
        
        return {
            'total_conflicts': len(conflicts),
            'room_conflicts': len(room_conflicts),
            'lecturer_conflicts': len(lecturer_conflicts),
            'affected_rooms': list(set(c.details['room'] for c in room_conflicts)),
            'affected_lecturers': list(set(c.details['lecturer'] for c in lecturer_conflicts)),
        }


def format_conflict_report(conflicts: List[Conflict]) -> str:
    """
    Format conflicts into a readable report
    
    Args:
        conflicts: List of conflicts
        
    Returns:
        Formatted report string
    """
    if not conflicts:
        return "✓ No conflicts detected!"
    
    report = f"\n{'=' * 80}\n"
    report += f"CONFLICT DETECTION REPORT - {len(conflicts)} conflict(s) found\n"
    report += f"{'=' * 80}\n\n"
    
    # Group by type
    room_conflicts = [c for c in conflicts if c.conflict_type == 'room_conflict']
    lecturer_conflicts = [c for c in conflicts if c.conflict_type == 'lecturer_conflict']
    
    if room_conflicts:
        report += f"ROOM CONFLICTS ({len(room_conflicts)}):\n"
        report += "-" * 80 + "\n"
        for idx, conflict in enumerate(room_conflicts, 1):
            d = conflict.details
            report += f"{idx}. {d['day']} - Room {d['room']}\n"
            report += f"   Schedule 1: {d['course1']} ({d['schedule1_time']})\n"
            report += f"   Schedule 2: {d['course2']} ({d['schedule2_time']})\n"
            report += f"   IDs: {conflict.affected_schedules[0].id} ↔ {conflict.affected_schedules[1].id}\n\n"
    
    if lecturer_conflicts:
        report += f"LECTURER CONFLICTS ({len(lecturer_conflicts)}):\n"
        report += "-" * 80 + "\n"
        for idx, conflict in enumerate(lecturer_conflicts, 1):
            d = conflict.details
            report += f"{idx}. {d['day']} - Lecturer {d['lecturer']}\n"
            report += f"   Schedule 1: {d['course1']} in {d['room1']} ({d['schedule1_time']})\n"
            report += f"   Schedule 2: {d['course2']} in {d['room2']} ({d['schedule2_time']})\n"
            report += f"   IDs: {conflict.affected_schedules[0].id} ↔ {conflict.affected_schedules[1].id}\n\n"
    
    detector = ScheduleConflictDetector()
    detector.conflicts = conflicts
    summary = detector.get_conflict_summary(conflicts)
    
    report += f"SUMMARY:\n"
    report += "-" * 80 + "\n"
    report += f"Total Conflicts: {summary['total_conflicts']}\n"
    report += f"Room Conflicts: {summary['room_conflicts']}\n"
    report += f"Lecturer Conflicts: {summary['lecturer_conflicts']}\n"
    report += f"Affected Rooms: {', '.join(summary['affected_rooms']) or 'None'}\n"
    report += f"Affected Lecturers: {', '.join(summary['affected_lecturers']) or 'None'}\n"
    report += f"{'=' * 80}\n"
    
    return report
