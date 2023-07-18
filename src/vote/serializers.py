from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CategoryModel, CandidateModel, VoteModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateModel
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteModel
        fields = '__all__'