# userfollows/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import UserFollows, UserBlock
from django.http import JsonResponse

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

    following = UserFollows.objects.filter(user=request.user).select_related("followed_user")
    followers = UserFollows.objects.filter(followed_user=request.user).select_related("user")
    blocked_list = UserBlock.objects.filter(user=request.user).select_related("blocked_user")

    return render(request, "userfollows/subscriptions.html", {
        "following": following,
        "followers": followers,
        "blocked_list": blocked_list,  # ✅ nom cohérent avec le template
    })


@login_required
def unfollow(request, user_id):
    """Se désabonner d’un utilisateur"""
    user_to_unfollow = get_object_or_404(User, id=user_id)
    link = UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow)
    if link.exists():
        link.delete()
        messages.success(request, f"✅ Vous vous êtes désabonné de {user_to_unfollow.username}.")
    return redirect("subscriptions")


@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()
    search_type = request.GET.get("type", "follow")  # follow ou block
    results = []

    if query:
        users = User.objects.filter(username__istartswith=query)

        # exclut soi-même
        users = users.exclude(id=request.user.id)

        if search_type == "follow":
            # exclut ceux que je suis déjà
            already_following = UserFollows.objects.filter(
                user=request.user
            ).values_list("followed_user_id", flat=True)

            # exclut aussi ceux que j’ai bloqués
            already_blocked = UserBlock.objects.filter(
                user=request.user
            ).values_list("blocked_user_id", flat=True)

            users = users.exclude(id__in=already_following).exclude(id__in=already_blocked)

        elif search_type == "block":
            # exclut ceux que j’ai déjà bloqués
            already_blocked = UserBlock.objects.filter(
                user=request.user
            ).values_list("blocked_user_id", flat=True)

            users = users.exclude(id__in=already_blocked)

        results = list(users.values("id", "username")[:5])  # limite à 5 résultats

    return JsonResponse(results, safe=False)



@login_required
def block_user(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if target == request.user:
        messages.error(request, "Vous ne pouvez pas vous bloquer vous-même.")
        return redirect("subscriptions")

    # Supprimer des abonnés si nécessaire
    UserFollows.objects.filter(user=target, followed_user=request.user).delete()
    # Supprimer si on le suit déjà
    UserFollows.objects.filter(user=request.user, followed_user=target).delete()

    UserBlock.objects.get_or_create(user=request.user, blocked_user=target)

    messages.success(request, f"✅ Vous avez bloqué {target.username}.")
    return redirect("subscriptions")


@login_required
def unblock_user(request, user_id):
    """Débloquer un utilisateur"""
    block = get_object_or_404(UserBlock, user=request.user, blocked_user_id=user_id)
    block.delete()
    messages.success(request, "✅ Utilisateur débloqué avec succès.")
    return redirect("subscriptions")


@login_required
def block_user_search(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user_to_block = User.objects.get(username=username)
            if user_to_block == request.user:
                messages.error(request, "❌ Vous ne pouvez pas vous bloquer vous-même.")
            else:
                # Supprimer s'il est abonné à moi
                UserFollows.objects.filter(user=user_to_block, followed_user=request.user).delete()
                # Supprimer si je le suis déjà
                UserFollows.objects.filter(user=request.user, followed_user=user_to_block).delete()

                UserBlock.objects.get_or_create(user=request.user, blocked_user=user_to_block)
                messages.success(request, f"🚫 Vous avez bloqué {user_to_block.username}.")
        except User.DoesNotExist:
            messages.error(request, "Utilisateur introuvable.")
    return redirect("subscriptions")

