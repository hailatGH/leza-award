from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


from .models import CategoryModel, CandidateModel, VoteModel
from .serializers import CategorySerializer, CandidateSerializer, VoteSerializer
from utils.custom_permissions import CustomPermission

class CategoryViewSet(ModelViewSet):
    queryset = CategoryModel.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes=[CustomPermission]
    
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
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        if not request.user.has_perm('vote.delete_categorymodel'):
            return Response({'message': 'You do not have permission to access this resource.'}, status=403)
        return super().destroy(request, *args, **kwargs)
        

class CandidateViewSet(ModelViewSet):
    queryset = CandidateModel.objects.all().order_by('id')
    serializer_class = CandidateSerializer
    permission_classes=[CustomPermission]
    
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
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
       raise MethodNotAllowed(request.method, HTTP_405_METHOD_NOT_ALLOWED)

    
    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, HTTP_405_METHOD_NOT_ALLOWED)

    
    def list(self, request, *args, **kwargs):
        queryset = CategoryModel.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        
        for category in serializer.data:
            for candidate in category['candidates']:
                candidate['percentage'] = (self.queryset.filter(category=category['id'], candidate=candidate['id']).count() / len(category['candidates'])) * 100
        return Response(serializer.data)
    
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, HTTP_405_METHOD_NOT_ALLOWED)
