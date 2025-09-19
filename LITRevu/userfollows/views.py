# userfollows/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import UserFollows
from django.http import JsonResponse
from django.db.models import Q

User = get_user_model()


@login_required
def subscriptions(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow == request.user:
                messages.error(request, "❌ Vous ne pouvez pas vous abonner à vous-même.")
            else:
                UserFollows.objects.get_or_create(
                    user=request.user,
                    followed_user=user_to_follow
                )
                messages.success(request, f"✅ Vous êtes abonné à {user_to_follow.username}.")
        except User.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
        return redirect("subscriptions")

    # Abonnements de l’utilisateur
    following = UserFollows.objects.filter(user=request.user)
    # Abonnés de l’utilisateur
    followers = UserFollows.objects.filter(followed_user=request.user)

    return render(request, "userfollows/subscriptions.html", {
        "following": following,
        "followers": followers,
    })


@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    link = UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow)
    if link.exists():
        link.delete()
        messages.success(request, f"✅ Vous vous êtes désabonné de {user_to_unfollow.username}.")
    return redirect("subscriptions")

@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        # récupère tous les users qui matchent la recherche
        users = User.objects.filter(username__icontains=query)

        # on exclut soi-même
        users = users.exclude(id=request.user.id)

        # on exclut ceux qu’on suit déjà
        already_following = UserFollows.objects.filter(user=request.user).values_list("followed_user_id", flat=True)
        users = users.exclude(id__in=already_following)

        results = list(users.values("id", "username")[:10])  # limite à 10 résultats

    return JsonResponse(results, safe=False)