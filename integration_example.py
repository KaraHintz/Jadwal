"""
Integration example: Combining Observer Pattern with Conflict Detection
"""

from datetime import time
from observer import ScheduleSubject, StudentObserver, LecturerObserver
from conflict_detector import Schedule, ScheduleConflictDetector, format_conflict_report


class ScheduleManager:
    """
    Manages schedules with integrated conflict detection and notifications
    """
    
    def __init__(self):
        self.schedules = []
        self.detector = ScheduleConflictDetector()
        self.subject = ScheduleSubject()
    
    def register_observer(self, observer):
        """Register an observer to be notified of schedule changes"""
        self.subject.attach(observer)
    
    def add_schedule(self, schedule: Schedule) -> bool:
        """
        Add a new schedule and check for conflicts
        
        Args:
            schedule: Schedule object to add
            
        Returns:
            True if added successfully, False if conflicts found
        """
        # Try adding the schedule
        test_schedules = self.schedules + [schedule]
        
        # Detect conflicts
        conflicts = self.detector.detect_schedule_conflict(test_schedules)
        
        if conflicts:
            # Notify about conflicts detected
            print(format_conflict_report(conflicts))
            self.subject.notify('SCHEDULE_CONFLICT_DETECTED', {
                'schedule_id': schedule.id,
                'conflict_count': len(conflicts),
                'conflicts': [
                    {
                        'type': c.conflict_type,
                        'with_schedule': c.affected_schedules[1].id,
                        'details': c.details
                    }
                    for c in conflicts
                ]
            })
            return False
        
        # Add schedule and notify observers
        self.schedules.append(schedule)
        print(f"\n✓ Schedule {schedule.id} added successfully!")
        
        self.subject.notify('SCHEDULE_ADDED', {
            'schedule_id': schedule.id,
            'course_name': schedule.course_name,
            'day': schedule.hari,
            'time': f"{schedule.jam_mulai} - {schedule.jam_selesai}",
            'room': schedule.ruangan,
            'lecturer': schedule.dosen
        })
        
        return True
    
    def update_schedule(self, schedule_id: str, updated_schedule: Schedule) -> bool:
        """
        Update an existing schedule and check for conflicts
        
        Args:
            schedule_id: ID of schedule to update
            updated_schedule: Updated schedule object
            
        Returns:
            True if updated successfully, False if conflicts found
        """
        # Find and remove old schedule
        old_schedule = None
        remaining_schedules = []
        
        for sch in self.schedules:
            if sch.id == schedule_id:
                old_schedule = sch
            else:
                remaining_schedules.append(sch)
        
        if old_schedule is None:
            print(f"✗ Schedule {schedule_id} not found!")
            return False
        
        # Check conflicts with new schedule
        test_schedules = remaining_schedules + [updated_schedule]
        conflicts = self.detector.detect_schedule_conflict(test_schedules)
        
        if conflicts:
            print(format_conflict_report(conflicts))
            self.subject.notify('SCHEDULE_UPDATE_FAILED', {
                'schedule_id': schedule_id,
                'reason': 'Conflicts detected',
                'conflict_count': len(conflicts)
            })
            return False
        
        # Update schedule
        self.schedules = test_schedules
        print(f"\n✓ Schedule {schedule_id} updated successfully!")
        
        self.subject.notify('SCHEDULE_CHANGED', {
            'schedule_id': schedule_id,
            'course_name': updated_schedule.course_name,
            'old_day': old_schedule.hari,
            'new_day': updated_schedule.hari,
            'old_time': f"{old_schedule.jam_mulai} - {old_schedule.jam_selesai}",
            'new_time': f"{updated_schedule.jam_mulai} - {updated_schedule.jam_selesai}",
            'old_room': old_schedule.ruangan,
            'new_room': updated_schedule.ruangan,
            'lecturer': updated_schedule.dosen
        })
        
        return True
    
    def remove_schedule(self, schedule_id: str) -> bool:
        """Remove a schedule"""
        old_length = len(self.schedules)
        self.schedules = [s for s in self.schedules if s.id != schedule_id]
        
        if len(self.schedules) == old_length:
            print(f"✗ Schedule {schedule_id} not found!")
            return False
        
        print(f"\n✓ Schedule {schedule_id} removed successfully!")
        self.subject.notify('SCHEDULE_REMOVED', {
            'schedule_id': schedule_id
        })
        
        return True
    
    def get_schedule_status(self) -> dict:
        """Get current schedule status and conflicts"""
        conflicts = self.detector.detect_schedule_conflict(self.schedules)
        summary = self.detector.get_conflict_summary(conflicts)
        
        return {
            'total_schedules': len(self.schedules),
            'conflicts': conflicts,
            'summary': summary
        }
    
    def print_schedule_report(self):
        """Print detailed schedule report"""
        status = self.get_schedule_status()
        
        print("\n" + "=" * 80)
        print("SCHEDULE REPORT")
        print("=" * 80)
        
        print(f"\nTotal Schedules: {status['total_schedules']}")
        
        if status['total_schedules'] > 0:
            print("\nSchedules:")
            print("-" * 80)
            for sch in self.schedules:
                print(f"  {sch.id}: {sch.course_name}")
                print(f"    - {sch.hari}, {sch.jam_mulai} - {sch.jam_selesai}")
                print(f"    - Room: {sch.ruangan}, Lecturer: {sch.dosen}")
        
        if status['conflicts']:
            print(format_conflict_report(status['conflicts']))
        else:
            print("\n✓ No conflicts detected!")


