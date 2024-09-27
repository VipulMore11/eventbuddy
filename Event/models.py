from django.db import models
from Authentication.models import User

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
    organiser = models.ForeignKey(User, on_delete=models.CASCADE)  
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