import gzip, json, base64, jwt
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ItemDb
from .serializers import ItemDbSerializer
from django.middleware.gzip import GZipMiddleware
from django.http import FileResponse, HttpResponse

gzip_middleware = GZipMiddleware()

def data_to_gzip(data):
    file_name = 'gz-warehouse/items.gz'
    with gzip.GzipFile(file_name, 'w') as fout:
        fout.write(json.dumps(data).encode('utf-8'))
    return file_name

class ItemsList(generics.ListAPIView):
    # queryset = ItemDb.objects.all()

    def get(self, request):
        items = ItemDb.objects.all()
        serializer = ItemDbSerializer(items, many=True)
        res_data = list(serializer.data)
        gzip_file_name = data_to_gzip(res_data)
        response = HttpResponse(open(gzip_file_name, 'rb'))
        response['Content-Encoding'] = 'gzip'
        return response

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
#                     'exp': str(expired_at)
#                 }, 'authentication', algorithm='HS256')
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
#         serializer = RegisterSerializer(data=request.data)
#         request.data['birthdate'] = datetime.strptime(request.data['birthdate'], '%m/%d/%Y').date()
#         if serializer.is_valid():
#             data = dict(serializer.validated_data)
#             try:
#                 if Login.objects.get(userid=data['userid']):
#                     return Response({ 'detail': 'Username has existed' }, status=406)
#                 if Login.objects.get(email=data['email']):
#                     return Response({ 'detail': 'Email has existed' }, status=406)
#             except Login.DoesNotExist:
#                 # birthdate = datetime.strptime(data['birthdate'], '%m/%d/%Y')
#                 new_user = Login(userid=data['userid'],
#                                  user_pass=data['user_pass'],
#                                  email=data['email'],
#                                  birthdate=data['birthdate'],
#                                  sex=data['sex'])
#                 new_user.save()
#             return Response({ 'detail': 'Success' }, status=200)                
#         return Response({ 'detail' : 'Wrong format syntax' }, status=400)