from rest_framework import serializers

from rest.enum import RoleChoice

from .models import (
    Comment,
    CustomUser,
    Document,
    Notification,
    Profile,
    Project,
    Task,
    Timeline,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email",)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "role",
            "contact_number",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, required=True
    )

    role = serializers.CharField()
    contact_number = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "role",
            "contact_number",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        email = data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User email already exists.")

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"Error": "Passwords must match."})

        role = data.get("role")

        if role not in (r.value for r in RoleChoice):
            raise serializers.ValidationError(
                {"Invalid Role": "Role must be from the specified roles"}
            )

        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        Profile.objects.create(
            user=user,
            role=validated_data["role"],
            contact_number=validated_data["contact_number"],
        )
        return validated_data


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "manager", "description", "start_date", "end_date")

    def validate(self, data):
        title = data.get("title")
        if len(title) < 5 :
            raise serializers.ValidationError("Name must be more than 5 characters")

        manager = data.get("manager")
        print(data.get("manager"))

        user = CustomUser.objects.filter(email=manager)
        if manager != user:
            raise serializers.ValidationError("Error: Project must be assigned to an existing user")

        start = data.get('start_date')
        end = data.get("end_date")
        if start > end:
            raise serializers.ValidationError("Start Date can not be later than end date")

        return data

    def create(self, validated_data):
        project = Project.objects.create(
            title=validated_data["title"],
            manager=validated_data["manager"],
            description=validated_data["description"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
        )
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.description = validated_data["description"]
        instance.start_date = validated_data["start_date"]
        instance.end_date = validated_data["end_date"]
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("title", "description", "project", "status", "assignee")

    def create(self, validated_data):
        task = Task.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            status=validated_data.get("status", None),
            project=validated_data["project"],
        )
        return task


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "name",
            "description",
            "version",
            "file",
            "project",
        )

    def create(self, validated_data):
        document = Document.objects.create(
            name=validated_data["name"],
            description=validated_data.get("description", ""),
            file=validated_data["file"],
            version=validated_data.get("version", ""),
            project=validated_data["project"],
        )
        return document

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.description = validated_data.get("description", "")
        instance.file = validated_data["file"]
        instance.version = validated_data.get("version", "")
        instance.project = validated_data["project"]
        instance.save()

        return instance


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "text",
            "author",
            "task",
            "project",
        )
        action_fields = {"list": {"fields": ("create_date")}}

        def create(self, validated_data):
            comment = Comment.objects.create(
                text=validated_data["text"],
                author=validated_data["author"],
                task=validated_data["task"],
                project=validated_data["project"],
            )
            return comment


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "user",
            "message",
            "is_read",
            "project",
        )


class TimelineSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="project.title")

    class Meta:
        model = Timeline
        fields = ("project_title", "timestamp")


# class CommentsSerializer(serializers.ModelSerializer):
#     # project = ProjectSerializer()     # to get whole project dictionary from ProjectSerializer
#     project_title = serializers.CharField(
#         source="project.title"
#     )  # to write only this field instead of a nested dictionary.
#     # to compare, see how different task field and this look on browser
#     project_date = serializers.DateField(source="project.start_date")
#     author_name = serializers.CharField(source="author.email")
#     task = TaskSerializer()

#     class Meta:
#         model = Comment
#         fields = (
#             "text",
#             "author_name",
#             "task",
#             "project_title",
#             "project_date",
#             "create_date",
#         )
# def create(self, validated_data):
#     author_email = validated_data.get('author_name')
#     print(author_email)
#     author = CustomUser.objects.get(email=author_email)

#     task_data = validated_data.get('task')
#     task = Task.objects.get(id=task_data.get('id'))

#     project_title = validated_data.get('project_title')
#     project = Project.objects.filter(title = project_title)

#     comment = Comment.objects.create(
#         text=validated_data['text'],
#         author=author,
#         task=task,
#         project=project
#     )
#     return comment


# class ProjectInfoSerializer(serializers.Serializer):
#     # get all the projects and count of projects

#     projects = ProjectSerializer(many=True)
#     count = serializers.IntegerField()
