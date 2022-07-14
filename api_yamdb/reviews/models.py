from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES_CHOICES = [
    (USER, 'user'),
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
]


class User(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=150)
    email = models.EmailField('Электронная почта', unique=True)
    password = models.CharField('Пароль', max_length=100, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        choices=ROLES_CHOICES,
        max_length=100,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'token': str(refresh.access_token),
        }


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveIntegerField(verbose_name='Год', db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre, through='Genretitle', verbose_name='Жанр'
    )
    description = models.CharField(
        max_length=256, blank=True, verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genretitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genres'
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(verbose_name='Рейтинг')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        verbose_name = 'Отзывы'


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарии к отзывам'
