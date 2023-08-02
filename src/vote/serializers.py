from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from .models import CategoryModel, CandidateModel, VoteModel
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteModel
        fields = '__all__'
        
    def create(self, validated_data):
        category = validated_data.get('category')
        ipv4 = validated_data.get('ipv4')
        finger_print = validated_data.get('finger_print')
        
        if VoteModel.objects.filter(category=category, ipv4=ipv4, finger_print=finger_print).exists():
            raise serializers.ValidationError('You can only vote once per category!')
        
        instance = super().create(validated_data)
        return instance
        
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateModel
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    
    class Meta:
        model = CategoryModel
        fields = '__all__'