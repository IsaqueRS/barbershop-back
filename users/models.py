from django.db import models
from django.contrib.auth.models import AbstractUser
from barber_shop.models import Company

# Create your models here.
TYPE_USER = (
    ('cliente', 'Cliente'),
    ('barbeiro', 'Barbeiro'),
    ('dono', 'Dono')
)


class UserProfile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField('Nome', max_length=40, null=True, blank=True)
    type = models.CharField('Tipo do usuário', choices=TYPE_USER, max_length=50, default='cliente')
    owner_company = models.ForeignKey(Company, related_name="company_owner", verbose_name="Gerente de",
                                      on_delete=models.SET_NULL, blank=True, null=True)
    is_owner = models.BooleanField('Dono de alguma barbearia?', default=False)
    full_name = models.CharField("Nome Completo", max_length=512, blank=True, null=True)
    email = models.EmailField('E-mail', unique=True)
    image = models.ImageField('Foto de perfil', blank=True, null=True)
    description = models.TextField('Descrição de usuário', max_length=500, default='', blank=True, null=True)
    token_google = models.TextField('Token', default='', max_length=500)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user_profiles",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user_profiles",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username


class Barbers(models.Model):
    company = models.ForeignKey(Company, verbose_name='Barbearia', on_delete=models.CASCADE)
    barber = models.ForeignKey(UserProfile, verbose_name='Barbeiro', on_delete=models.CASCADE)
    password = models.CharField('Senha', max_length=12, default='')
    profile_photo = models.ImageField('Foto do barbeiro', help_text='(opcional)', blank=True, null=True)
    email_barber = models.EmailField('Email do barbeiro', unique=True)

    def __str__(self):
        return str(f"{self.company} - {self.barber} - {self.email_barber}")

    class Meta:
        verbose_name = 'Barbeiro'
        verbose_name_plural = 'Barbeiros'
