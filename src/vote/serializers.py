from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CategoryModel, CandidateModel, VoteModel
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteModel
        fields = '__all__'
        
    validators = [
        UniqueTogetherValidator(
            queryset=VoteModel.objects.all(),
            fields=['category', 'candidate']
        ),
        UniqueTogetherValidator(
            queryset=VoteModel.objects.all(),
            fields=['category', 'ipv4']
        ),
        UniqueTogetherValidator(
            queryset=VoteModel.objects.all(),
            fields=['category', 'finger_print']
        ),
        UniqueTogetherValidator(
            queryset=VoteModel.objects.all(),
            fields=['candidate', 'ipv4']
        ),
        UniqueTogetherValidator(
            queryset=VoteModel.objects.all(),
            fields=['candidate', 'finger_print']
        )
    ]
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateModel
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    
    class Meta:
        model = CategoryModel
        fields = '__all__'