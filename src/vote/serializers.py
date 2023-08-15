from rest_framework import serializers

from .models import CategoryModel, CandidateModel, VoteModel
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteModel
        fields = '__all__'
        
    def create(self, validated_data):
        category = validated_data.get('category')
        ipv4 = validated_data.get('ipv4')
        finger_print = validated_data.get('finger_print')
        
        if VoteModel.objects.filter(category=category, ipv4=ipv4).exists():
            raise serializers.ValidationError('You can only vote once per category!')
        
        if VoteModel.objects.filter(category=category, finger_print=finger_print).exists():
            raise serializers.ValidationError('You can only vote once per category!')
        
        instance = super().create(validated_data)
        return instance
        
class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CandidateModel
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    category_vote_count = serializers.SerializerMethodField()
    vote_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = CategoryModel
        fields = '__all__'
    
    def get_category_vote_count(self, instance):
        return VoteModel.objects.filter(category=instance.id).count()
        
    def get_vote_percentage(self, instance):
        total_vote_count = VoteModel.objects.all().count()
        category_vote_count = self.get_category_vote_count(instance)
        percentage = (category_vote_count / total_vote_count) * 100 if total_vote_count else 0
        return percentage
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category_id = representation['id']
        for candidate_data in representation['candidates']:
            category_query = VoteModel.objects.filter(category=category_id)
            total_category_vote_count = category_query.count()
            candidate_vote_count = category_query.filter(category=category_id, candidate=candidate_data['id']).count()
            candidate_data['vote_count_in_the_category'] = candidate_vote_count
            candidate_data['vote_percentage_in_the_category'] = (candidate_vote_count / total_category_vote_count) * 100 if total_category_vote_count else 0
                
        return representation