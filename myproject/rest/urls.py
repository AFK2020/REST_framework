from django.urls import path
from rest import views


urlpatterns = [
    path('profile/',views.ProfileListAPIView.as_view()),
    path('profile/create/',views.ProfileListCreateAPIView.as_view()),
    path('profile/<int:pk>', views.ProfileDetailAPIView.as_view),
    path('project/info', views.ProjectInfoView.as_view()),
    path('comment/',views.CommentListAPIView.as_view()),
    path('user-comment/',views.UserCommentListAPIView.as_view()),


]
