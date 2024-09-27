from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer, GetMessageSerializer
from Authentication.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_chatrooms(request):
    user = request.user
    chatrooms = ChatRoom.objects.filter(participants=user, is_private=True)
    serializer = ChatRoomSerializer(chatrooms, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chatroom(request):
    participant_id = request.data.get('participant_id')
    participant = get_object_or_404(User, pk=participant_id)
    user = request.user

    existing_chatroom = ChatRoom.objects.filter(
        Q(participants=user) & Q(participants=participant)
    ).first()
    if existing_chatroom:
        return Response(ChatRoomSerializer(existing_chatroom).data, status=status.HTTP_200_OK)

    chatroom = ChatRoom.objects.create(is_private=True)
    chatroom.participants.add(user, participant)
    chatroom.save()
    serializer = ChatRoomSerializer(chatroom)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.participants.all():
        return Response({"error": "You are not a participant in this chatroom."}, status=status.HTTP_403_FORBIDDEN)

    messages = Message.objects.filter(room=room)
    serializer = GetMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.participants.all():
        return Response({"error": "You are not a participant in this chatroom."}, status=status.HTTP_403_FORBIDDEN)

    data = request.data.copy()
    data['room'] = room.id
    data['sender'] = request.user.id
    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
