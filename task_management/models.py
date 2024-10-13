from django.db import models

# Create your models here.
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Assessment(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="assessment")
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return f"{self.task.title} - Priority: {self.get_priority_display()}"
