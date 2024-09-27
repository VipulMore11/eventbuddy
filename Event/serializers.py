from rest_framework import serializers
from .models import *
from Authentication.serializers import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title', 
            'event_type', 
            'description', 
            'date', 
            'start_time', 
            'venue', 
            'image',
            'organiser', 
            'budget', 
            'no_of_guests', 
        ]
    def create(self, validated_data):
        title = validated_data.get('title')
        event_type = validated_data.get('event_type')
        description = validated_data.get('description')
        date = validated_data.get('date')
        image = validated_data.get('image')
        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')
        venue = validated_data.get('venue')
        organiser = validated_data.get('organiser')
        budget = validated_data.get('budget')
        no_of_guests = validated_data.get('no_of_guests')
        image = validated_data.get('image')
        contact = validated_data.get('contact')

        # Create the Event instance with all validated data
        event = Event.objects.create(
            title=title,
            event_type=event_type,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            organiser=organiser, 
            budget=budget,
            no_of_guests=no_of_guests,
            image=image,
            contact=contact
        )
        return event

class GetEventSerializer(serializers.ModelSerializer):
    organiser = GetOrganiserSerializer()
    class Meta:
        model = Event
        fields = '__all__'
        depth = 1

class WeddingDetailsSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = WeddingDetails
        fields = ['event', 'bride_name', 'groom_name', 'theme']


class BirthdayDetailsSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = BirthdayDetails
        fields = ['event','bd_person', 'age']


class CorporateDetailsSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = CorporateDetails
        fields = ['event','speakers', 'company_name', 'host', 'agenda']


class CollegeFestDetailsSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    class Meta:
        model = CollegeFestDetails
        fields = ['event','fest_name', 'college_name', 'theme']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title', 'notification_type', 'status', 'from_who', 'recipient']
        read_only_fields = ['from_who']
    
class GetNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    assigned_by = GetOrganiserSerializer()
    assigned_to = GetStaffSerializer()
    class Meta:
        model = Tasks
        fields = ['id', 'title','event', 'description', 'assigned_by', 'assigned_to', 
                  'start_date', 'end_date', 'priority', 'status']