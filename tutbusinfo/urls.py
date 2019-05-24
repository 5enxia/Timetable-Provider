from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    #table
    path('<str:station_name>/',views.tableindex,name='tableindex'),
    path('<str:station_name>/<str:table_name>/',views.table,name='table'),
    ]