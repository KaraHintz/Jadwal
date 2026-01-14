// JavaScript for Schedule Conflict Detection System

// Show/Hide sections
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Add active to nav link
    event.target.classList.add('active');
    
    // Refresh data
    if (sectionId === 'schedules') {
        loadSchedules();
    } else if (sectionId === 'conflicts') {
        refreshConflicts();
    } else if (sectionId === 'statistics') {
        loadStatistics();
    } else if (sectionId === 'logs') {
        loadLogs();
    }
}

// Show/Hide add schedule form
function showAddScheduleForm() {
    document.getElementById('addScheduleForm').classList.remove('hidden');
}

function hideAddScheduleForm() {
    document.getElementById('addScheduleForm').classList.add('hidden');
    document.getElementById('scheduleForm').reset();
}

// Add schedule
async function addSchedule(event) {
    event.preventDefault();
    
    const scheduleData = {
        id: document.getElementById('scheduleId').value,
        course_name: document.getElementById('courseName').value,
        hari: document.getElementById('hari').value,
        jam_mulai: document.getElementById('jamMulai').value,
        jam_selesai: document.getElementById('jamSelesai').value,
        ruangan: document.getElementById('ruangan').value,
        dosen: document.getElementById('dosen').value
    };
    
    try {
        const response = await fetch('/api/schedules', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(scheduleData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✓ Schedule added successfully!');
            hideAddScheduleForm();
            loadSchedules();
            loadStatistics();
        } else {
            if (data.conflicts) {
                let conflictMessage = 'Conflicts detected:\n\n';
                data.conflicts.forEach(conflict => {
                    conflictMessage += `Type: ${conflict.type}\n`;
                    conflictMessage += `With: ${conflict.with_schedule}\n\n`;
                });
                alert(conflictMessage);
            } else {
                alert('Error: ' + data.error);
            }
        }
    } catch (error) {
        alert('Error adding schedule: ' + error.message);
    }
}

// Load schedules
async function loadSchedules() {
    try {
        const response = await fetch('/api/schedules');
        const schedules = await response.json();
        
        const tbody = document.getElementById('schedulesBody');
        
        if (schedules.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center">No schedules yet</td></tr>';
            return;
        }
        
        tbody.innerHTML = schedules.map(schedule => `
            <tr>
                <td><strong>${schedule.id}</strong></td>
                <td>${schedule.course_name}</td>
                <td>${schedule.hari}</td>
                <td>${schedule.jam_mulai} - ${schedule.jam_selesai}</td>
                <td>${schedule.ruangan}</td>
                <td>${schedule.dosen}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteSchedule('${schedule.id}')">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading schedules:', error);
    }
}

// Delete schedule
async function deleteSchedule(scheduleId) {
    if (!confirm(`Are you sure you want to delete schedule ${scheduleId}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/schedules/${scheduleId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('✓ Schedule deleted successfully!');
            loadSchedules();
            loadStatistics();
        } else {
            alert('Error deleting schedule');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Refresh conflicts
async function refreshConflicts() {
    try {
        const response = await fetch('/api/conflicts');
        const data = await response.json();
        
        const container = document.getElementById('conflictsContainer');
        
        if (data.total_conflicts === 0) {
            container.innerHTML = '<div class="message-box">✓ No conflicts detected!</div>';
            return;
        }
        
        let html = '<div class="conflict-list">';
        
        // Room conflicts
        data.conflicts
            .filter(c => c.type === 'room_conflict')
            .forEach((conflict, index) => {
                html += `
                    <div class="conflict-card room">
                        <div class="conflict-title">⚠️ Room Conflict #${index + 1}</div>
                        <div class="conflict-detail">
                            <strong>Room:</strong> ${conflict.details.room}<br>
                            <strong>Day:</strong> ${conflict.details.day}<br>
                            <strong>Schedule 1:</strong> ${conflict.details.course1} (${conflict.details.schedule1_time})<br>
                            <strong>Schedule 2:</strong> ${conflict.details.course2} (${conflict.details.schedule2_time})<br>
                            <strong>Affected Schedules:</strong> ${conflict.schedules.join(', ')}
                        </div>
                    </div>
                `;
            });
        
        // Lecturer conflicts
        data.conflicts
            .filter(c => c.type === 'lecturer_conflict')
            .forEach((conflict, index) => {
                html += `
                    <div class="conflict-card lecturer">
                        <div class="conflict-title">⚠️ Lecturer Conflict #${index + 1}</div>
                        <div class="conflict-detail">
                            <strong>Lecturer:</strong> ${conflict.details.lecturer}<br>
                            <strong>Day:</strong> ${conflict.details.day}<br>
                            <strong>Schedule 1:</strong> ${conflict.details.course1} in ${conflict.details.room1} (${conflict.details.schedule1_time})<br>
                            <strong>Schedule 2:</strong> ${conflict.details.course2} in ${conflict.details.room2} (${conflict.details.schedule2_time})<br>
                            <strong>Affected Schedules:</strong> ${conflict.schedules.join(', ')}
                        </div>
                    </div>
                `;
            });
        
        html += '</div>';
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading conflicts:', error);
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const stats = await response.json();
        
        document.getElementById('totalSchedules').textContent = stats.total_schedules;
        document.getElementById('totalConflicts').textContent = stats.total_conflicts;
        document.getElementById('roomConflicts').textContent = stats.room_conflicts;
        document.getElementById('lecturerConflicts').textContent = stats.lecturer_conflicts;
        
        document.getElementById('affectedRooms').textContent = 
            stats.affected_rooms.length > 0 ? stats.affected_rooms.join(', ') : 'None';
        document.getElementById('affectedLecturers').textContent = 
            stats.affected_lecturers.length > 0 ? stats.affected_lecturers.join(', ') : 'None';
        
        const statusElement = document.getElementById('systemStatus');
        if (stats.system_status === 'OK') {
            statusElement.textContent = '✓ OK - No conflicts';
            statusElement.className = 'detail-content status-ok';
        } else {
            statusElement.textContent = '✗ CONFLICTS DETECTED';
            statusElement.className = 'detail-content status-error';
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load logs
async function loadLogs() {
    try {
        const response = await fetch('/api/logs');
        const logs = await response.json();
        
        const tbody = document.getElementById('logsBody');
        
        if (logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No logs yet</td></tr>';
            return;
        }
        
        tbody.innerHTML = logs.map(log => {
            const date = new Date(log.timestamp);
            const timeString = date.toLocaleString();
            const conflictInfo = log.conflicts.length > 0 
                ? `${log.conflicts.length} conflict(s)`
                : 'None';
            
            return `
                <tr>
                    <td>${timeString}</td>
                    <td><strong>${log.schedule_id}</strong></td>
                    <td>
                        <span style="color: ${log.status === 'ADDED' ? '#28a745' : log.status === 'REJECTED' ? '#dc3545' : '#6c757d'}">
                            ${log.status}
                        </span>
                    </td>
                    <td>${conflictInfo}</td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

// Clear logs
async function clearLogs() {
    if (!confirm('Are you sure you want to clear all logs?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/logs', {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('✓ Logs cleared!');
            loadLogs();
        } else {
            alert('Error clearing logs');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSchedules();
    loadStatistics();
    
    // Set default nav link as active
    const firstNavLink = document.querySelector('.nav-link');
    if (firstNavLink) {
        firstNavLink.classList.add('active');
    }
    
    // Auto-refresh statistics every 10 seconds
    setInterval(loadStatistics, 10000);
});
