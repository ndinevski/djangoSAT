from rest_framework.serializers import ModelSerializer
from .models import Company
from .models import User

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'