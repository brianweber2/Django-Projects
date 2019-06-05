from django.urls import path

from .views import BlogPostRudView, BlogPostAPIView


app_name = 'api_postings'
urlpatterns = [
    # path(r'(?P<pk>\d+)/', BlogPostRudView.as_view(), name='post-rud'),
    path('<int:pk>/', BlogPostRudView.as_view(), name='post-rud'),
    path('', BlogPostAPIView.as_view(), name='post-listcreate'),
]