def main():
    """Demonstrate the integrated schedule manager"""
    
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█  SCHEDULE MANAGER - OBSERVER + CONFLICT DETECTION INTEGRATION".ljust(79) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    # Create manager
    manager = ScheduleManager()
    
    # Register observers
    student = StudentObserver("STU001", "student@university.ac.id")
    lecturer = LecturerObserver("LEC001", "Dr. Ahmad", "+62812345678")
    
    manager.register_observer(student)
    manager.register_observer(lecturer)
    
    # Scenario 1: Add valid schedules
    print("\n" + "="*80)
    print("SCENARIO 1: Adding valid schedules (no conflicts)")
    print("="*80)
    
    schedule1 = Schedule(
        id="SCH001",
        hari="Senin",
        jam_mulai=time(10, 0),
        jam_selesai=time(12, 0),
        ruangan="Lab 301",
        dosen="Dr. Ahmad",
        course_name="OOP dan Agentic AI"
    )
    manager.add_schedule(schedule1)
    
    schedule2 = Schedule(
        id="SCH002",
        hari="Selasa",
        jam_mulai=time(13, 0),
        jam_selesai=time(15, 0),
        ruangan="Lab 302",
        dosen="Ibu Siti",
        course_name="Web Development"
    )
    manager.add_schedule(schedule2)
    
    manager.print_schedule_report()
    
    # Scenario 2: Try to add conflicting schedule (same room, overlapping time)
    print("\n" + "="*80)
    print("SCENARIO 2: Attempt to add schedule with ROOM CONFLICT")
    print("="*80)
    
    conflict_schedule = Schedule(
        id="SCH003",
        hari="Senin",
        jam_mulai=time(11, 0),
        jam_selesai=time(13, 0),
        ruangan="Lab 301",  # Same room as SCH001
        dosen="Prof. Budi",
        course_name="Database Design"
    )
    manager.add_schedule(conflict_schedule)
    
    manager.print_schedule_report()
    
    # Scenario 3: Update schedule with conflict
    print("\n" + "="*80)
    print("SCENARIO 3: Update schedule causing LECTURER CONFLICT")
    print("="*80)
    
    # Try to change SCH002 to same time as SCH001 with same lecturer
    updated_schedule = Schedule(
        id="SCH002",
        hari="Senin",
        jam_mulai=time(11, 0),
        jam_selesai=time(13, 0),
        ruangan="Lab 302",
        dosen="Dr. Ahmad",  # Same lecturer as SCH001
        course_name="Web Development"
    )
    manager.update_schedule("SCH002", updated_schedule)
    
    manager.print_schedule_report()
    
    # Scenario 4: Add a valid schedule for the same lecturer on different day
    print("\n" + "="*80)
    print("SCENARIO 4: Add schedule with same lecturer on different day (valid)")
    print("="*80)
    
    schedule3 = Schedule(
        id="SCH003",
        hari="Rabu",  # Different day
        jam_mulai=time(10, 0),
        jam_selesai=time(12, 0),
        ruangan="Lab 303",
        dosen="Dr. Ahmad",
        course_name="Python Programming"
    )
    manager.add_schedule(schedule3)
    
    manager.print_schedule_report()
    
    # Scenario 5: Remove a schedule
    print("\n" + "="*80)
    print("SCENARIO 5: Remove a schedule")
    print("="*80)
    
    manager.remove_schedule("SCH001")
    manager.print_schedule_report()
    
    # Final Summary
    print("\n" + "█" * 80)
    print("█  DEMONSTRATION COMPLETED".ljust(79) + "█")
    print("█" * 80 + "\n")


if __name__ == "__main__":
    main()
