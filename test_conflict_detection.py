"""
Test cases and examples for Schedule Conflict Detection
"""

from datetime import time
from conflict_detector import Schedule, ScheduleConflictDetector, format_conflict_report


def test_room_conflict():
    """Test case 1: Two schedules in same room with overlapping time"""
    print("\n" + "="*80)
    print("TEST 1: ROOM CONFLICT DETECTION")
    print("="*80)
    
    detector = ScheduleConflictDetector()
    
    schedules = [
        Schedule(
            id="SCH001",
            hari="Senin",
            jam_mulai=time(10, 0),
            jam_selesai=time(12, 0),
            ruangan="Lab 301",
            dosen="Dr. Ahmad",
            course_name="OOP dan Agentic AI"
        ),
        Schedule(
            id="SCH002",
            hari="Senin",
            jam_mulai=time(11, 0),  # Overlaps with SCH001
            jam_selesai=time(13, 0),
            ruangan="Lab 301",  # Same room
            dosen="Ibu Siti",
            course_name="Web Development"
        ),
    ]
    
    conflicts = detector.detect_schedule_conflict(schedules)
    print(format_conflict_report(conflicts))
    
    assert len(conflicts) == 1, f"Expected 1 conflict, got {len(conflicts)}"
    assert conflicts[0].conflict_type == 'room_conflict'
    print("✓ Test 1 passed!")


def test_lecturer_conflict():
    """Test case 2: Two schedules with same lecturer with overlapping time"""
    print("\n" + "="*80)
    print("TEST 2: LECTURER CONFLICT DETECTION")
    print("="*80)
    
    detector = ScheduleConflictDetector()
    
    schedules = [
        Schedule(
            id="SCH003",
            hari="Selasa",
            jam_mulai=time(13, 0),
            jam_selesai=time(15, 0),
            ruangan="Lab 201",
            dosen="Dr. Ahmad",
            course_name="Python Programming"
        ),
        Schedule(
            id="SCH004",
            hari="Selasa",
            jam_mulai=time(14, 0),  # Overlaps with SCH003
            jam_selesai=time(16, 0),
            ruangan="Lab 202",  # Different room
            dosen="Dr. Ahmad",  # Same lecturer
            course_name="Database Design"
        ),
    ]
    
    conflicts = detector.detect_schedule_conflict(schedules)
    print(format_conflict_report(conflicts))
    
    assert len(conflicts) == 1, f"Expected 1 conflict, got {len(conflicts)}"
    assert conflicts[0].conflict_type == 'lecturer_conflict'
    print("✓ Test 2 passed!")


def test_no_conflict():
    """Test case 3: Schedules with no conflicts"""
    print("\n" + "="*80)
    print("TEST 3: NO CONFLICT DETECTION")
    print("="*80)
    
    detector = ScheduleConflictDetector()
    
    schedules = [
        Schedule(
            id="SCH005",
            hari="Rabu",
            jam_mulai=time(10, 0),
            jam_selesai=time(12, 0),
            ruangan="Lab 301",
            dosen="Dr. Ahmad",
            course_name="OOP"
        ),
        Schedule(
            id="SCH006",
            hari="Rabu",
            jam_mulai=time(13, 0),  # No overlap (starts after first ends)
            jam_selesai=time(15, 0),
            ruangan="Lab 301",
            dosen="Ibu Siti",
            course_name="Web Dev"
        ),
    ]
    
    conflicts = detector.detect_schedule_conflict(schedules)
    print(format_conflict_report(conflicts))
    
    assert len(conflicts) == 0, f"Expected 0 conflicts, got {len(conflicts)}"
    print("✓ Test 3 passed!")


def test_multiple_conflicts():
    """Test case 4: Multiple conflicts in complex schedule"""
    print("\n" + "="*80)
    print("TEST 4: MULTIPLE CONFLICTS DETECTION")
    print("="*80)
    
    detector = ScheduleConflictDetector()
    
    schedules = [
        Schedule(
            id="SCH007",
            hari="Kamis",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="Lab 301",
            dosen="Dr. Ahmad",
            course_name="OOP"
        ),
        Schedule(
            id="SCH008",
            hari="Kamis",
            jam_mulai=time(9, 0),  # Room conflict with SCH007
            jam_selesai=time(11, 0),
            ruangan="Lab 301",
            dosen="Ibu Siti",
            course_name="Web Dev"
        ),
        Schedule(
            id="SCH009",
            hari="Kamis",
            jam_mulai=time(9, 30),  # Lecturer conflict with SCH007
            jam_selesai=time(11, 30),
            ruangan="Lab 202",
            dosen="Dr. Ahmad",
            course_name="Database"
        ),
        Schedule(
            id="SCH010",
            hari="Kamis",
            jam_mulai=time(14, 0),  # No conflicts
            jam_selesai=time(16, 0),
            ruangan="Lab 401",
            dosen="Prof. Budi",
            course_name="AI"
        ),
    ]
    
    conflicts = detector.detect_schedule_conflict(schedules)
    print(format_conflict_report(conflicts))
    
    # SCH007 conflicts with SCH008 (room) and SCH009 (lecturer) = 2 conflicts
    # SCH008 and SCH009 don't conflict (different lecturers and rooms)
    assert len(conflicts) == 2, f"Expected 2 conflicts, got {len(conflicts)}"
    print("✓ Test 4 passed!")


