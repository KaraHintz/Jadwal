from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class Observer(ABC):
    """Abstract base class for observers"""
    
    @abstractmethod
    def update(self, event_type: str, schedule_data: Dict[str, Any]) -> None:
        """
        Called when schedule subject notifies observers
        
        Args:
            event_type: Type of event (e.g., 'SCHEDULE_CHANGED')
            schedule_data: Schedule data related to the event
        """
        pass


class ScheduleSubject:
    """Publisher class that manages schedule notifications"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to receive notifications
        
        Args:
            observer: Observer instance to attach
        """
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"✓ Observer {observer.__class__.__name__} attached")
    
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from notifications
        
        Args:
            observer: Observer instance to detach
        """
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"✓ Observer {observer.__class__.__name__} detached")
    
    def notify(self, event_type: str, schedule_data: Dict[str, Any]) -> None:
        """
        Notify all attached observers about an event
        
        Args:
            event_type: Type of event
            schedule_data: Schedule data related to the event
        """
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Notifying observers - Event: {event_type}")
        print(f"Data: {schedule_data}\n")
        
        for observer in self._observers:
            observer.update(event_type, schedule_data)


class StudentObserver(Observer):
    """Observer that handles student notifications"""
    
    def __init__(self, student_id: str, email: str):
        self.student_id = student_id
        self.email = email
    
    def update(self, event_type: str, schedule_data: Dict[str, Any]) -> None:
        """
        Handle student notification for schedule changes
        
        Args:
            event_type: Type of event
            schedule_data: Schedule data
        """
        if event_type == 'SCHEDULE_CHANGED':
            self._send_email_notification(schedule_data)
        elif event_type == 'SCHEDULE_CANCELLED':
            self._send_cancellation_email(schedule_data)
        elif event_type == 'SCHEDULE_POSTPONED':
            self._send_postponement_email(schedule_data)
    
    def _send_email_notification(self, schedule_data: Dict[str, Any]) -> None:
        """Send schedule change email to student"""
        subject = f"Jadwal Perkuliahan Berubah - {schedule_data.get('course_name', 'N/A')}"
        body = f"""
Mahasiswa: {self.student_id}

Pemberitahuan: Jadwal perkuliahan Anda telah berubah.

Informasi Jadwal:
- Mata Kuliah: {schedule_data.get('course_name', 'N/A')}
- Waktu Lama: {schedule_data.get('old_time', 'N/A')}
- Waktu Baru: {schedule_data.get('new_time', 'N/A')}
- Ruang Kelas: {schedule_data.get('room', 'N/A')}
- Dosen: {schedule_data.get('lecturer_name', 'N/A')}

Pastikan Anda mengecek perubahan ini di sistem akademik.

Salam,
Admin Jadwal
        """
        print(f"📧 [Student] Email dikirim ke {self.email}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body}")
    
    def _send_cancellation_email(self, schedule_data: Dict[str, Any]) -> None:
        """Send cancellation notification to student"""
        subject = f"Pembatalan Jadwal - {schedule_data.get('course_name', 'N/A')}"
        body = f"Jadwal {schedule_data.get('course_name')} dibatalkan."
        print(f"📧 [Student] Email pembatalan dikirim ke {self.email}")
        print(f"   Subject: {subject}")
    
    def _send_postponement_email(self, schedule_data: Dict[str, Any]) -> None:
        """Send postponement notification to student"""
        subject = f"Penundaan Jadwal - {schedule_data.get('course_name', 'N/A')}"
        body = f"Jadwal {schedule_data.get('course_name')} ditunda ke {schedule_data.get('new_time')}."
        print(f"📧 [Student] Email penundaan dikirim ke {self.email}")
        print(f"   Subject: {subject}")


class LecturerObserver(Observer):
    """Observer that handles lecturer notifications"""
    
    def __init__(self, lecturer_id: str, name: str, phone: str = None):
        self.lecturer_id = lecturer_id
        self.name = name
        self.phone = phone
    
    def update(self, event_type: str, schedule_data: Dict[str, Any]) -> None:
        """
        Handle lecturer notification for schedule changes
        
        Args:
            event_type: Type of event
            schedule_data: Schedule data
        """
        if event_type == 'SCHEDULE_CHANGED':
            self._notify_schedule_change(schedule_data)
        elif event_type == 'SCHEDULE_CANCELLED':
            self._notify_cancellation(schedule_data)
        elif event_type == 'SCHEDULE_POSTPONED':
            self._notify_postponement(schedule_data)
    
    def _notify_schedule_change(self, schedule_data: Dict[str, Any]) -> None:
        """Notify lecturer of schedule changes"""
        message = f"""
🔔 [Dosen] Notifikasi: Jadwal Perkuliahan Berubah
   Dosen: {self.name} ({self.lecturer_id})
   Mata Kuliah: {schedule_data.get('course_name', 'N/A')}
   Waktu Lama: {schedule_data.get('old_time', 'N/A')}
   Waktu Baru: {schedule_data.get('new_time', 'N/A')}
   Ruang Kelas: {schedule_data.get('room', 'N/A')}
        """
        self._send_notification(message)
    
    def _notify_cancellation(self, schedule_data: Dict[str, Any]) -> None:
        """Notify lecturer of schedule cancellation"""
        message = f"""
🔔 [Dosen] Notifikasi: Jadwal Dibatalkan
   Dosen: {self.name} ({self.lecturer_id})
   Mata Kuliah: {schedule_data.get('course_name', 'N/A')}
   Alasan: {schedule_data.get('reason', 'Tidak ada alasan')}
        """
        self._send_notification(message)
    
    def _notify_postponement(self, schedule_data: Dict[str, Any]) -> None:
        """Notify lecturer of schedule postponement"""
        message = f"""
🔔 [Dosen] Notifikasi: Jadwal Ditunda
   Dosen: {self.name} ({self.lecturer_id})
   Mata Kuliah: {schedule_data.get('course_name', 'N/A')}
   Waktu Baru: {schedule_data.get('new_time', 'N/A')}
        """
        self._send_notification(message)
    
    def _send_notification(self, message: str) -> None:
        """Send notification via SMS or system alert"""
        print(message)
        if self.phone:
            print(f"   📱 SMS akan dikirim ke: {self.phone}")
