from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminListCreateUser, CategoryViewSet, CommentsViewSet,
                    CreateToken, CreateUser, GenreViewSet, ReviewViewSet,
                    TitleViewSet)

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(r'', AdminListCreateUser)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

SIGNUP_TOKEN_URLS = [
    path('signup/', CreateUser.as_view()),
    path('token/', CreateToken.as_view()),
]

urlpatterns = [
    path('v1/users/', include(router.urls)),
    path('v1/auth/', include(SIGNUP_TOKEN_URLS)),
    path('v1/', include(router.urls)),

]
