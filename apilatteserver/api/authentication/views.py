import jwt
import base64
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Login, Token
from .serializers import LoginSerializer, RegisterSerializer

class LoginCheck(generics.CreateAPIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(Login, userid=serializer.validated_data['userid'])
            if user and user.user_pass == serializer.validated_data['user_pass']:
                create_at = timezone.now()
                expired_at = timezone.now() + timedelta(minutes=15)
                token = jwt.encode({
                    'id': user.userid,
                    'gid': user.group_id,
                    'exp': str(expired_at)
                }, '42y0cvq)_2^twb2m=&#_ubvag9%@19ubm(u$55a(0(0srqa$&i', algorithm='HS256')
                try:
                    _token = Token.objects.get(user=user)
                    _token.token = token.decode('utf-8')
                    _token.create_at = create_at
                    _token.expired_at = expired_at
                except Token.DoesNotExist:
                    _token = Token(user=user, token=token.decode('utf-8'))
                _token.save()
                return Response({ 'token': token.decode('utf-8') })
            return Response({'detail': 'Password mismatch'}, status=401)
        return Response({ 'detail' : 'Wrong format syntax. If you want to login, use two properties: userid, user_pass.' }, status=400)


class RegisterView(generics.CreateAPIView):

    def post(self, request):
        try:
            # if isinstance(request.data, dict):
            #     try:
            #         request.data['birthdate'] = datetime.strptime(request.data['birthdate'], '%m/%d/%Y').date()
            #     except ValueError:
            #         try:
            #             request.data['birthdate'] = datetime.strptime(request.data['birthdate'], '%d/%m/%Y').date()
            #         except ValueError:
            #             request.data['birthdate'] = datetime.strptime('1/1/2000', '%m/%d/%Y').date()
            # else:
            #     ini_data = request.data.dict()
            #     try:
            #         ini_data['birthdate'] = datetime.strptime(ini_data['birthdate'], '%m/%d/%Y').date()
            #     except ValueError:
            #         try:
            #             ini_data['birthdate'] = datetime.strptime(ini_data['birthdate'], '%d/%m/%Y').date()
            #         except ValueError:
            #             ini_data['birthdate'] = datetime.strptime('1/1/2000', '%m/%d/%Y').date()
            req_data = request.data.copy()
            try:
                req_data['birthdate'] = datetime.strptime(req_data['birthdate'], '%m/%d/%Y').date()
            except ValueError:
                try:
                    req_data['birthdate'] = datetime.strptime(req_data['birthdate'], '%d/%m/%Y').date()
                except ValueError:
                    req_data['birthdate'] = datetime.strptime('1/1/2000', '%m/%d/%Y').date()
            serializer = RegisterSerializer(data=req_data)
            if serializer.is_valid():
                print('should be validated')
                data = dict(serializer.validated_data)
                try:
                    if Login.objects.get(userid=data['userid']):
                        return Response({ 'detail': 'Username existed' }, status=406)
                except Login.DoesNotExist:
                    try:
                        if Login.objects.get(email=data['email']):
                            return Response({ 'detail': 'Email existed' }, status=406)
                    except Login.MultipleObjectsReturned:
                        return Response({ 'detail': 'Email existed' }, status=406)
                    except Login.DoesNotExist:
                        new_user = Login(userid=data['userid'],
                                        user_pass=data['user_pass'],
                                        email=data['email'],
                                        birthdate=data['birthdate'],
                                        sex=data['sex'])
                        new_user.save()
                    return Response({ 'detail': 'Success' }, status=200)                
            return Response({ 'detail' : 'Wrong syntax' }, status=400)
        except Exception as e:
            print(str(e))
            with open('~/error.log', 'a+') as f:
                f.write(str(e))

# class LoginViewSet(viewsets.ModelViewSet):
#     queryset = Login.objects.all()
#     serilizer_class = LoginSerializer

#     @action(methods=['post'], detail=False, url_name="login")
#     def login(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = get_object_or_404(Login, userid=serializer.validated_data['userid'])
#             if user and user.user_pass == serializer.validated_data['user_pass']:
#                 create_at = timezone.now()
#                 expired_at = timezone.now() + timedelta(minutes=15)
#                 token = jwt.encode({
#                     'id': user.userid,
#                     'gid': user.group_id,
#                     'exp': str(expired_at)
#                 }, '42y0cvq)_2^twb2m=&#_ubvag9%@19ubm(u$55a(0(0srqa$&i', algorithm='HS256')
#                 try:
#                     _token = Token.objects.get(user=user)
#                     _token.token = token.decode('utf-8')
#                     _token.create_at = create_at
#                     _token.expired_at = expired_at
#                 except Token.DoesNotExist:
#                     _token = Token(user=user, token=token.decode('utf-8'))
#                 _token.save()
#                 return Response({ 'token': token.decode('utf-8') })
#             return Response({'detail': 'Password mismatch'}, status=401)
#         return Response({ 'detail' : 'Wrong format syntax. If you want to login, use two properties: userid, user_pass.' }, status=400)


# class RegisterViewSet(viewsets.ModelViewSet):
#     queryset = Login.objects.all()
#     serializer_class = RegisterSerializer

#     def create(self, request):
#         print(request.data)
#         serializer = RegisterSerializer(data=request.data)
#         request.data['birthdate'] = datetime.strptime(request.data['birthdate'], '%m/%d/%Y').date()
#         if serializer.is_valid():
#             data = dict(serializer.validated_data)
#             try:
#                 if Login.objects.get(userid=data['userid']):
#                     return Response({ 'detail': 'Username existed' }, status=406)
#             except Login.DoesNotExist:
#                 try:
#                     if Login.objects.get(email=data['email']):
#                         return Response({ 'detail': 'Email existed' }, status=406)
#                 except Login.MultipleObjectsReturned:
#                     return Response({ 'detail': 'Email existed' }, status=406)
#                 except Login.DoesNotExist:
#                     # birthdate = datetime.strptime(data['birthdate'], '%m/%d/%Y')
#                     new_user = Login(userid=data['userid'],
#                                     user_pass=data['user_pass'],
#                                     email=data['email'],
#                                     birthdate=data['birthdate'],
#                                     sex=data['sex'])
#                     new_user.save()
#                 return Response({ 'detail': 'Success' }, status=200)                
#         return Response({ 'detail' : 'Wrong syntax' }, status=400)
