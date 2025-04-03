from django.db import models
from rest.Validators.custom_validator import validate_image
from rest.customfield import CustomPhoneNumberField
from rest.enum import RoleChoice,StatusChoice
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(
        default=True
    )  # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(
        default=True
    )  # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(
        default=False
    )  # this field we inherit from PermissionsMixin.

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Name")
    role = models.CharField(
        max_length=50, choices=RoleChoice.choices(), verbose_name="Professional Designation"
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
        return self.user.email


class Project(models.Model):
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name="manager_user")
    title = models.CharField(max_length=50)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    team_members = models.ManyToManyField(CustomUser, related_name="team")

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name="Description" , blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=StatusChoice.choices(), verbose_name="Task Status"
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
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="documents/")
    version = models.CharField(max_length=50,blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(verbose_name="Comment")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.email



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True) 
    
    def __str__(self):
        return f'{self.message}'
    
    
class Timeline(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.project.title}'