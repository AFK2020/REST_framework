from django.db import models
from django.contrib.auth import get_user_model
from rest.Validators.custom_validator import validate_image
from rest.customfield import CustomPhoneNumberField


User = get_user_model()

Role_Choices = {
    "d": "Developer",
    "qa": "Quality Assurance",
    "m": "Manager",
    "a": "System Architect",
    "n": "Networks Engineer",
}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Name")
    role = models.CharField(
        max_length=2, choices=Role_Choices, verbose_name="Professional Designation"
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        help_text="Max img size 5mb",
        validators=[validate_image],
        blank=True,
        null=True,
    )
    contact_number = CustomPhoneNumberField(blank=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    team_members = models.ManyToManyField(User)

    def __str__(self):
        return self.title


Status_Choice = {
    "o": "Open",
    "r": "Review",
    "w": "Working",
    "ar": "Awaiting Release",
    "wq": "Waiting QA",
}


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name="Description" , blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=Status_Choice, verbose_name="Task Status"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # assumption: one to many relation. one project can have many tasks but one task belong
    # to only one project
    assignee = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title


class Document(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to="documents/")
    version = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(verbose_name="Comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username
