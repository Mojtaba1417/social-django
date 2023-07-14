from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/detail/<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>', views.PostUpdateView.as_view(), name='update_post'),
    path('post/create/', views.PostCreateView.as_view(), name='create_post'),
    path('reply/<int:post_id>/<int:comment_id>/', views.PostReplyView.as_view(), name='add_reply'),
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='post_like')
]