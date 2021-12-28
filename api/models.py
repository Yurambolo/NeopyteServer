from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, company=None, gender=None):
        if first_name is None:
            raise TypeError('Users should have a first name')
        if last_name is None:
            raise TypeError('Users should have a last name')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name,
                          company=company, gender=gender)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Vacancy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    key_words = models.TextField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sv_file = models.BinaryField(null=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, models.CASCADE)
    datetime = models.DateTimeField()
    link = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} {}".format(str(self.datetime), str(self.candidate))


class InterviewProgress(models.Model):
    interview = models.ForeignKey(Interview, models.CASCADE)
    datetime = models.DateTimeField()
    result = models.JSONField()

    def __str__(self):
        return "{} - {}".format(str(self.interview), str(self.datetime))
