from django.contrib.auth.models import User
from rest.serializers import ProfileSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest.models import Profile, Project, Comment, Task, Document
from rest.serializers import (
    ProfileSerializer,
    ProjectSerializer,
    CommentsSerializer,
    TaskSerializer,
    ProjectInfoSerializer,
    ProfileCreateSerializer
)
from rest_framework import generics

class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


class UserCommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):     # filtering based on specific/ authenticated user 
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(author=user)
    

class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    # lookup_url_kwarg = 'comment_id' 
    # if in url you write comment_id instead of primary key then this will be used.
    # it will take the id int value given in url and compare it with the pk which is id
    # eg. path('comment/<int comment_id>',views.CommentListAPIView),


class ProjectInfoView(APIView):
    def get(self,request):
        projects = Project.objects.all()
        serializer = ProjectInfoSerializer({
            'projects' : projects,
            'count' : len(projects)
        })
        return Response(serializer.data)
    



# @api_view(["GET"])
# def project_info(request):
#     projects = Project.objects.all()
#     serializer = ProjectInfoSerializer({
#         'projects' : projects,
#         'count' : len(projects)
#     })
#     return Response(serializer.data)




################ Function Based Views #################

# @api_view(["GET"])
# def profile_list(request):
#     profiles = Profile.objects.all()
#     serializer = ProfileSerializer(profiles, many=True)
#     return Response(serializer.data)

# @api_view(["GET"])
# def profile_detail(request, pk):
#     # profile = Profile.objects.get(id=pk)
#     profile = get_object_or_404(Profile, pk=pk)
#     serializer = ProfileSerializer(profile, many=False)  # only one profile
#     return Response(serializer.data)

# @api_view(["GET"])
# def comment_list(request):
#     comments = Comment.objects.all()
#     serializer = CommentsSerializer(comments, many=True)
#     return Response(serializer.data)

# @api_view(["GET"])
# def comment_detail(request, pk):
#     # profile = Profile.objects.get(id=pk)
#     comment = get_object_or_404(Comment, pk=pk)
#     serializer = Comment(comment, many=False)  # only one profile
#     return Response(serializer.data)
