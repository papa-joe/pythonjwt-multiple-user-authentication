from pyexpat import model
from rest_framework import serializers
from .models import User, People

class UserSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('EmployeeId', 'EmployeeName', 'Department', 'DateOfJoining', 'PhotoFileName')