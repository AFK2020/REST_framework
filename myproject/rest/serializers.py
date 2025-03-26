from rest_framework import serializers
from .models import Profile,Project,Task,Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = (
            'user',
            'role',
            'contact_number',
        )
    # def validate_name(self,value):
    #     print()
    #     if len(value) < 5 :
    #         raise serializers.ValidationError("Name must be more than 5 characters")
    #     return value


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'user',
            'role',
            'contact_number',
        )


class ProjectSerializer(serializers.ModelSerializer):
    # comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'start_date',
        )
    def validate_title(self,value):
        if len(value) < 10:
            raise serializers.ValidationError("Name must be more than 10 characters")
        return value


class TaskSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer()
    class Meta:
        model = Task
        fields = (
                'title', 
                'description', 
                'project',
                )

class CommentsSerializer(serializers.ModelSerializer): 
    # project = ProjectSerializer()     # to get whole project dictionary from ProjectSerializer
    project_title = serializers.CharField(source='project.title')   #to write only this field instead of a nested dictionary.
    # to compare, see how different task field and this look on browser
    project_date = serializers.DateField(source='project.start_date')
    author_name= serializers.CharField(source = 'author.username')
    task = TaskSerializer()

    class Meta:
        model = Comment
        fields = (
            "text",
            "author_user",
            "create_date",
            "task", 
            "project_title",
            "project_date",

            )


class ProjectInfoSerializer(serializers.Serializer):
    # get all the projects and count of projects

    projects = ProjectSerializer(many=True)
    count = serializers.IntegerField()