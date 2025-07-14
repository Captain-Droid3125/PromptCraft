from django.urls import path
from .views import index, ImageGenerationView

urlpatterns = [
    path('', index, name='index'),
    path('api/generate-image/', ImageGenerationView.as_view(), name='generate_image'),
]