def test_different_days_no_conflict():
    """Test case 5: Same room/lecturer on different days - no conflict"""
    print("\n" + "="*80)
    print("TEST 5: DIFFERENT DAYS - NO CONFLICT")
    print("="*80)
    
    detector = ScheduleConflictDetector()
    
    schedules = [
        Schedule(
            id="SCH011",
            hari="Senin",
            jam_mulai=time(10, 0),
            jam_selesai=time(12, 0),
            ruangan="Lab 301",
            dosen="Dr. Ahmad",
            course_name="OOP"
        ),
        Schedule(
            id="SCH012",
            hari="Selasa",  # Different day
            jam_mulai=time(10, 0),
            jam_selesai=time(12, 0),
            ruangan="Lab 301",  # Same room
            dosen="Dr. Ahmad",  # Same lecturer
            course_name="Python"
        ),
    ]
    
    conflicts = detector.detect_schedule_conflict(schedules)
    print(format_conflict_report(conflicts))
    
    assert len(conflicts) == 0, f"Expected 0 conflicts, got {len(conflicts)}"
    print("✓ Test 5 passed!")


def test_edge_case_touching_times():
    """Test case 6: Schedules with touching times (no overlap)"""
    print("\n" + "="*80)
    print("TEST 6: TOUCHING TIMES - NO OVERLAP")
    print("="*80)
    
    detector = ScheduleConflictDetector()
    
    schedules = [
        Schedule(
            id="SCH013",
            hari="Jumat",
            jam_mulai=time(10, 0),
            jam_selesai=time(12, 0),
            ruangan="Lab 301",
            dosen="Dr. Ahmad",
            course_name="OOP"
        ),
        Schedule(
            id="SCH014",
            hari="Jumat",
            jam_mulai=time(12, 0),  # Exactly when first ends
            jam_selesai=time(14, 0),
            ruangan="Lab 301",
            dosen="Ibu Siti",
            course_name="Web Dev"
        ),
    ]
    
    conflicts = detector.detect_schedule_conflict(schedules)
    print(format_conflict_report(conflicts))
    
    # Should have no conflicts since times don't overlap
    assert len(conflicts) == 0, f"Expected 0 conflicts, got {len(conflicts)}"
    print("✓ Test 6 passed!")


def test_large_schedule():
    """Test case 7: Large schedule set (performance test)"""
    print("\n" + "="*80)
    print("TEST 7: LARGE SCHEDULE SET (Performance Test)")
    print("="*80)
    
    detector = ScheduleConflictDetector()
    
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    rooms = ["Lab 301", "Lab 302", "Lab 303"]
    lecturers = ["Dr. Ahmad", "Ibu Siti", "Prof. Budi"]
    courses = ["OOP", "Web Dev", "Database", "Python", "AI"]
    
    schedules = []
    schedule_id = 1
    
    # Create 30 schedules
    for day in days:
        for hour in range(8, 18, 2):
            room = rooms[(schedule_id - 1) % len(rooms)]
            lecturer = lecturers[(schedule_id - 1) % len(lecturers)]
            course = courses[(schedule_id - 1) % len(courses)]
            
            schedules.append(Schedule(
                id=f"SCH{schedule_id:03d}",
                hari=day,
                jam_mulai=time(hour, 0),
                jam_selesai=time(hour + 2, 0),
                ruangan=room,
                dosen=lecturer,
                course_name=course
            ))
            schedule_id += 1
    
    conflicts = detector.detect_schedule_conflict(schedules)
    print(format_conflict_report(conflicts))
    
    print(f"✓ Test 7 passed! Processed {len(schedules)} schedules")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█  SCHEDULE CONFLICT DETECTION - TEST SUITE".ljust(79) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    try:
        test_room_conflict()
        test_lecturer_conflict()
        test_no_conflict()
        test_multiple_conflicts()
        test_different_days_no_conflict()
        test_edge_case_touching_times()
        test_large_schedule()
        
        print("\n" + "█" * 80)
        print("█" + " " * 78 + "█")
        print("█  ✓ ALL TESTS PASSED!".ljust(79) + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        raise


if __name__ == "__main__":
    run_all_tests()
