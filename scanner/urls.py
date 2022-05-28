from django.urls import path
from scanner import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('scans/', views.scan_list),
    path('scans/<int:id>', views.scan_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)