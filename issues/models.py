import uuid
from django.db import models

class Issue(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    DEPARTMENT_CHOICES = [
        ('Roads & Infrastructure', 'Roads & Infrastructure'),
        ('Electricity & Lighting', 'Electricity & Lighting'),
        ('Sanitation & Waste', 'Sanitation & Waste'),
        ('Water & Drainage', 'Water & Drainage'),
        ('General Civic', 'General Civic'),
    ]

    tracking_id = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='General Civic')
    location = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    citizen_name = models.CharField(max_length=100, default='Anonymous')
    citizen_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            for _ in range(5):
                candidate = "TS-" + uuid.uuid4().hex[:8].upper()
                if not Issue.objects.filter(tracking_id=candidate).exists():
                    self.tracking_id = candidate
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.tracking_id}] {self.title} - {self.status}"