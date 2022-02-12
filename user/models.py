from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, is_kakao, name, kakao_id , major, phone_number, student_id, position):
        
        if not email: 
            raise ValueError('Users should have your email')
        email = self.normalize_email(email)

        if not is_kakao: 
            user = self.model(
                email = email,
                is_staff = is_staff,
                is_active = True,
                is_superuser = is_superuser,
                is_kakao = is_kakao,
                kakao_id = None,
                name = name,
                major = major,
                phone_number = phone_number,
                student_id = student_id,
                position = position,
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

        else:
            user = self.model(
                email = email,
                is_staff = is_staff,
                is_active = True,
                is_superuser = is_superuser,
                is_kakao = is_kakao,
                kakao_id = kakao_id,
                name = name,
                major = major,
                phone_number = phone_number,
                student_id = student_id,
                position = position,
            )
            user.set_unusable_password()
            user.save(using=self._db)
            return user

    def create_user(self, email,  password, is_kakao, name, kakao_id, major, phone_number, student_id, position):
        return self._create_user(email, password,False, False, is_kakao, name, kakao_id, major, phone_number, student_id, position)

    def create_superuser(self, email, password):
        return self._create_user(email, password,True,True,False, '','','','','','')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    position_choices=[
        (None, '선택'),
        ('개발', '개발'),
        ('기획', '기획'),
        ('디자인', '디자인'),
    ]
    email = models.EmailField(max_length=100, unique=True, blank=False, null=True)
    name = models.CharField(max_length=20, blank=False, null=True)
    major = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    student_id = models.CharField(max_length=12)
    position = models.CharField(
        max_length=10,
        choices = position_choices,
        default='선택',
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_kakao = models.BooleanField(default=False) 
    kakao_id = models.CharField(max_length=15, default='', unique=True, blank=False, null=True)    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELD = ['email', 'name', 'major', 'phone_number', 'student_id','position']

    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk) 
