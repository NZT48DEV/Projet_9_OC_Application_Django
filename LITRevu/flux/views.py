"""
Vues pour la gestion du flux principal (home) de l'application.
"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from reviews.models import Review
from tickets.models import Ticket
from userfollows.models import UserBlock, UserFollows


@login_required
def home(request):
    """
    Vue principale du flux utilisateur avec support du scroll infini.

    Fonctionnalités :
    - Filtrage des tickets (tous les tickets ou seulement ceux des abonnements).
    - Exclusion des tickets créés par des utilisateurs ayant bloqué l’utilisateur courant.
    - Préchargement des critiques associées aux tickets.
    - Pagination avec gestion AJAX pour l'infinite scroll.
    - Renvoie uniquement un fragment HTML lors des requêtes AJAX.
    """
    # Gestion du filtre
    if "filter" in request.GET:
        request.session["filter_mode"] = request.GET["filter"]

    filter_mode = request.session.get("filter_mode", "following")

    # Utilisateurs qui m’ont bloqué
    blocked_me = UserBlock.objects.filter(
        blocked_user=request.user
    ).values_list("user_id", flat=True)

    # Utilisateurs que j’ai bloqués
    i_blocked = UserBlock.objects.filter(
        user=request.user
    ).values_list("blocked_user_id", flat=True)

    # Récupération des tickets en fonction du filtre
    if filter_mode == "all":
        tickets = Ticket.objects.exclude(user_id__in=blocked_me).exclude(user_id__in=i_blocked)
    else:
        followed_users = UserFollows.objects.filter(
            user=request.user
        ).values_list("followed_user", flat=True)

        tickets = (
            Ticket.objects.filter(user__in=list(followed_users) + [request.user.id])
            .exclude(user_id__in=blocked_me)
            .exclude(user_id__in=i_blocked)
            .order_by("-time_created", "-id")
            .distinct()
        )

    # Optimisations des requêtes
    tickets = (
        tickets.select_related("user")
        .prefetch_related("review_set")
        .order_by("-time_created", "-id")
    )

    # Tickets déjà critiqués par l'utilisateur
    reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user).values_list(
            "ticket_id", flat=True
        )
    )

    # Pagination
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(tickets, 5)

    # Si la page demandée est trop grande → retour vide (évite doublons)
    if page_number > paginator.num_pages:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"html": "", "has_next": False})
        page_number = paginator.num_pages  # fallback si URL = ?page=999

    page_obj = paginator.get_page(page_number)

    # Requête AJAX → retour HTML partiel
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "flux/partials/_tickets_list.html",
            {"tickets": page_obj, "reviewed_ticket_ids": reviewed_ticket_ids},
            request=request,
        )
        return JsonResponse({"html": html, "has_next": page_obj.has_next()})

    # Requête classique → rendu complet
    return render(
        request,
        "flux/home.html",
        {
            "tickets": page_obj,
            "reviewed_ticket_ids": reviewed_ticket_ids,
            "filter_mode": filter_mode,
        },
    )
