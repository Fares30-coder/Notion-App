from django.contrib import admin
from django.urls import path, include
from notion_app.views import notion_integration, update_notion_page, MySecuredView,get_models_view, audio_transcription_view, home, transcribe_video, create_entity
from rest_framework import permissions
from drf_yasg.views import get_schema_view

from drf_yasg import openapi



schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API endpoints documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
     path('notion-integration/', notion_integration, name='notion_integration'),
    path('notion-page/<str:page_id>/', update_notion_page, name='update-notion-page'),
    path('my-secured-view/', MySecuredView.as_view(), name='my-secured-view'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #path('envoyer-video/', envoyer_video, name='envoyer_video'),
    #path('resultats/<int:video_id>/', recuperer_resultats, name='wrecuperer_resultats'),
    path('api/get-models/', get_models_view, name='get_models'),
    path('api/transcribe-audio/', audio_transcription_view, name='transcribe_audio'),
    path('api/transcribe-video/', transcribe_video, name='transcribe-video'),
    path('create-entity/', create_entity, name='create_entity'),
]

