from django.conf.urls import url

from django.urls import path

from . import views

app_name = 'lg'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('statistics/city/', views.statistics_city_view, name='stats'),
    path('statistics/sells/', views.statistics_sells_view, name='stats_sells'),
    path('add_article/', views.add_article, name='add_article'),
    path('boughts/<int:id>/', views.buying_view.as_view()),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
