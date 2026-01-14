# Observer Pattern - Schedule Notification System

## 📋 Deskripsi

Implementasi **Observer Pattern** untuk sistem notifikasi perubahan jadwal akademik. Pola ini memungkinkan multiple observers (mahasiswa dan dosen) untuk menerima notifikasi otomatis ketika ada perubahan jadwal.

## 🏗️ Struktur Arsitektur

```
┌──────────────────────┐
│  ScheduleSubject     │ (Publisher)
│  ┌────────────────┐  │
│  │  - observers   │  │
│  │  + attach()    │  │
│  │  + detach()    │  │
│  │  + notify()    │  │
│  └────────────────┘  │
└──────────────────────┘
         │ notifies
    ┌────┴────┐
    │          │
┌─────────────┐  ┌───────────────┐
│  Observer   │  │   Observer    │
│ (Abstract)  │  │  (Abstract)   │
│+ update()   │  │  + update()   │
└─────────────┘  └───────────────┘
    │                    │
    ├────────┬───────────┤
    │        │           │
┌─────────────────┐  ┌──────────────────┐
│ StudentObserver │  │ LecturerObserver │
│ - student_id    │  │ - lecturer_id    │
│ - email         │  │ - name           │
│ + update()      │  │ - phone          │
└─────────────────┘  │ + update()       │
                     └──────────────────┘
```

## 🔑 Komponen Utama

### 1. **Observer (Abstract Base Class)**
Mendefinisikan interface untuk semua observers.

```python
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, schedule_data: Dict[str, Any]) -> None:
        pass
```

### 2. **ScheduleSubject (Publisher)**
Mengelola observers dan mengirimkan notifikasi.

```python
class ScheduleSubject:
    def attach(self, observer: Observer) -> None
    def detach(self, observer: Observer) -> None
    def notify(self, event_type: str, schedule_data: Dict[str, Any]) -> None
```

### 3. **StudentObserver (Concrete Observer)**
Menangani notifikasi untuk mahasiswa (email).

```python
class StudentObserver(Observer):
    def __init__(self, student_id: str, email: str)
    def update(self, event_type: str, schedule_data: Dict[str, Any]) -> None
```

### 4. **LecturerObserver (Concrete Observer)**
Menangani notifikasi untuk dosen (SMS/alert).

```python
class LecturerObserver(Observer):
    def __init__(self, lecturer_id: str, name: str, phone: str = None)
    def update(self, event_type: str, schedule_data: Dict[str, Any]) -> None
```

## 📝 Event Types yang Didukung

| Event Type | Deskripsi | Notifikasi |
|---|---|---|
| `SCHEDULE_CHANGED` | Jadwal berubah waktu/ruang | Email ke student, SMS ke dosen |
| `SCHEDULE_CANCELLED` | Jadwal dibatalkan | Email pembatalan, notifikasi dosen |
| `SCHEDULE_POSTPONED` | Jadwal ditunda | Email penundaan, notifikasi dosen |

## 🚀 Cara Penggunaan

### Contoh Dasar

```python
from observer import ScheduleSubject, StudentObserver, LecturerObserver

# 1. Buat subject (publisher)
schedule_subject = ScheduleSubject()

# 2. Buat observers
student = StudentObserver("STU001", "student@university.ac.id")
lecturer = LecturerObserver("LEC001", "Dr. Ahmad", "+62812345678")

# 3. Attach observers ke subject
schedule_subject.attach(student)
schedule_subject.attach(lecturer)

# 4. Notify ketika jadwal berubah
schedule_data = {
    'course_name': 'OOP dan Agentic AI',
    'old_time': 'Tuesday 10:00 - 12:00',
    'new_time': 'Wednesday 14:00 - 16:00',
    'room': 'Lab 301',
    'lecturer_name': 'Dr. Ahmad'
}
schedule_subject.notify('SCHEDULE_CHANGED', schedule_data)

# 5. Detach observer jika diperlukan
schedule_subject.detach(student)
```

### Output Contoh

```
✓ Observer StudentObserver attached
✓ Observer LecturerObserver attached

[12:54:32] Notifying observers - Event: SCHEDULE_CHANGED
Data: {...}

📧 [Student] Email dikirim ke student@university.ac.id
   Subject: Jadwal Perkuliahan Berubah - OOP dan Agentic AI

🔔 [Dosen] Notifikasi: Jadwal Perkuliahan Berubah
   Dosen: Dr. Ahmad (LEC001)
   📱 SMS akan dikirim ke: +62812345678
```

## ✅ Keuntungan Observer Pattern

1. **Loose Coupling**: Publisher tidak perlu tahu detail observers
2. **Dynamic Subscription**: Observers dapat di-attach/detach secara dinamis
3. **Scalability**: Mudah menambah observer baru tanpa mengubah existing code
4. **Separation of Concerns**: Setiap observer menangani responsibilitynya sendiri
5. **Event-Driven Architecture**: Sistem yang reaktif dan responsif

## 📂 File Structure

```
Jadwal/
├── observer.py          # Core implementation
├── example_usage.py     # Usage examples
└── README.md           # Documentation
```

## 🧪 Testing

Jalankan example usage:

```bash
python example_usage.py
```

## 💡 Use Cases

1. **Notifikasi Perubahan Jadwal** - Mahasiswa dan dosen mendapat notifikasi real-time
2. **Alert Pembatalan Kelas** - Sistem otomatis mengirim notifikasi pembatalan
3. **Reminder Penundaan** - Pengingat untuk jadwal yang ditunda
4. **Multi-Channel Notifications** - Email untuk student, SMS untuk dosen
5. **Event Logging** - Track semua perubahan jadwal

## 🔧 Integrasi dengan Sistem Nyata

Untuk production, extend dengan:

```python
# Email service
class EmailService:
    @staticmethod
    def send(recipient: str, subject: str, body: str) -> bool:
        # Implementasi SMTP
        pass

# SMS service
class SMSService:
    @staticmethod
    def send(phone: str, message: str) -> bool:
        # Implementasi SMS gateway (Twilio, dll)
        pass

# Database logging
class ScheduleLogger:
    @staticmethod
    def log_event(event_type: str, data: Dict) -> bool:
        # Simpan ke database
        pass
```

## 📚 Referensi Diagram Alur

```
User mengubah jadwal
        ↓
    ScheduleSubject.notify(event_type, data)
        ↓
    Loop through semua observers
        ↓
    Observer.update(event_type, data)
        ↓
    ├─ StudentObserver → send email
    ├─ LecturerObserver → send SMS/notification
    └─ AdditionalObservers → custom actions
```

## 🎓 Pembelajaran

Pattern ini mengimplementasikan:
- **Behavioral Design Pattern**
- **Publish-Subscribe Model**
- **Event-Driven Architecture**
- **Loose Coupling Principle**
- **Open/Closed Principle** (SOLID)
"# Jadwal" 
