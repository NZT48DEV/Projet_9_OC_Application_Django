"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import authentication.views
import flux.views
import posts.views
import reviews.views
import tickets.views
import userfollows.views
from authentication.views import CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", CustomLoginView.as_view(), name="welcome"),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("home/", flux.views.home, name="home"),
    path("image/upload/", tickets.views.image_upload, name="image_upload"),
    path("ticket/create", tickets.views.create_ticket, name="create_ticket"),
    path(
        "ticket/<int:ticket_id>", tickets.views.view_ticket, name="view_ticket"
    ),
    path(
        "ticket/<int:ticket_id>/delete",
        tickets.views.delete_ticket,
        name="delete_ticket",
    ),
    path(
        "ticket/<int:ticket_id>/update/",
        tickets.views.update_ticket,
        name="update_ticket",
    ),
    path(
        "review/create/",
        reviews.views.create_review_with_ticket,
        name="create_review_with_ticket",
    ),
    path(
        "ticket/<int:ticket_id>/review/",
        reviews.views.create_review_response,
        name="create_review_response",
    ),
    path(
        "review/<int:review_id>", reviews.views.view_review, name="view_review"
    ),
    path(
        "review/<int:review_id>/delete",
        reviews.views.delete_review,
        name="delete_review",
    ),
    path(
        "review/<int:review_id>/update/",
        reviews.views.update_review,
        name="update_review",
    ),
    path("posts/", posts.views.user_posts, name="user_posts"),
    path(
        "review_with_ticket/<int:review_id>/update/",
        reviews.views.update_review_with_ticket,
        name="update_review_with_ticket",
    ),
    path(
        "review_with_ticket/<int:review_id>/delete/",
        reviews.views.delete_review_with_ticket,
        name="delete_review_with_ticket",
    ),
    path(
        "subscriptions/", userfollows.views.subscriptions, name="subscriptions"
    ),
    path(
        "unfollow/<int:user_id>/", userfollows.views.unfollow, name="unfollow"
    ),
    path("search-users/", userfollows.views.search_users, name="search_users"),
    path(
        "block/<int:user_id>/", userfollows.views.block_user, name="block_user"
    ),
    path(
        "unblock/<int:user_id>/",
        userfollows.views.unblock_user,
        name="unblock_user",
    ),
    path(
        "block/search/",
        userfollows.views.block_user_search,
        name="block_user_search",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
