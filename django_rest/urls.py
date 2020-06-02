"""settingsdjango_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django_rest import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Django REST API",
      default_version='v1',
      description="Home project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Swagger
    path(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Employees
    path('employee/', views.EmployeesCreateAPIView.as_view(), name='employee_create'),
    path('employee/<int:pk>/', views.EmployeeAPIView.as_view(), name='employee'),

    # Departments
    path('department/', views.DepartmentCreateAPIView.as_view(), name='department_create'),
    path('department/<int:pk>/', views.DepartmentAPIView.as_view(), name='department'),

    # Projects
    path('project/', views.ProjectCreateAPIView.as_view(), name='project_create'),
    path('project/<int:pk>/', views.ProjectAPIView.as_view(), name='project'),

    # Tasks
    path('task/', views.TaskCreateAPIView.as_view(), name='task_create'),
    path('task/<int:pk>/', views.TaskAPIView.as_view(), name='task'),

]
