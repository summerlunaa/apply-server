from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser


class KakaoBackend(BaseBackend):
    """
    login 시 authenticate를 진행시키는 함수
    authenticate 시에 email, kakao_id 및 password를 검증 추가 구현
    """
    def authenticate(self, request, email=None, password=None, kakao_id=None ):
        if kakao_id is not None: #카카오 로그인의 경우
            try:
                user = CustomUser.objects.get(kakao_id=kakao_id)
                return user
            except CustomUser.DoesNotExist:
                return None
        else: # 일반 로그인의 경우
            try:
                user = CustomUser.objects.get(email=email) 
                if password is None:
                    return user
                try:
                    validate_password(password, user)
                    return user
                except ValidationError:
                    return None
            except CustomUser.DoesNotExist: 
                return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None