from django.urls import path, include

from .views import MatriculantSignupView, MatriculantAppIndex

urlpatterns = [
    path('', MatriculantAppIndex.as_view(), name='matriculant_app_index'),
    path('signup/', MatriculantSignupView.as_view(), name='matriculant_signup'),
]