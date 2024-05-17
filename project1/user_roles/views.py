from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Role, UserRole
from .serializers import UserSerializer, RoleSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .signals import UserStore
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAuthenticated




class UserAPI(APIView):
    def get(self, request):
        obj = User.objects.all()
        serializer = UserSerializer(obj, many=True)
        return Response(data=serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=400)
    
    def put(self, request, pk):
        obj = User.objects.get(pk=pk)
        serializer = UserSerializer(data=request.data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=400 )
    
    def delete(self, request, pk):
        obj = User.objects.get(pk=pk)
        user = UserRole.objects.get( user=obj )
        user.status = 'disabled'
        user.save()
        return Response(data={"msg":"User deleted."}, status=200)
    

def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
    
        
        return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

class LoginView(APIView):

	def post(self,request):
		un = request.data.get( 'username' )
		pw = request.data.get( 'password' )
		user = authenticate(username=un,password=pw)
		ur_count = UserRole.objects.filter( user=user ).count()
		if user:
			if ur_count != 1:
				u=UserStore()
				u.user_login(request,user)
				tokens_data = get_tokens_for_user(user)
            
				return Response(data = tokens_data)
			return Response({"msg": "user is disabled."}, status=200)
		return Response({"msg": "user and password incorrect."}, status=400)


class LogoutView(APIView):
	authentication_classes = [ JWTAuthentication ]
	permission_classes = [ IsAuthenticated ]

	def get(self,request):
		u=UserStore()
		u.user_logout(request,request.user)
		return Response(data={"msg":"logged out."}, status=200)


class UserRoleView(APIView):
    authentication_classes = [ JWTAuthentication ]
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"msg":"role changed"}, status=200)
        return Response(data={"msg": "role not changed"}, status=400)

    def get(self, request):
        obj = Role.objects.all()
        serializer = RoleSerializer(obj, many=True)
        return Response(data=serializer.data, status=200)


    def put(self,request,pk):
        obj = Role.objects.get( pk=pk)
        serializer = RoleSerializer( data=request.data, instance=obj, partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(data={"msg":"Role changed."})
        return Response(data={"msg":"Role isn't changed."})




class ChangeUserRoleView(APIView):

	authentication_classes = [ JWTAuthentication ]
	permission_classes = [ IsAuthenticated ]

	def put(self,request,pk=None):
		obj = UserRole.objects.get( pk=pk )
		serializer = RoleSerializer( data=request.data,instance=obj,partial=True )
		if serializer.is_valid():
			serializer.save()
			return Response(data={"msg":"Role changed."})
		return Response(data={"msg":"Role is't changed."})


