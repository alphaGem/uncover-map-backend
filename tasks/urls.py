from django.urls import path 
from . import views

# define the urls
urlpatterns = [
    path('import/', views.ImportView.as_view()),
    path('export/', views.ExportView.as_view()),
    path('info/<int:pk>/', views.info_detail),
    path('query/',views.query),
    path('pending_query/',views.pending_query),
    path('item_count/',views.item_count),
    path('suggest/',views.AdminSuggestView.suggest),
    path('get_token/',views.CustomAuthToken.as_view()),
]
