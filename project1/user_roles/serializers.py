from rest_framework import serializers
from .models import User, Role, UserRole

class UserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    class Meta:
        model = User
        fields = ('id','username')

    def create(self, validated_data):
       pw = User.objects.make_random_password()
       validated_data['password'] = pw
       un = validated_data.get('username')
       return  User.objects.create_user(**validated_data)
        

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id','role', 'status', 'user')

    def update(self,instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

