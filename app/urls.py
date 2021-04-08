from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/<int:id>/<slug>/', views.post_detail, name='post_detail'),
    path('post_create/', views.post_create, name='post_create'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('<int:id>/post_edit/', views.post_edit, name='post_edit'),
    path('<int:id>/post_delete/', views.post_delete, name='post_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
