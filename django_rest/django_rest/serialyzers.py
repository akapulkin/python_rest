from django.contrib.auth.hashers import make_password
from django_rest.models import Employee
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class EmployeeSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True, max_length=100)
    password = serializers.CharField(required=False, allow_blank=True, max_length=100)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    birthdate = serializers.DateField()

    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'birthdate']

    def create(self, validated_data):
        """
        Create and return a new `Employer` instance, given the validated data.
        """
        user, created = User.objects.get_or_create(username=validated_data['username'])
        if created:
            user.password = make_password(validated_data['password'])
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            user.save()
            return Employee.objects.create(user=user, birthdate=validated_data['birthdate'])
        else:
            return f"This username:{validated_data['username']} already used"
