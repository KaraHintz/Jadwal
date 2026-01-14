# 🌐 Web Application Setup Guide

## 🚀 Quick Start

### 1. Install Flask
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install Flask==2.3.0 Werkzeug==2.3.0
```

### 2. Run the Web Server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 3. Open in Browser
Go to: **http://localhost:5000**

---

## 📊 Features

### 📅 Schedules Management
- ✅ View all schedules
- ✅ Add new schedules
- ✅ Delete schedules
- ✅ Automatic conflict checking on add

### ⚠️ Conflict Detection
- ✅ Real-time conflict detection
- ✅ Room conflict identification
- ✅ Lecturer conflict identification
- ✅ Detailed conflict information

### 📈 Statistics
- ✅ Total schedules count
- ✅ Conflict statistics
- ✅ Affected rooms/lecturers
- ✅ System status indicator

### 📋 Event Logging
- ✅ Log all schedule changes
- ✅ Track conflict events
- ✅ Clear logs
- ✅ Timestamp for all events

---

## 🌐 Web Interface

### Navigation
- **Schedules**: Manage all schedules
- **Conflicts**: View current conflicts
- **Statistics**: View system stats
- **Logs**: View event history

### Add New Schedule
1. Click "Add New Schedule" button
2. Fill in all fields:
   - Schedule ID (unique)
   - Course Name
   - Day (Senin - Jumat)
   - Start Time (HH:MM)
   - End Time (HH:MM)
   - Room (e.g., Lab 301)
   - Lecturer (Name)
3. Click "Add Schedule"

The system will:
- ✅ Check for conflicts
- ✅ Reject if conflicts found
- ✅ Add successfully if no conflicts
- ✅ Log the action
- ✅ Notify observers

---

## 📡 API Endpoints

### Schedules
- **GET /api/schedules** - Get all schedules
- **POST /api/schedules** - Add new schedule
- **DELETE /api/schedules/<id>** - Delete schedule

### Conflicts
- **GET /api/conflicts** - Get current conflicts

### Statistics
- **GET /api/statistics** - Get system statistics

### Logs
- **GET /api/logs** - Get event logs
- **DELETE /api/logs** - Clear logs

---

## 📝 Request/Response Examples

### Add Schedule
```bash
curl -X POST http://localhost:5000/api/schedules \
  -H "Content-Type: application/json" \
  -d '{
    "id": "SCH001",
    "course_name": "OOP dan Agentic AI",
    "hari": "Senin",
    "jam_mulai": "10:00",
    "jam_selesai": "12:00",
    "ruangan": "Lab 301",
    "dosen": "Dr. Ahmad"
  }'
```

### Get Conflicts
```bash
curl http://localhost:5000/api/conflicts
```

Response:
```json
{
  "total_conflicts": 1,
  "room_conflicts": 1,
  "lecturer_conflicts": 0,
  "affected_rooms": ["Lab 301"],
  "affected_lecturers": [],
  "conflicts": [
    {
      "type": "room_conflict",
      "schedules": ["SCH001", "SCH002"],
      "details": {...}
    }
  ]
}
```

---

## 🎨 UI Features

### Dashboard
- Color-coded conflict cards (Red = Room, Blue = Lecturer)
- Real-time statistics updates
- Status indicator
- Event logging

### Responsive Design
- Works on desktop
- Mobile-friendly
- Tablet optimized

### User Experience
- Smooth animations
- Clear feedback messages
- Intuitive navigation
- Error handling

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Use different port
python -c "from app import app; app.run(port=5001)"
```

### Flask Not Installed
```bash
pip install Flask
```

### Browser Won't Connect
1. Check if Flask is running (see console)
2. Try http://127.0.0.1:5000 instead of localhost
3. Check firewall settings

---

## 📂 Project Structure
```
Jadwal/
├── app.py                  (Flask application)
├── requirements.txt        (Python dependencies)
├── templates/
│   └── index.html         (Web interface)
└── static/
    ├── style.css          (Styling)
    └── script.js          (Frontend logic)
```

---

## 🎯 Example Workflow

1. **Open Browser** → http://localhost:5000
2. **Add Schedule 1** → SCH001, Senin, 10:00-12:00, Lab 301, Dr. Ahmad
3. **Add Schedule 2** → SCH002, Senin, 11:00-13:00, Lab 301, Ibu Siti
   - System detects ROOM CONFLICT ⚠️
   - Schedule rejected
4. **Check Conflicts** → Shows 1 room conflict
5. **View Statistics** → Shows conflict details
6. **Check Logs** → Shows all events

---

## 📚 Integration with Backend

The Flask app integrates with:
- ✅ `conflict_detector.py` - Conflict detection
- ✅ `observer.py` - Notification system
- ✅ Both patterns working together

---

## 🚀 Production Deployment

For production use:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📞 Support

For issues or questions:
1. Check browser console (F12)
2. Check server logs
3. Review API responses
4. Check firewall settings

Happy scheduling! 🎉
