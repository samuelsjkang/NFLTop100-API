from django.db import models
from django.contrib.auth.models \
    import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    # Creates and saves a user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User did not provide email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Creates a superuser
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# Player Model
class Player(models.Model):
    name = models.CharField(max_length=255)
    ranking = models.IntegerField()
    team = models.ManyToManyField('Team')
    position = models.ManyToManyField('Position')
    last_ranking = models.IntegerField()
    youtube_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


# Team Model
class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Position Model
class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
