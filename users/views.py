from django.shortcuts import render
import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings import MY_SECRET_KEY 

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if User.objects.filter(email=data['email']).exists():
                if bcrypt.checkpw(data['password'].encode('utf-8'), (User.objects.get(email = data['email']).password).encode('utf-8')):
                    access_token = jwt.encode({"id": User.objects.get(email = data['email']).id }, MY_SECRET_KEY , algorithm="HS256")
                    return JsonResponse({"MESSAGE": "SUCCESS", 'token' : access_token}, status=200)
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)