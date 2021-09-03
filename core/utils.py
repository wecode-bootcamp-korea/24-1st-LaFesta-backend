import jwt

from django.http  import JsonResponse

from users import User
from my_settings import MY_SECRET_KEY


def login_decorator(func): 
    def wrapper(self,request, *args, **kwargs):
        try : 
            access_token = request.headers.get('Authorization', None)    
            payload = jwt.decode(access_token, MY_SECRET_KEY, algorithm='HS256')  
            request.user = User.objects.get(id=payload['id'])                                                           
        except jwt.exceptions.DecodeError:                                     
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except User.DoesNotExist:                     
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
