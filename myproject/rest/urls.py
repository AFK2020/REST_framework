from django.urls import path,include
from rest import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = routers.DefaultRouter()
router.register(r'project', viewset=views.ProjectAPIView, basename='project')
router.register(r'task', viewset=views.TaskAPIView, basename='task')
router.register(r'document', viewset=views.DocumentAPIView, basename='document')
router.register(r'notification', viewset=views.NotificationAPIView, basename='notifcation')
router.register(r'comment', viewset=views.CommentAPIView, basename='comment')
router.register(r'timeline', viewset=views.TimelineAPIView, basename='timeline')


urlpatterns = [
    path('',include(router.urls)),
    path('register/',views.UserRegistrationView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    # path('project/create/',views.ProjectListCreateAPIView.as_view()),

    # path('profile/',views.ProfileListAPIView.as_view()),
    # path('profile/create/',views.ProfileListCreateAPIView.as_view()),
    # path('profile/<int:pk>', views.ProfileDetailAPIView.as_view),
    # path('project/info', views.ProjectInfoView.as_view()),
    # path('comment/',views.CommentListAPIView.as_view()),
    # path('user-comment/',views.UserCommentListAPIView.as_view()),

]
