from django.db import models
from django.contrib.auth.models import User


class Ward(models.Model):
    name = models.CharField(max_length=100)
    ward_number = models.PositiveIntegerField(unique=True)
    zone = models.CharField(max_length=100, default='East Zone')

    class Meta:
        ordering = ['ward_number']

    def __str__(self):
        return f"Ward {self.ward_number} - {self.name}"


class Community(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='communities')
    name = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = 'Communities'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.ward.name})"


class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('road', 'Roads & Footpaths'),
        ('water', 'Water Supply'),
        ('sewage', 'Drainage & Sewage'),
        ('garbage', 'Garbage & Sanitation'),
        ('electricity', 'Streetlights & Power'),
        ('traffic', 'Traffic & Parking'),
        ('parks', 'Parks & Greenery'),
        ('health', 'Public Health & Pest Control'),
        ('safety', 'Public Safety & Vandalism'),
        ('other', 'Other / General'),
    ]

    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    location = models.CharField(max_length=200)
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issues'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    upvotes = models.PositiveIntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_issues', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment on {self.issue.title}"


class IssueStatusLog(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='status_logs')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    old_status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=Issue.STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.issue.title}: {self.old_status} -> {self.new_status} by {self.changed_by}"