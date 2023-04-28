from rest_framework import validators
from django.contrib.auth import password_validation as pv
from rest_framework import serializers
from .models import Category, Item, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserRegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, write_only=True)
    password_2 = serializers.CharField(max_length=64, write_only=True)#только для передечи, возваращать не будет (wtite_only)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError('Пароли не совпадают')
        if attrs['username'] == attrs['password']:
            raise serializers.ValidationError('Нельзя')
        return attrs

    def validate_password(self, value):
        try:
            pv.validate_password(value)
        except pv.ValidationError as e:
            raise serializers.ValidationError(e)
        else:
            return value

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

