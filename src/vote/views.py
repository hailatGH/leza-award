from django.db.models import Q
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


from .models import CategoryModel, CandidateModel, VoteModel
from .serializers import CategorySerializer, CandidateSerializer, VoteSerializer, CategoryNoCandidateSerializer
from utils.custom_permissions import CustomPermission
from django.db.models import Count

class CategoryViewSet(ModelViewSet):
    queryset = CategoryModel.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes=[CustomPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(vote_count=Count('votemodel__category')).order_by('-vote_count')
        fetch_top_categories = self.request.query_params.get('fetch_top_categories')

        if fetch_top_categories:
            queryset = queryset.filter(is_top_category=True)

        return queryset
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.add_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.change_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.delete_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        
        if CategoryModel.objects.get(id=kwargs['pk']).candidates.exists():
            return Response({'message': 'You can not delete the category since it has candidates init.'}, status=400)
        
        return super().destroy(request, *args, **kwargs)        
    
    
class CategoryNoCandidateViewSet(ModelViewSet):
    queryset = CategoryModel.objects.all().order_by('id')
    serializer_class = CategoryNoCandidateSerializer
    permission_classes=[CustomPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(vote_count=Count('votemodel__category')).order_by('-vote_count')
        fetch_top_categories = self.request.query_params.get('fetch_top_categories')

        if fetch_top_categories:
            queryset = queryset.filter(is_top_category=True)

        return queryset
    
    def create(self, request, *args, **kwargs):
        return Response("Not allowed!", status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        return Response("Not allowed!", status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        return Response("Not allowed!", status=status.HTTP_400_BAD_REQUEST)   

class CandidateViewSet(ModelViewSet):
    queryset = CandidateModel.objects.all().order_by('id')
    serializer_class = CandidateSerializer
    permission_classes=[CustomPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(vote_count=Count('votemodel__candidate')).order_by('-vote_count')
        return queryset 
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.add_candidatemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.change_candidatemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.delete_candidatemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().destroy(request, *args, **kwargs)

class VoteViewSet(ModelViewSet):
    queryset = VoteModel.objects.all().order_by('id')
    serializer_class = VoteSerializer
    
    def update(self, request, *args, **kwargs):
       raise MethodNotAllowed(request.method, HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, HTTP_405_METHOD_NOT_ALLOWED)
    
    def list(self, request, *args, **kwargs):
        response = {}
        
        category_id = self.request.query_params.get('category_id')
        candidate_id = self.request.query_params.get('candidate_id')
        
        today = date.today()
        
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        start_of_month = date(today.year, today.month, 1)
        
        next_month = today.month + 1
        next_year = today.year
        
        if next_month > 12:
            next_month = 1  # Reset month to January
            next_year += 1   # Increment the year

        end_of_month = date(next_year, next_month, 1) - timedelta(days=1)
       
        if category_id:
            category_vote = self.queryset.filter(category=int(category_id))
            response["category_votes_of_the_day"] = category_vote.filter(created_at__date=today).count()
            response["category_votes_of_the_week"] = category_vote.filter(created_at__date__range=[start_of_week, end_of_week]).count()
            response["category_votes_of_the_month"] = category_vote.filter(created_at__date__range=[start_of_month, end_of_month]).count()
            response["total_category_votes"] = category_vote.count()
            return Response(response, status=status.HTTP_200_OK)
        
        if candidate_id:
            candidate_vote = self.queryset.filter(candidate=int(candidate_id))
            response["candidate_votes_of_the_day"] = candidate_vote.filter(created_at__date=today).count()
            response["candidate_votes_of_the_week"] = candidate_vote.filter(created_at__date__range=[start_of_week, end_of_week]).count()
            response["candidate_votes_of_the_month"] = candidate_vote.filter(created_at__date__range=[start_of_month, end_of_month]).count()
            response["total_candidate_votes"] = candidate_vote.count()
            return Response(response, status=status.HTTP_200_OK)
        
        response["total_votes_of_the_day"] = self.queryset.filter(created_at__date=today).count()
        response["total_votes_of_the_week"] = self.queryset.filter(created_at__date__range=[start_of_week, end_of_week]).count()
        response["total_votes_of_the_month"] = self.queryset.filter(created_at__date__range=[start_of_month, end_of_month]).count()
        response["total_votes"] = self.queryset.count()

        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, HTTP_405_METHOD_NOT_ALLOWED)