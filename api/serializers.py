from base64 import b64encode, b64decode

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from docx2txt import process
from .relevance import relevance_filter
from .models import User, Candidate, Vacancy, Interview


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'company', 'gender')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        if 'company' not in validated_data:
            validated_data['company'] = None
        if 'gender' not in validated_data:
            validated_data['gender'] = None
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company=validated_data['company'],
            gender=validated_data['gender'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CandidateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    sv_file = serializers.FileField(required=False)

    class Meta:
        model = Candidate
        fields = ('id', 'email', 'first_name', 'last_name', 'sv_file', 'vacancy')
        extra_kwargs = {
            'vacancy': {'required': True},
        }

    def validate(self, attrs):
        if 'sv_file' in attrs:
            sv_text = process(attrs['sv_file'])
            tags = Vacancy.objects.filter(id=attrs['vacancy'].id).first().key_words.split(', ')
            if not relevance_filter(tags, sv_text):
                raise serializers.ValidationError({"sv_file": "SV file is not compatible to this vacancy"})
            attrs['sv_file'] = attrs['sv_file'].read()
        return attrs

    def to_representation(self, instance):
        representation = super(CandidateSerializer, self).to_representation(instance)
        if instance.sv_file:
            representation['sv_file'] = b64encode(instance.sv_file)
            tmp = b64decode(representation['sv_file'])
        return representation


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ('id', 'name', 'description', 'key_words')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'key_words': {'required': True},
        }


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ('id', 'candidate', 'datetime', 'link')
        extra_kwargs = {
            'candidate': {'required': True},
            'datetime': {'required': True},
        }


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=False, allow_blank=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'first_name', 'last_name', 'company', 'gender')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if 'password' in attrs and attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        if 'company' in validated_data:
            instance.company = validated_data['company']
        if 'gender' in validated_data:
            instance.gender = validated_data['gender']
        if 'password' in validated_data and validated_data['password']:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company=validated_data['company'],
            gender=validated_data['gender'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
