from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'profile_pic']

    def create(self, validated_data):
        profile_pic = validated_data.pop('profile_pic', None)

        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )

        user.is_creator = True

        if profile_pic:
            user.profile_pic = profile_pic

        user.save()
        return user


class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = User.ROLE.ADMIN
        validated_data['is_staff'] = True
        validated_data['is_superuser'] = True
        validated_data['is_active'] = True
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        # Include the user object in the validated data
        data['user'] = user
        return data
       
# serializers.py
from rest_framework import serializers
from .models import ImagePost  # Use the new model name

class ImagePostSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = ImagePost
        fields = [
            'id', 'creator', 'title', 'description',
            'image', 'views', 'uploaded_at'
        ]
        read_only_fields = ['views', 'uploaded_at'] 

