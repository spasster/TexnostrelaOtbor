from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, avatar=None):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=self.normalize_email(email), avatar=avatar)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, avatar=None):
        user = self.create_user(email=email, password=password, avatar=avatar)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):  # Добавлен PermissionsMixin
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Позволяет пользователю иметь определённые права (обычно True для суперюзеров)."""
        return self.is_superuser  # Можно изменить логику под свои нужды

    def has_module_perms(self, app_label):
        """Позволяет пользователю видеть приложение в админке."""
        return self.is_superuser  # Можно сделать более гибкую проверку
