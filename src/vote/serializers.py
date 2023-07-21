from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CategoryModel, CandidateModel, VoteModel
        
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateModel
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    
    class Meta:
        model = CategoryModel
        fields = '__all__'
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteModel
        fields = '__all__'
        
    validators = [
        UniqueTogetherValidator(
            queryset=VoteModel.objects.all(),
            fields=['category', 'candidate', 'ipv4', 'finger_print']
        )
    ]