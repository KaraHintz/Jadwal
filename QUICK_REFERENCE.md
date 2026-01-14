# 🚀 Quick Reference Guide - Schedule Conflict Detection

## 📦 Modul Utama

### Import
```python
from conflict_detector import (
    Schedule, 
    ScheduleConflictDetector, 
    TimeInterval,
    format_conflict_report
)
```

## 1️⃣ Basic Usage (30 detik)

```python
from datetime import time
from conflict_detector import Schedule, ScheduleConflictDetector

# Buat schedule
schedule1 = Schedule(
    id="S1",
    hari="Senin",
    jam_mulai=time(10, 0),
    jam_selesai=time(12, 0),
    ruangan="Lab 301",
    dosen="Dr. Ahmad",
    course_name="OOP"
)

# Detect conflicts
detector = ScheduleConflictDetector()
conflicts = detector.detect_schedule_conflict([schedule1, schedule2])

# Check results
print(f"Conflicts found: {len(conflicts)}")
```

## 2️⃣ Complete Example

```python
from datetime import time
from conflict_detector import (
    Schedule, 
    ScheduleConflictDetector,
    format_conflict_report
)

# 1. Create schedules
schedules = [
    Schedule("S1", "Senin", time(10,0), time(12,0), "Lab301", "Dr.A", "OOP"),
    Schedule("S2", "Senin", time(11,0), time(13,0), "Lab301", "Dr.B", "Web"),
]

# 2. Detect conflicts
detector = ScheduleConflictDetector()
conflicts = detector.detect_schedule_conflict(schedules)

# 3. Print formatted report
print(format_conflict_report(conflicts))

# 4. Get summary
summary = detector.get_conflict_summary(conflicts)
print(f"Room conflicts: {summary['room_conflicts']}")
print(f"Lecturer conflicts: {summary['lecturer_conflicts']}")
```

## 3️⃣ Schedule Data Model

```python
@dataclass
class Schedule:
    id: str                    # Unique ID (required)
    hari: str                  # Day: Senin, Selasa, etc (required)
    jam_mulai: time           # Start time (required)
    jam_selesai: time         # End time (required)
    ruangan: str              # Room number (required)
    dosen: str                # Lecturer name (required)
    course_name: str = None   # Course name (optional)
```

### Example Data
```python
Schedule(
    id="SCH001",                    # Unique identifier
    hari="Senin",                   # Monday
    jam_mulai=time(10, 0),          # 10:00 AM
    jam_selesai=time(12, 0),        # 12:00 PM
    ruangan="Lab 301",              # Room number
    dosen="Dr. Ahmad Subandi",      # Lecturer
    course_name="OOP dan AI"        # Course (optional)
)
```

## 4️⃣ Conflict Types

| Type | Kondisi | Contoh |
|------|---------|--------|
| `room_conflict` | Hari sama + Waktu overlap + Ruangan sama | Lab301: 10-12 & 11-13 |
| `lecturer_conflict` | Hari sama + Waktu overlap + Dosen sama | Dr.A: 10-12 & 11-13 |

## 5️⃣ Conflict Object

```python
@dataclass
class Conflict:
    conflict_type: str           # 'room_conflict' atau 'lecturer_conflict'
    affected_schedules: List     # [schedule1, schedule2]
    details: Dict              # Detail informasi conflict
```

### Details Structure
```python
# Room Conflict Details
{
    'day': 'Senin',
    'room': 'Lab 301',
    'schedule1_time': '10:00 - 12:00',
    'schedule2_time': '11:00 - 13:00',
    'course1': 'OOP',
    'course2': 'Web Dev'
}

# Lecturer Conflict Details
{
    'day': 'Senin',
    'lecturer': 'Dr. Ahmad',
    'schedule1_time': '10:00 - 12:00',
    'schedule2_time': '11:00 - 13:00',
    'room1': 'Lab 301',
    'room2': 'Lab 302',
    'course1': 'OOP',
    'course2': 'Database'
}
```

## 6️⃣ API Reference

### ScheduleConflictDetector

#### `detect_schedule_conflict(schedules: List[Schedule]) -> List[Conflict]`
**Deteksi semua konflik dalam list jadwal**
```python
detector = ScheduleConflictDetector()
conflicts = detector.detect_schedule_conflict(schedules)
```
- **Input**: List of Schedule objects
- **Output**: List of Conflict objects
- **Time**: O(n²) worst case
- **Space**: O(n)

#### `get_conflict_summary(conflicts: List[Conflict]) -> Dict`
**Dapatkan ringkasan konflik**
```python
summary = detector.get_conflict_summary(conflicts)
# {
#     'total_conflicts': 2,
#     'room_conflicts': 1,
#     'lecturer_conflicts': 1,
#     'affected_rooms': ['Lab 301'],
#     'affected_lecturers': ['Dr. Ahmad']
# }
```

### TimeInterval

#### `overlaps_with(other: TimeInterval) -> bool`
**Cek overlap antara dua interval waktu**
```python
interval1 = TimeInterval(time(10,0), time(12,0))
interval2 = TimeInterval(time(11,0), time(13,0))
print(interval1.overlaps_with(interval2))  # True
```

