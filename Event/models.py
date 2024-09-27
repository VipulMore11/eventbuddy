from django.db import models
from Authentication.models import *

EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('conference', 'Conference'),
        ('fest', 'College Fest'),
        ('corporate', 'Corporate Event'),
    ]

class Event(models.Model):
    title = models.CharField(max_length=255)  
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()  
    date = models.CharField(max_length=255, null=True, blank=True)  
    start_time = models.CharField(max_length=255, null=True, blank=True) 
    end_time = models.CharField(max_length=255, null=True, blank=True) 
    venue = models.CharField(max_length=255) 
    organiser = models.ForeignKey(Organiser, on_delete=models.CASCADE)  
    budget = models.CharField(max_length=255, blank=True, null=True)
    no_of_guests = models.IntegerField(blank=True, default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    image = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} "
    
class WeddingDetails(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,  blank=True, null=True)
    bride_name = models.CharField(max_length=255)
    groom_name = models.CharField(max_length=255)
    theme = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Wedding: {self.bride_name} & {self.groom_name}"

class BirthdayDetails(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,blank=True, null=True)
    bd_person = models.CharField(max_length=255)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"Birthday of {self.birthday_person}"

class CorporateDetails(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True,null=True)
    speakers = models.TextField()  
    company_name = models.CharField(max_length=255)
    host = models.CharField(max_length=255, blank=True, null=True)
    agenda = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Corporate Event: {self.event.title}"

class CollegeFestDetails(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    fest_name = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255, blank=True, null=True)
    theme = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"College Fest: {self.fest_name}"
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('invitation', 'Invitation'),
        ('normal', 'Normal'),
    )
    
    title = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='normal')
    is_seen = models.BooleanField(default=False)
    status = models.CharField(max_length=20, null=True, blank=True) 
    from_who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.notification_type} - {'Seen' if self.is_seen else 'Unseen'}"
    
class Tasks(models.Model):
    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    assigned_by = models.ForeignKey(Organiser, on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.title}"