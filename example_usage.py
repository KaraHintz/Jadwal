"""
Example usage of the Observer Pattern for Schedule Notifications
"""

from observer import ScheduleSubject, StudentObserver, LecturerObserver


def main():
    # Create the subject (publisher)
    schedule_subject = ScheduleSubject()
    
    # Create observers (subscribers)
    student1 = StudentObserver("STU001", "student1@university.ac.id")
    student2 = StudentObserver("STU002", "student2@university.ac.id")
    lecturer1 = LecturerObserver("LEC001", "Dr. Ahmad Subandi", "+62812345678")
    lecturer2 = LecturerObserver("LEC002", "Ibu Siti Nurhaliza")
    
    # Attach observers to the subject
    schedule_subject.attach(student1)
    schedule_subject.attach(student2)
    schedule_subject.attach(lecturer1)
    schedule_subject.attach(lecturer2)
    
    print("=" * 70)
    print("📅 OBSERVER PATTERN - SCHEDULE NOTIFICATION SYSTEM")
    print("=" * 70)
    
    # Scenario 1: Schedule Changed
    print("\n>>> SCENARIO 1: SCHEDULE CHANGED")
    print("-" * 70)
    schedule_changed_data = {
        'course_name': 'Object-Oriented Programming',
        'old_time': 'Tuesday 10:00 - 12:00',
        'new_time': 'Wednesday 14:00 - 16:00',
        'room': 'Lab 301',
        'lecturer_name': 'Dr. Ahmad Subandi'
    }
    schedule_subject.notify('SCHEDULE_CHANGED', schedule_changed_data)
    
    # Scenario 2: Schedule Cancelled
    print("\n>>> SCENARIO 2: SCHEDULE CANCELLED")
    print("-" * 70)
    schedule_cancelled_data = {
        'course_name': 'Web Development',
        'reason': 'Dosen sakit',
        'lecturer_name': 'Ibu Siti Nurhaliza'
    }
    schedule_subject.notify('SCHEDULE_CANCELLED', schedule_cancelled_data)
    
    # Scenario 3: Schedule Postponed
    print("\n>>> SCENARIO 3: SCHEDULE POSTPONED")
    print("-" * 70)
    schedule_postponed_data = {
        'course_name': 'Database Design',
        'new_time': 'Friday 13:00 - 15:00',
        'reason': 'Hari libur nasional'
    }
    schedule_subject.notify('SCHEDULE_POSTPONED', schedule_postponed_data)
    
    # Detach an observer
    print("\n>>> SCENARIO 4: DETACHING OBSERVER")
    print("-" * 70)
    schedule_subject.detach(student2)
    
    # Notify remaining observers
    print("\n>>> SCENARIO 5: SCHEDULE CHANGED (STUDENT2 DETACHED)")
    print("-" * 70)
    schedule_changed_data_2 = {
        'course_name': 'Python Programming',
        'old_time': 'Monday 09:00 - 11:00',
        'new_time': 'Monday 13:00 - 15:00',
        'room': 'Lab 201',
        'lecturer_name': 'Dr. Ahmad Subandi'
    }
    schedule_subject.notify('SCHEDULE_CHANGED', schedule_changed_data_2)
    
    print("\n" + "=" * 70)
    print("✓ Demonstration completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
