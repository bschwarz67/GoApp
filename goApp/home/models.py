#need to put in username for create
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from board.models import Game
class PlayerManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class Player(AbstractUser):
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="addUserToGame", null=True)
	color = models.BooleanField(default=True)	#TRUE = white, FALSE = BLACK
	turn = models.BooleanField(default=True) #TRUE = the players turn, FALSE = not the players turn
	lastOutOfGameAction = models.DateTimeField(auto_now=True)
	objects = PlayerManager()
