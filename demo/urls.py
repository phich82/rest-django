from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from demo import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'test', views.DemoViewSet)

urlpatterns = [
    path('', views.demo_list),
    path('api-view', views.demo_list_api_view),
    path('<int:pk>', views.demo_detail),
    path('users', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('test', include(router.urls)),
]
