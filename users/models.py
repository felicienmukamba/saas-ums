from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# ====================================================================
# 1. Custom User Manager
# ====================================================================

class CustomUserManager(BaseUserManager):
    """
    Manager personnalisé pour le modèle User où l'email est le champ
    d'identification unique plutôt que le username.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'adresse email doit être fournie.'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser doit avoir is_superuser=True.'))

        # Assurez-vous qu'un rôle par défaut est défini pour le superuser
        extra_fields.setdefault('role', 'ADMIN')

        return self.create_user(email, password, **extra_fields)

# ====================================================================
# 2. Custom User Model
# ====================================================================

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur Système'),
        ('RECTORAT', 'Rectorat/Direction'),
        ('FINANCE', 'Service Financier'),
        ('ACADEMIC', 'Service Académique/Secrétariat'),
        ('PROFESSOR', 'Professeur/Enseignant'),
        ('STUDENT', 'Étudiant'),
        ('STAFF', 'Personnel Support'),
    )


    # Champs personnalisés
    email = models.EmailField(_('Adresse email'), unique=True)
    first_name = models.CharField(_('Prénom'), max_length=150, blank=True)
    last_name = models.CharField(_('Nom'), max_length=150, blank=True)
    avatar = models.ImageField(
        _('Avatar'), 
        upload_to='avatars/', 
        null=True, 
        blank=True
    )
    role = models.CharField(
        _('Rôle'), 
        max_length=50, 
        choices=ROLE_CHOICES, 
        default='STUDENT'
    )
    
    # Rendre le champ 'username' non obligatoire/unique si on utilise l'email comme identifiant
    username = models.CharField(
        _('Nom d\'utilisateur'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role'] 
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')

    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def get_role_display(self):
        """Retourne l'affichage du rôle."""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role})' if self.first_name and self.last_name else self.email

