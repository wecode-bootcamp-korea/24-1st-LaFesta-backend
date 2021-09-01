import json, re, bcrypt

from django.http     import JsonResponse
from django.views    import View

from users.models import User

class SignupView(View):
    def post(self, request):
        data             = json.loads(request.body)
        email_validation = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        password_validation = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
        password = data['password']
            
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'MESSAGE':"ALREADY EXISTED EMAIL"}, status=400)

        if not email_validation.match(data['email']):
            return JsonResponse({"MESSAGE":"EMAIL_ERROR"}, status=400)

        if not password_validation.match(data['password']):
            return JsonResponse({"MESSAGE":"PASSWORD_ERROR"}, status=400)

        hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        decoded_password = hashed_password.decode('utf-8')

        User.objects.create(
            name         = data['name'],
            gender       = data['gender'],
            email        = data['email'],
            phone_number = data['phone_number'],
            password     = decoded_password,
            birthday     = data['birthday']
            )
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
