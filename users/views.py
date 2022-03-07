from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerialize, LoginSerialize, EmployeeSerializer
from .models import User, People
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerialize(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        
        err = {}

        if "email" not in request.data:
            err["email"] = "Email is required"

        if "password" not in request.data:
            err["password"] = "Password is required"

        if len(err) > 0:
            response = Response()
            response.data = err

            return response

        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
           raise AuthenticationFailed('Incorrect password')

        payload = {
            'id':user.id,
            "aud": "urn:user",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm="HS256")

        response = Response()

        response.set_cookie(key='user_token', value=token, httponly=True)

        response.data = {
            'message': 'success',
            'jwt': token
        }

        return response

class PeopleLoginView(APIView):
    def post(self, request):
        
        err = {}

        if "EmployeeName" not in request.data:
            err["EmployeeName"] = "EmployeeName is required"

        if "Department" not in request.data:
            err["Department"] = "Department is required"

        if len(err) > 0:
            response = Response()
            response.data = err

            return response

        EmployeeName = request.data['EmployeeName']
        Department = request.data['Department']
        
        people = People.objects.filter(EmployeeName=EmployeeName).first()

        if people is None:
            raise AuthenticationFailed('User not found')

        payload = {
            'id':people.EmployeeId,
            "aud": "urn:people",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm="HS256")

        response = Response()

        response.set_cookie(key='ppl_token', value=token, httponly=True)

        response.data = {
            'message': 'success',
            'jwt': token
        }

        return response

class UserView(APIView):
    def auth(request):

        token = request.COOKIES.get('user_token')

        if not token:
            return False
            
        try:
            payload = jwt.decode(token, 'secret', audience="urn:user", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidAudienceError:
            return False
        except jwt.InvalidIssuedAtError:
            return False

        user = User.objects.filter(id=payload['id']).first()

        return user

class PeopleView(APIView):
    def auth(request):

        token = request.COOKIES.get('ppl_token')

        if not token:
            return False

        try:
            payload = jwt.decode(token, 'secret', audience="urn:people", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidAudienceError:
            return False
        except jwt.InvalidIssuedAtError:
            return False

        people = People.objects.filter(EmployeeId=payload['id']).first()

        return people

class TestView(UserView):
    def get(self, request):
        if not UserView.auth(request):
            raise AuthenticationFailed('Unauthenticated')
        else:
            user =  UserView.auth(request)
            serializer = UserSerialize(user)

            return Response(serializer.data['name'])

class TestViewp(PeopleView):
    def get(self, request):
        if not PeopleView.auth(request):
            raise AuthenticationFailed('Unauthenticated')
        else:
            people =  PeopleView.auth(request)
            serializer = EmployeeSerializer(people)

            return Response(serializer.data)
         


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('user_token')
        response.data = {
            'message': 'success'
        }

        return response

class PeopleLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('ppl_token')
        response.data = {
            'message': 'success'
        }

        return response