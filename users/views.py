import json, re, bcrypt, jwt

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import MY_SECRET_KEY


class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        REGEX_EMAIL = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        REGEX_PASSWORD = re.compile(
            "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
        )

        password = data["password"]

        if User.objects.filter(email=data["email"]).exists():
            return JsonResponse({"MESSAGE": "ALREADY EXISTED EMAIL"}, status=400)

        if not REGEX_EMAIL.match(data["email"]):
            return JsonResponse({"MESSAGE": "EMAIL_ERROR"}, status=400)

        if not REGEX_PASSWORD.match(data["password"]):
            return JsonResponse({"MESSAGE": "PASSWORD_ERROR"}, status=400)

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        decoded_password = hashed_password.decode("utf-8")

        User.objects.create(
            name=data["name"],
            gender=data["gender"],
            email=data["email"],
            phone_number=data["phone_number"],
            password=decoded_password,
            birthday=data["birthday"],
        )
        return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)


class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            access_token = jwt.encode({"id": user.id}, MY_SECRET_KEY, algorithm="HS256")
            return JsonResponse(
                {"MESSAGE": "SUCCESS", "token": access_token}, status=200
            )

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
