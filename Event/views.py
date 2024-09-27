from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *
from Chat.models import ChatRoom
from Authentication.serializers import GetAllStaffSerializer
from django.db.models import Q

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):    
    event_data = request.data.copy()
    event_data['title'] = event_data.get('title', '')
    event_data['event_type'] = event_data.get('event_type', '')
    event_data['description'] = event_data.get('description', '')
    event_data['date'] = event_data.get('date', '')
    event_data['start_time'] = event_data.get('start_time', '')
    event_data['end_time'] = event_data.get('end_time', '')
    event_data['venue'] = event_data.get('venue', '')
    event_data['organizer'] = request.user.id  # Assuming the organizer is the logged-in user
    event_data['budget'] = event_data.get('budget', '')
    event_data['no_of_guests'] = event_data.get('no_of_guests', 0)
    event_data['image'] = event_data.get('image', '')
    event_data['contact'] = event_data.get('contact', '')

    event_serializer = EventSerializer(data=event_data)
    if event_serializer.is_valid():
        ev = event_serializer.save()
        # print(ev.id)
        event, created = Event.objects.get_or_create(id=ev.id)
        
        chatroom = ChatRoom.objects.create(name=event.title)
        chatroom.participants.add(request.user)
        chatroom.save()
        # print(event)
        if event.event_type == 'wedding':
            wedding_data = WeddingDetails.objects.create(
                bride_name=event_data.get('bride_name'),
                groom_name=event_data.get('groom_name'),
                theme=event_data.get('theme')
            )
            wedding_data.event = event
            wedding_data.save()
            
            return Response({'message': 'Wedding created.'},status=status.HTTP_201_CREATED)

        elif event.event_type == 'birthday':
            birthday_data = BirthdayDetails.objects.create(
                bd_person=event_data.get('bd_person'),
                age=event_data.get('age')
            )
            birthday_data.event = event
            birthday_data.save()
            return Response({'message': 'Birthday created.'}, status=status.HTTP_201_CREATED)

        elif event.event_type == 'conference':
            corporate_data = CorporateDetails.objects.create(
                speakers=event_data.get('speakers'),
                company_name=event_data.get('company_name'),
                host=event_data.get('host'),
                agenda=event_data.get('agenda')
            )
            corporate_data.event = event
            corporate_data.save()
            return Response({'message': 'Corporate event created.'}, status=status.HTTP_201_CREATED)

        elif event.event_type == 'fest':
            fest_data = CollegeFestDetails.objects.create(
                fest_name=event_data.get('fest_name'),
                college_name=event_data.get('college_name'),
                theme=event_data.get('theme')
            )
            fest_data.event = event
            fest_data.save()
            return Response({'message': 'College Fest created.'}, status=status.HTTP_201_CREATED)
    else:
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request):
    try:
        user = request.user
        ev_id = request.GET.get('id')
        if ev_id is None:
            org = Organiser.objects.get(user=user)
            events = Event.objects.filter(organiser=org)
            serializer = GetEventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            events = Event.objects.get(id=ev_id)
            serializer = GetEventSerializer(events)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    data = request.data
    organizer_id = request.user
    recipient = request.data.get('recipient')
    reci = User.objects.get(id=recipient)
    print(reci)
    # Step 1: Check if the organizer exists
    try:
        organizer = User.objects.get(id=organizer_id.id)
        print(organizer)
    except Organiser.DoesNotExist:
        return Response({'error': 'Organizer not found.'}, status=status.HTTP_404_NOT_FOUND)
    try:
        Notification.objects.create(
            title=data.get('title', ''),
            notification_type=data.get('notification_type', 'normal'),
            status=data.get('status', None),
            from_who=organizer,
            recipient=reci
        )
        return Response({'message': 'Notifications sent successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f"Failed to create notification for recipient "}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    user = request.user
    try:
        organiser = Organiser.objects.get(user=user)
    except Organiser.DoesNotExist:
        return Response({'error': 'Only organizers can create tasks.'}, status=status.HTTP_403_FORBIDDEN)
    

    data = request.data
    try:
        eve = Event.objects.get(id=data.get('event', ''),)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=status.HTTP_403_FORBIDDEN)
    try:
        su = User.objects.get(id=data.get('assigned_to'))
        assigned_to = Staff.objects.get(user=su)
    except Staff.DoesNotExist:
        return Response({'error': 'Assigned staff member not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Create the task
    task = Tasks.objects.create(
        title=data.get('title', ''),
        description=data.get('description', ''),
        event=eve,
        assigned_by=organiser,
        assigned_to=assigned_to,
        start_date=data.get('start_date', ''),
        end_date=data.get('end_date', ''),
        priority=data.get('priority', 'medium'),  # Default is 'medium'
        status=data.get('status', 'new')  # Default is 'new'
    )


    # Serialize the created task
    serializer = TaskSerializer(task)
    return Response({'message': 'Task created successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    try:
        user = request.user
        org = Organiser.objects.get(user=user)
        eve = Event.objects.get(id=request.GET.get('event_id'))
        tasks = Tasks.objects.filter(Q(assigned_by=org) & Q(event_id=eve))
        serializers = TaskSerializer(tasks, many=True)
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_staff(request):
    try:
        staff = Staff.objects.all()
        serializers = GetAllStaffSerializer(staff, many=True)
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)