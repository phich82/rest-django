from django.urls import path
from demo import views
from demo.views import DemoListAPIView

urlpatterns = [
    # path('', views.demo_list),
    # path('api-view', views.demo_list_api_view),
    # path('<int:pk>', views.demo_detail),
    # path('users', views.UserList.as_view()),
    # path('users/<int:pk>', views.UserDetail.as_view()),

    path('', views.DemoCreateListAPIView.as_view()),
    path('<int:pk>', views.DemoDetailUpdateDeleteAPIView.as_view()),

    path('list', views.DemoListAPIView.as_view()),
    path('create', views.DemoCreateAPIView.as_view()),
    path('<int:pk>/detail', views.DemoDetailAPIView.as_view()),
    path('<int:pk>/update', views.DemoUpdateAPIView.as_view()),
    path('<int:pk>/delete', views.DemoDeleteAPIView.as_view()),
]
