from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser

from .models import CategoryModel, CandidateModel, VoteModel
from .serializers import CategorySerializer, CandidateSerializer, VoteSerializer


class CategoryViewSet(ModelViewSet):
    queryset = CategoryModel.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes=[IsAuthenticated, DjangoModelPermissions]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.add_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.change_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.view_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.delete_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().destroy(request, *args, **kwargs)
        

class CandidateViewSet(ModelViewSet):
    queryset = CandidateModel.objects.all().order_by('id')
    serializer_class = CandidateSerializer
    permission_classes=[DjangoModelPermissions, IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.add_candidatemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.change_candidatemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.view_candidatemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
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
    permission_classes=[DjangoModelPermissions, IsAuthenticated, IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.add_votemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.change_votemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.view_votemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.delete_votemodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().destroy(request, *args, **kwargs)