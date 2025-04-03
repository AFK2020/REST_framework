from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from rest.enum import RoleChoice
from rest.models import (
    Comment,
    Document,
    Notification,
    Profile,
    Project,
    Task,
    Timeline,
)
from rest.permissions import IsManager
from rest.serializers import (
    CommentsSerializer,
    DocumentSerializer,
    NotificationSerializer,
    ProjectCreateSerializer,
    TaskSerializer,
    TimelineSerializer,
    UserRegisterSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProjectAPIView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def get_queryset(self):
        if self.request.user.profile.role == RoleChoice.MANAGER.value:
            return self.queryset.filter(manager=self.request.user)

        if self.request.user.profile.role in [
            "qa",
            "developer",
            "system architect",
            "networks engineer",
        ]:
            return self.queryset.filter(team_members__in=[self.request.user])

    def destroy(self, request, pk=None):
        project = Project.objects.get(id=pk)

        if self.request.user == project.manager:
            self.perform_destroy(project)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class TaskAPIView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.request.user.profile.role == RoleChoice.MANAGER.value:
            return self.queryset.filter(project__manager=self.request.user)

    def destroy(self, request, pk=None):
        task = Task.objects.get(id=pk)
        if self.request.user == task.project.manager:
            self.perform_destroy(task)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        project_id = self.request.data.get("project")
        project = Project.objects.get(id=project_id)
        if self.request.user != project.manager:
            return Response(
                {
                    "Auth Error": "Managers can only create tasks for their own projects."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        task_id = kwargs.get("pk")
        task = Task.objects.get(id=task_id)
        try:
            if request.user != task.project.manager:
                return Response(
                    {
                        "Auth Error": "Managers can only updates tasks for their own projects."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Exception:
            return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["PATCH"])
    def assign_team_member(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
            assign = request.data.get("assignee")
            if not assign:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            member = Profile.objects.get(id=assign)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user != task.project.manager:
            return Response(
                {"Auth Error": "Managers can only assign tasks of their own projects."},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.assignee = member
        task.save()
        return Response(
            {"Detail": "Member assigned to project"}, status=status.HTTP_200_OK
        )


class DocumentAPIView(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        project_id = self.request.data.get("project")
        result = self.queryset.filter(project=project_id)
        return result

    def retrieve(self, request, *args, **kwargs):
        document_id = kwargs.get("pk")
        try:
            instance = self.queryset.get(pk=document_id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception:
            return Response(
                {
                    "Error": "No such Document exsist for the manager trying to access it. "
                    "Managers can only access documents for projects that they manage"
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class NotificationAPIView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=True, methods=["PATCH", "PUT"])
    def read_notification(self, request, pk=None):
        try:
            notifcation = Notification.objects.get(pk=pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user != notifcation.user:
            return Response(
                {"Auth Error": "Users can only access their notifications"},
                status=status.HTTP_403_FORBIDDEN,
            )

        notifcation.is_read = True
        notifcation.save()
        return Response(
            {"Detail": "Notification marked as Read"}, status=status.HTTP_200_OK
        )


class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    def get_queryset(self):
        project_id = self.request.data.get("project")
        result = self.queryset.filter(project=project_id)
        return result

    def retrieve(self, request, *args, **kwargs):
        comments_id = kwargs.get("pk")
        try:
            instance = self.queryset.get(pk=comments_id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception:
            return Response(
                {
                    "Error": "No comment exsist for the project that user is trying to access. "
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class TimelineAPIView(viewsets.ModelViewSet):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer


"""
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


@api_view(["GET"])
def project_info(request):
    projects = Project.objects.all()
    serializer = ProjectInfoSerializer({
        'projects' : projects,
        'count' : len(projects)
    })
    return Response(serializer.data)


############### Function Based Views #################

@api_view(["GET"])
def profile_list(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def profile_detail(request, pk):
    # profile = Profile.objects.get(id=pk)
    profile = get_object_or_404(Profile, pk=pk)
    serializer = ProfileSerializer(profile, many=False)  # only one profile
    return Response(serializer.data)

@api_view(["GET"])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentsSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def comment_detail(request, pk):
    # profile = Profile.objects.get(id=pk)
    comment = get_object_or_404(Comment, pk=pk)
    serializer = Comment(comment, many=False)  # only one profile
    return Response(serializer.data)
"
"""
