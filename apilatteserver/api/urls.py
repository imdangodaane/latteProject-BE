from django.urls import include, path
from rest_framework import routers
from .authentication import views as authen_views
from .database.items import views as db_views
from .article import views as article_views

router = routers.DefaultRouter()
# router.register(r'authentication', authen_views.LoginViewSet)
# router.register(r'register', authen_views.RegisterViewSet)

urlpatterns = [
    # ROUTER URLS
    path('', include(router.urls)),
    # AUTHENTICATION URLS
    path('authentication/login', authen_views.LoginCheck.as_view()),
    # REGISTER URLS
    path('register', authen_views.RegisterView.as_view()),
    # DATABASE URLS
    path('database/items', db_views.ItemsList.as_view()),
    # ARTICLE URLS
    path('article/all', article_views.GetAllArticles.as_view()),
    path('article/new', article_views.CreateArticle.as_view()),
    path('article/<int:id>', article_views.ArticleById.as_view()),
    path('article/<slug:slug>', article_views.ArticleBySlug.as_view()),
    path('article/<int:id>/setarticleoncarousel', article_views.SetArticleOnCarousel.as_view()),
]