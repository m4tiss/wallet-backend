from rest_framework_simplejwt.tokens import UntypedToken


def get_user_id(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise ValueError("Brak lub nieprawidłowy nagłówek Authorization")

    token = auth_header.split(' ')[1]
    untokened = UntypedToken(token)
    user_id = untokened.payload['user_id']
    return user_id
