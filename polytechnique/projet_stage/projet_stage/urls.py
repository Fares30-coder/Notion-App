from django.contrib import admin
from django.urls import path, include
from notion_app.views import get_notion_pages, update_notion_page, MySecuredView, envoyer_video,recuperer_resultats
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
    path('admin/', admin.site.urls),
    path('notion-pages/', get_notion_pages, name='notion-pages'),
    path('notion-page/<str:page_id>/', update_notion_page, name='update-notion-page'),
    path('my-secured-view/', MySecuredView.as_view(), name='my-secured-view'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('envoyer-video/', envoyer_video, name='envoyer_video'),
    path('resultats/<int:video_id>/', recuperer_resultats, name='recuperer_resultats'),
]

