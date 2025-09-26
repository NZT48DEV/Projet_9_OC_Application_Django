"""
Vues pour la gestion des abonnements et blocages utilisateurs.
"""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import UserBlock, UserFollows

User = get_user_model()


@login_required
def subscriptions(request):
    """
    Page des abonnements et blocages.

    - Si méthode POST : permet de s’abonner à un utilisateur via son username.
    - Si méthode GET : affiche mes abonnements, mes abonnés et ma liste de blocage.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user_to_follow = User.objects.get(username=username)
            if user_to_follow == request.user:
                messages.error(
                    request, "❌ Vous ne pouvez pas vous abonner à vous-même."
                )
            else:
                UserFollows.objects.get_or_create(
                    user=request.user, followed_user=user_to_follow
                )
                messages.success(
                    request,
                    f"✅ Vous êtes abonné à {user_to_follow.username}.",
                )
        except User.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
        return redirect("subscriptions")

    following = UserFollows.objects.filter(user=request.user).select_related(
        "followed_user"
    )

    followers = UserFollows.objects.filter(
        followed_user=request.user
    ).select_related("user")

    blocked_list = UserBlock.objects.filter(user=request.user).select_related(
        "blocked_user"
    )

    return render(
        request,
        "userfollows/subscriptions.html",
        {
            "following": following,
            "followers": followers,
            "blocked_list": blocked_list,
        },
    )


@login_required
def unfollow(request, user_id):
    """
    Se désabonner d’un utilisateur.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    link = UserFollows.objects.filter(
        user=request.user, followed_user=user_to_unfollow
    )

    if link.exists():
        link.delete()
        messages.success(
            request,
            f"✅ Vous vous êtes désabonné de {user_to_unfollow.username}.",
        )

    return redirect("subscriptions")


@login_required
def search_users(request):
    """
    Recherche d’utilisateurs pour l’abonnement ou le blocage (autocomplete).

    Paramètres GET :
    - q : début du nom d’utilisateur.
    - type : "follow" ou "block" (défaut = follow).

    Retour :
    - JSON contenant max 5 résultats (id, username).
    """
    query = request.GET.get("q", "").strip()
    search_type = request.GET.get("type", "follow")  # "follow" ou "block"
    results = []

    if query:
        users = User.objects.filter(username__istartswith=query).exclude(
            id=request.user.id
        )

        already_blocked = UserBlock.objects.filter(
            user=request.user
        ).values_list("blocked_user_id", flat=True)

        if search_type == "follow":
            already_following = UserFollows.objects.filter(
                user=request.user
            ).values_list("followed_user_id", flat=True)

            users = users.exclude(id__in=already_following).exclude(
                id__in=already_blocked
            )

        elif search_type == "block":
            users = users.exclude(id__in=already_blocked)

        results = list(users.values("id", "username")[:5])

    return JsonResponse(results, safe=False)


@login_required
def block_user(request, user_id):
    """
    Bloquer un utilisateur :
    - Supprime l’abonnement réciproque s’il existe.
    - Ajoute l’utilisateur à la liste des bloqués.
    """
    target = get_object_or_404(User, id=user_id)

    if target == request.user:
        messages.error(request, "Vous ne pouvez pas vous bloquer vous-même.")
        return redirect("subscriptions")

    UserFollows.objects.filter(
        user=target, followed_user=request.user
    ).delete()
    UserFollows.objects.filter(
        user=request.user, followed_user=target
    ).delete()

    UserBlock.objects.get_or_create(user=request.user, blocked_user=target)

    messages.success(request, f"✅ Vous avez bloqué {target.username}.")
    return redirect("subscriptions")


@login_required
def unblock_user(request, user_id):
    """
    Débloquer un utilisateur.
    """
    block = get_object_or_404(
        UserBlock, user=request.user, blocked_user_id=user_id
    )
    block.delete()
    messages.success(request, "✅ Utilisateur débloqué avec succès.")
    return redirect("subscriptions")


@login_required
def block_user_search(request):
    """
    Bloquer un utilisateur via un formulaire (POST avec username).
    - Supprime les abonnements existants.
    - Ajoute l’utilisateur à la liste de blocage.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user_to_block = User.objects.get(username=username)
            if user_to_block == request.user:
                messages.error(
                    request, "❌ Vous ne pouvez pas vous bloquer vous-même."
                )
            else:
                UserFollows.objects.filter(
                    user=user_to_block, followed_user=request.user
                ).delete()

                UserFollows.objects.filter(
                    user=request.user, followed_user=user_to_block
                ).delete()

                UserBlock.objects.get_or_create(
                    user=request.user, blocked_user=user_to_block
                )
                messages.success(
                    request, f"🚫 Vous avez bloqué {user_to_block.username}."
                )
        except User.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")

    return redirect("subscriptions")
