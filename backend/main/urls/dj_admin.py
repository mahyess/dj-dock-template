from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

import users.views as users_views
import admin_panel.views as admin_views


urlpatterns = [
    path("", admin_views.Dashboard.as_view(), name="dashboard"),
    path("", admin.site.urls),
]