### Utility Function

#### `format_conflict_report(conflicts: List[Conflict]) -> str`
**Format conflicts menjadi laporan yang readable**
```python
report = format_conflict_report(conflicts)
print(report)
```

**Output Example**:
```
================================================================================
CONFLICT DETECTION REPORT - 2 conflict(s) found
================================================================================

ROOM CONFLICTS (1):
1. Senin - Room Lab 301
   Schedule 1: OOP (10:00 - 12:00)
   Schedule 2: Web Dev (11:00 - 13:00)
   IDs: SCH001 ↔ SCH002

LECTURER CONFLICTS (1):
1. Selasa - Lecturer Dr. Ahmad
   Schedule 1: Python (13:00 - 15:00)
   Schedule 2: Database (14:00 - 16:00)
   IDs: SCH003 ↔ SCH004
```

## 7️⃣ Time Overlap Logic

### How Overlap Check Works

```
Schedule 1: 10:00 - 12:00
Schedule 2: 11:00 - 13:00
           ^^^^
         Overlap

Schedule 1: 10:00 - 12:00
Schedule 2: 12:00 - 14:00
           (No overlap - exactly touching)

Schedule 1: 10:00 - 12:00
Schedule 2: 13:00 - 15:00
           (No overlap - gap between)
```

**Formula**: `start1 < end2 AND start2 < end1`

```python
# Example
overlap = interval1.start < interval2.end and interval2.start < interval1.end
```

## 8️⃣ Integration with Observer Pattern

```python
from observer import ScheduleSubject, StudentObserver, LecturerObserver
from conflict_detector import Schedule, ScheduleConflictDetector

# Setup
subject = ScheduleSubject()
subject.attach(StudentObserver("S1", "email@uni.ac.id"))
subject.attach(LecturerObserver("L1", "Dr. Ahmad"))

# Detect and notify
detector = ScheduleConflictDetector()
conflicts = detector.detect_schedule_conflict(schedules)

if conflicts:
    subject.notify('SCHEDULE_CONFLICT_DETECTED', {
        'conflict_count': len(conflicts),
        'conflicts': conflicts
    })
else:
    subject.notify('SCHEDULE_UPDATED', {
        'status': 'success'
    })
```

## 9️⃣ Common Patterns

### Pattern 1: Check Schedule Before Adding

```python
def can_add_schedule(existing_schedules, new_schedule):
    detector = ScheduleConflictDetector()
    test_list = existing_schedules + [new_schedule]
    conflicts = detector.detect_schedule_conflict(test_list)
    return len(conflicts) == 0
```

### Pattern 2: Get Conflicting Schedules

```python
def get_conflicting_ids(conflicts):
    return [
        (c.affected_schedules[0].id, c.affected_schedules[1].id)
        for c in conflicts
    ]
```

### Pattern 3: Group by Conflict Type

```python
def group_by_type(conflicts):
    by_type = {'room_conflict': [], 'lecturer_conflict': []}
    for c in conflicts:
        by_type[c.conflict_type].append(c)
    return by_type
```

## 🔟 Performance Tips

| Action | Complexity | Tips |
|--------|-----------|------|
| Detect conflicts | O(n²) | Cache results if unchanged |
| Find overlapping | O(n) | Use interval tree for large n |
| Check single overlap | O(1) | Fast time comparison |

## 1️⃣1️⃣ Testing

**Run all tests**:
```bash
python test_conflict_detection.py
```

**Test coverage**:
- ✓ Room conflict detection
- ✓ Lecturer conflict detection
- ✓ No conflict scenarios
- ✓ Multiple conflicts
- ✓ Different days
- ✓ Edge cases (touching times)
- ✓ Large datasets

## 1️⃣2️⃣ Edge Cases

```python
# Case 1: Touching times (no conflict)
Schedule("S1", "Senin", time(10,0), time(12,0), "Lab301", "Dr.A")
Schedule("S2", "Senin", time(12,0), time(14,0), "Lab301", "Dr.B")
# Result: No conflict ✓

# Case 2: Same lecturer, different days (no conflict)
Schedule("S1", "Senin", time(10,0), time(12,0), "Lab301", "Dr.A")
Schedule("S2", "Selasa", time(10,0), time(12,0), "Lab302", "Dr.A")
# Result: No conflict ✓

# Case 3: Complete overlap (conflict)
Schedule("S1", "Senin", time(10,0), time(12,0), "Lab301", "Dr.A")
Schedule("S2", "Senin", time(10,0), time(12,0), "Lab301", "Dr.B")
# Result: Room conflict ✓
```

## 📂 Files

```
├── conflict_detector.py           # Core implementation
├── test_conflict_detection.py     # Test suite
├── integration_example.py         # Integration demo
└── CONFLICT_DETECTION_GUIDE.md    # Full documentation
```

## 🎯 Next Steps

1. ✓ Understand the basic usage
2. ✓ Review conflict types
3. ✓ Run tests to verify
4. ✓ Integrate with your schedule system
5. ✓ Add custom notifications

---

**Questions?** Check the full documentation in `CONFLICT_DETECTION_GUIDE.md`
