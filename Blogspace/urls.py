from django.urls import path, include

urlpatterns = [
    path('', include("blog_app.urls")),
]
