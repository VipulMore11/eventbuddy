from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import *

class OrganiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name','phone_no', 'profile_pic']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        phone_no = validated_data.get('phone_no')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        if not email:
            raise ValueError(_('The Email must be set'))
        User = get_user_model()
        user = User(email=email, username=email,first_name=first_name, last_name=last_name, phone_no=phone_no)
        user.set_password(password) 
        user.is_active= True
        user.save()
        Organiser.objects.create(user=user)
        return user
    
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name','phone_no', 'profile_pic']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        phone_no = validated_data.get('phone_no')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        if not email:
            raise ValueError(_('The Email must be set'))
        User = get_user_model()
        user = User(email=email, username=email,first_name=first_name, last_name=last_name, phone_no=phone_no)
        user.set_password(password) 
        user.is_active= True
        user.save()
        Staff.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user is not None:
                if user.is_active:
                    return user
                else:
                    raise ValidationError("User account is not active.")
            else:
                raise ValidationError("Invalid credentials. Please try again.")
        raise ValidationError("Both email and password are required.")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','phone_no', 'profile_pic']

class GetOrganiserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Organiser
        fields = '__all__'
        depth = 1

class GetProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model= Organiser
        fields= '__all__'
        depth=1
        