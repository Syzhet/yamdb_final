from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import (filters, generics, mixins, pagination, permissions,
                            status, viewsets)
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filter import TitleFilter
from .permissions import (AdminUserModerPermission, IsRoleAdmin,
                          OnlyAdminPermission, ReadOnly)
from .serializers import (AdminModerUsersSerializer, AdminUsersSerializer,
                          CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          TokenSerializer, UserSerializer)


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    permission_classes = [IsRoleAdmin | ReadOnly]
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    rating: int
    serializer_class = GenreSerializer
    permission_classes = [IsRoleAdmin | ReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='genre_slug'
    )
    def get_genre(self, request, slug):
        genre = self.get_object()
        serializer = GenreSerializer(genre)
        genre.delete()
        return Response(serializer.data, status=HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsRoleAdmin | ReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=HTTP_204_NO_CONTENT)


class CreateUser(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['username'] != 'me':
                serializer.save()
                user = get_object_or_404(
                    User,
                    email=serializer.validated_data['email']
                )
                token = default_token_generator.make_token(user)
                send_mail(
                    'Your invite code',
                    token,
                    settings.EMAIL_HOST_USER,
                    [serializer.validated_data['email'], ],
                    fail_silently=False,
                )
                return Response(serializer.validated_data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CreateToken(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
        }

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )
            if default_token_generator.check_token(
                    user,
                    serializer.validated_data['confirmation_code']):
                token = self.get_token(user)
                return Response(token, status=HTTP_200_OK)
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_400_BAD_REQUEST)


class AdminListCreateUser(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = AdminUsersSerializer
    permission_classes = (OnlyAdminPermission,)
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[AdminUserModerPermission]
    )
    def me(self, request):
        if request.method == 'GET':
            user = request.user
            serializer = AdminModerUsersSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        request.method == 'PATCH':
        username = request.user.username
        user = get_object_or_404(User, username=username)
        serializer = AdminModerUsersSerializer(
            user,
            request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
        | AdminUserModerPermission
        | ReadOnly
    ]
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        reviews = title.reviews.all()
        return reviews

    def create(self, request, *args, **kwargs):
        author = self.request.user
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        review_title = title.reviews.filter(author=author)
        if review_title.count() >= 1:
            return Response(
                'Лимит отзывов исчерпан',
                status=HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title_id=self.kwargs.get("title_id")
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого отзыва запрещено!')
        super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        if (
                user.role == 'admin'
                or user.role == 'moderator'
                or instance.author == user
        ):
            super(ReviewViewSet, self).perform_destroy(instance)
        else:
            raise PermissionDenied('Удаление чужого отзыва запрещено!')


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
        | AdminUserModerPermission
        | ReadOnly
    ]
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(
            author=self.request.user, review_id=review.id
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого коммента запрещено!')
        super(CommentsViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        user = self.request.user
        if (
                user.role == 'admin'
                or user.role == 'moderator'
                or instance.author == user
        ):
            super(CommentsViewSet, self).perform_destroy(instance)
        else:
            raise PermissionDenied('Удаление чужого коммента запрещено!')
