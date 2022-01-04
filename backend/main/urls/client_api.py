from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.api import (
    RegisterAPI,
    UserViewset,
    LoginAPI,
)

router = DefaultRouter()
urlpatterns = []

# -------------- auth app view sets --------------
urlpatterns += [
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("user/", UserViewset.as_view({"get": "retrieve"})),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
router.register("users", UserViewset)
# -------------- auth app view sets --------------

urlpatterns += router.urls

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version="v1",
        description="Doc for client API",
        contact=openapi.Contact(email="zephyrr2722@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path("", include(urlpatterns))],
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
