from django.urls import path
from . import views

app_name = 'KHUgle'         #KHUgle이라는 url 이름을 선언하여 url mapping에 사용한다.

urlpatterns = [
    path('', views.index, name='index'),                      #KHUgle의 인덱스 페이지 --> view로 매핑
    path('<int:post_id>/', views.detail, name='detail'),       #KHUgle의 post detail 페이지
    path('post/create', views.post_create, name='post_create'),
    path('post/modify/<int:post_id>/', views.post_modify, name='post_modify'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
]