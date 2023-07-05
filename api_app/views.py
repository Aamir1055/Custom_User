
from urllib import response
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import Group 
from rest_framework.permissions import IsAdminUser
from api_app.models import CustomUser, UserDetails
from api_app.serializers import CustomUserSerializer, UserDetailsSerializer
import re 


@api_view(['GET'])
def cb_User_all(request: Request):
    authenticated_user = JWTAuthentication().authenticate(request)
    if authenticated_user is None:
        return Response("Given token not valid for any token type", status = status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        user_list = CustomUser.objects.all()
        serializer = CustomUserSerializer(user_list, many = True, context = {'request': None})
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response("Request Failed", status = status.HTTP_400_BAD_REQUEST)



@api_view(['GET', "PUT", "DELETE"])
def cb_User(request: Request):
    req_data = request.data
    authenticated_user = JWTAuthentication().authenticate(request)
    if authenticated_user is not None:
        USER, TOKEN = authenticated_user
    else:
        return Response("Given token not valid for any token type", status = status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        user_list = [USER]
        serializer = CustomUserSerializer(user_list, many = True, context = {'request': None})
        return Response(serializer.data, status = status.HTTP_200_OK)


    elif request.method == "PUT":
         
        
        email = req_data['email']
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        email = req_data['email']
        if not (re.search(regex,email)):
           
            return Response("Invaid Email", status = status.HTTP_200_OK)  
        phnum = req_data['phnum']
        first_name = req_data['first_name']
        last_name = req_data['last_name']
        password = req_data['password']
        if len(password)<5:
            return Response("password length should be greater than 5",status=status.HTTP_401_UNAUTHORIZED)
        

        user = CustomUser(first_name = first_name, last_name = last_name, email = email, phnum = phnum)
        user.set_password(password)
        user.save()

        if user:
            return Response("User Updated", status = status.HTTP_200_OK)
        else:
            return Response("Failed to Authenticate", status = status.HTTP_401_UNAUTHORIZED)

    elif request.method == "DELETE":
        USER.delete()
        return Response("User Deleted", status = status.HTTP_200_OK)

    return Response("Request Failed", status = status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def cb_Signup_User(request: Request):
    req_data = request.data

    if request.method == "POST":
        email = req_data['email']
        if len(email)==0:
            return Response("Feild should not be blank")
        
        email = req_data['email']
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        email = req_data['email']
        if not (re.search(regex,email)):
           
            return Response("Invaid Email", status = status.HTTP_200_OK)  
        
        phnum = req_data['phnum']
        if len(phnum)==0:
            return Response("Feild should not be blank")
        first_name = req_data['first_name']
        if len(first_name)==0:
            return Response("Feild should not be blank")
        last_name = req_data['last_name']
        if len(last_name)==0:
            return Response("Feild should not be blank")
        password = req_data['password']
        if len(password)==0:
            return Response("Feild should not be blank")
        if len(password)<5:
            return Response("password length should be greater than 5",status=status.HTTP_401_UNAUTHORIZED)



        if not bool(CustomUser.objects.filter(email = email)):
            user = CustomUser(first_name = first_name, last_name = last_name, email = email, phnum = phnum,password=password)

            

            user.set_password(password)
            user.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            if user:
                return Response("User Created", status = status.HTTP_200_OK)
        else:
            return Response("User Already Exists", status = status.HTTP_200_OK)

    return Response("Request Failed", status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def cb_Login_User(request: Request):

    def _authenticate(_email = None, _password = None):
        _user = CustomUser.objects.get(email = _email)
        if _user is not None:
            if _user.check_password(_password):
                return _user
        return None

    req_data = request.data
    if request.method == "POST":
        email = req_data['email']
        if len(email)==0:
            return Response("Feild should not be blank")
        password = req_data['password']
        if len(password)==0:
            return Response("Feild should not be blank")
        if _authenticate(email, password):
            return Response("User Logged In", status = status.HTTP_200_OK)
        else:
            return Response("Failed to Authenticate", status = status.HTTP_401_UNAUTHORIZED)

    return Response("Request Failed", status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def cb_UserDetails_all(request: Request):
    authenticated_user = JWTAuthentication().authenticate(request)
    if authenticated_user is None:
        return Response("Given token not valid for any token type", status = status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        user_list = UserDetails.objects.all()
        serializer = UserDetailsSerializer(user_list, many = True, context = {'request': None})
        return Response(serializer.data, status = status.HTTP_200_OK)

    return Response("Request Failed", status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', "POST", "PATCH", "DELETE"])
def cb_UserDetails(request: Request):
    req_data = request.data
    authenticated_user = JWTAuthentication().authenticate(request)
    if authenticated_user is not None:
        USER, TOKEN = authenticated_user
    else:
        return Response("Given token not valid for any token type", status = status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        user_list = UserDetails.objects.filter(user_email_id = USER.email)
        serializer = UserDetailsSerializer(user_list, many = True, context = {'request': None})
        return Response(serializer.data, status = status.HTTP_200_OK)

    elif request.method == "POST":
        age = req_data['age']
        dob = req_data['dob']
        profession = req_data['profession']
        address = req_data['address']
        hobby = req_data['hobby']
        user = UserDetails(age = age, dob = dob, profession = profession, address = address, hobby = hobby, user_email_id = USER.email)
        user.save()
        return Response(f"Details Added For {USER.email}", status = status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        age = req_data['age']
        dob = req_data['dob']
        profession = req_data['profession']
        address = req_data['address']
        hobby = req_data['hobby']
        user = UserDetails(age = age, dob = dob, profession = profession, address = address, hobby = hobby, user_email_id = USER.email)
        user.save()
        return Response(f"Details Updated For {USER.email}", status = status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        UserDetails.objects.filter(user_email_id = USER.email).delete()
        return Response("Details Deleted", status = status.HTTP_200_OK)

    return Response("Request Failed", status = status.HTTP_400_BAD_REQUEST)
