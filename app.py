"""
Flask Web Application for Schedule Conflict Detection System
"""

from flask import Flask, render_template, request, jsonify
from datetime import time, datetime
from conflict_detector import Schedule, ScheduleConflictDetector, format_conflict_report
from observer import ScheduleSubject, StudentObserver, LecturerObserver
import json

app = Flask(__name__)

# Global state
detector = ScheduleConflictDetector()
subject = ScheduleSubject()
schedules = []
conflicts_log = []

# Setup observers
student_observer = StudentObserver("SYSTEM", "admin@university.ac.id")
lecturer_observer = LecturerObserver("SYSTEM", "Admin")
subject.attach(student_observer)
subject.attach(lecturer_observer)


def time_to_string(t):
    """Convert time object to string"""
    if isinstance(t, str):
        return t
    return f"{t.hour:02d}:{t.minute:02d}"


def string_to_time(s):
    """Convert string to time object"""
    if isinstance(s, time):
        return s
    parts = s.split(':')
    return time(int(parts[0]), int(parts[1]))


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    """Get all schedules"""
    schedules_data = [
        {
            'id': s.id,
            'course_name': s.course_name,
            'hari': s.hari,
            'jam_mulai': time_to_string(s.jam_mulai),
            'jam_selesai': time_to_string(s.jam_selesai),
            'ruangan': s.ruangan,
            'dosen': s.dosen
        }
        for s in schedules
    ]
    return jsonify(schedules_data)


@app.route('/api/schedules', methods=['POST'])
def add_schedule():
    """Add a new schedule"""
    try:
        data = request.json
        
        # Validate input
        if not all(key in data for key in ['id', 'course_name', 'hari', 'jam_mulai', 'jam_selesai', 'ruangan', 'dosen']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create schedule object
        new_schedule = Schedule(
            id=data['id'],
            hari=data['hari'],
            jam_mulai=string_to_time(data['jam_mulai']),
            jam_selesai=string_to_time(data['jam_selesai']),
            ruangan=data['ruangan'],
            dosen=data['dosen'],
            course_name=data['course_name']
        )
        
        # Check for conflicts
        test_schedules = schedules + [new_schedule]
        conflicts = detector.detect_schedule_conflict(test_schedules)
        
        if conflicts:
            conflict_details = [
                {
                    'type': c.conflict_type,
                    'with_schedule': c.affected_schedules[1].id if len(c.affected_schedules) > 1 else 'Unknown',
                    'details': c.details,
                    'suggestions': get_conflict_suggestions({
                        'type': c.conflict_type,
                        'details': c.details
                    })
                }
                for c in conflicts
            ]
            
            # Log conflict
            conflicts_log.append({
                'timestamp': datetime.now().isoformat(),
                'schedule_id': data['id'],
                'status': 'REJECTED',
                'conflicts': conflict_details
            })
            
            subject.notify('SCHEDULE_CONFLICT_DETECTED', {
                'schedule_id': data['id'],
                'conflict_count': len(conflicts)
            })
            
            return jsonify({
                'error': f'Conflict detected: {len(conflicts)} conflicts found',
                'conflicts': conflict_details
            }), 409
        
        # Add schedule
        schedules.append(new_schedule)
        
        # Log success
        conflicts_log.append({
            'timestamp': datetime.now().isoformat(),
            'schedule_id': data['id'],
            'status': 'ADDED',
            'conflicts': []
        })
        
        subject.notify('SCHEDULE_ADDED', {
            'schedule_id': data['id'],
            'course_name': data['course_name']
        })
        
        return jsonify({
            'message': 'Schedule added successfully',
            'schedule': {
                'id': new_schedule.id,
                'course_name': new_schedule.course_name,
                'hari': new_schedule.hari,
                'jam_mulai': time_to_string(new_schedule.jam_mulai),
                'jam_selesai': time_to_string(new_schedule.jam_selesai),
                'ruangan': new_schedule.ruangan,
                'dosen': new_schedule.dosen
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/schedules/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """Delete a schedule"""
    global schedules
    
    old_count = len(schedules)
    schedules = [s for s in schedules if s.id != schedule_id]
    
    if len(schedules) == old_count:
        return jsonify({'error': 'Schedule not found'}), 404
    
    # Log deletion
    conflicts_log.append({
        'timestamp': datetime.now().isoformat(),
        'schedule_id': schedule_id,
        'status': 'DELETED',
        'conflicts': []
    })
    
    subject.notify('SCHEDULE_REMOVED', {'schedule_id': schedule_id})
    
    return jsonify({'message': 'Schedule deleted successfully'})


def get_conflict_suggestions(conflict):
    """Generate resolution suggestions for a conflict"""
    suggestions = []
    
    if conflict['type'] == 'room_conflict':
        room = conflict['details']['room']
        day = conflict['details']['day']
        course1 = conflict['details']['course1']
        course2 = conflict['details']['course2']
        
        suggestions = [
            f"🔄 Reschedule '{course1}' to a different day or time slot",
            f"🔄 Reschedule '{course2}' to a different day or time slot",
            f"🏢 Move one course to a different room (e.g., Lab 302, Lab 303) on {day}",
            f"⏰ Stagger the time slots: adjust start/end times to avoid overlap in {room}",
            f"🎯 Consider holding one course online to free up {room}"
        ]
    
    elif conflict['type'] == 'lecturer_conflict':
        lecturer = conflict['details']['lecturer']
        course1 = conflict['details']['course1']
        course2 = conflict['details']['course2']
        
        suggestions = [
            f"👨‍🏫 Assign a substitute lecturer for '{course1}' or '{course2}'",
            f"🔄 Reschedule '{course1}' to a different day or time",
            f"🔄 Reschedule '{course2}' to a different day or time",
            f"⏰ Adjust timing so {lecturer} can handle both courses (increase break time)",
            f"🎓 Split one course section and assign to another qualified lecturer"
        ]
    
    return suggestions


@app.route('/api/conflicts', methods=['GET'])
def get_conflicts():
    """Get current conflicts"""
    conflicts = detector.detect_schedule_conflict(schedules)
    
    conflict_data = [
        {
            'type': c.conflict_type,
            'schedules': [s.id for s in c.affected_schedules],
            'details': c.details,
            'suggestions': get_conflict_suggestions({
                'type': c.conflict_type,
                'details': c.details
            })
        }
        for c in conflicts
    ]
    
    summary = detector.get_conflict_summary(conflicts)
    
    return jsonify({
        'total_conflicts': summary['total_conflicts'],
        'room_conflicts': summary['room_conflicts'],
        'lecturer_conflicts': summary['lecturer_conflicts'],
        'affected_rooms': summary['affected_rooms'],
        'affected_lecturers': summary['affected_lecturers'],
        'conflicts': conflict_data
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics"""
    conflicts = detector.detect_schedule_conflict(schedules)
    summary = detector.get_conflict_summary(conflicts)
    
    return jsonify({
        'total_schedules': len(schedules),
        'total_conflicts': summary['total_conflicts'],
        'room_conflicts': summary['room_conflicts'],
        'lecturer_conflicts': summary['lecturer_conflicts'],
        'affected_rooms': summary['affected_rooms'],
        'affected_lecturers': summary['affected_lecturers'],
        'system_status': 'OK' if summary['total_conflicts'] == 0 else 'CONFLICTS_DETECTED'
    })


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get conflict logs"""
    return jsonify(conflicts_log)


@app.route('/api/logs', methods=['DELETE'])
def clear_logs():
    """Clear conflict logs"""
    global conflicts_log
    conflicts_log = []
    return jsonify({'message': 'Logs cleared'})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
