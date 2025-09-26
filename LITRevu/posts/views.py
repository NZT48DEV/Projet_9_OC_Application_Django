"""
Vues pour la gestion des posts de l'utilisateur (tickets et critiques).
Inclut la pagination avec support AJAX pour le scroll infini.
"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from reviews.models import Review
from tickets.models import Ticket


@login_required
def user_posts(request):
    """
    Affiche les posts de l'utilisateur (tickets + critiques) triés par date.
    - Combine les tickets et critiques.
    - Trie les résultats par date de création décroissante.
    - Gère la pagination classique et AJAX (scroll infini).
    """
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    # Fusionne et trie les posts par date
    posts = sorted(
        list(tickets) + list(reviews),
        key=lambda obj: obj.time_created,
        reverse=True,
    )

    # Pagination
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(posts, 5)

    # ✅ Empêche de renvoyer la dernière page en doublon si la page demandée est trop grande
    if page_number > paginator.num_pages:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"html": "", "has_next": False})
        page_number = paginator.num_pages  # fallback si on accède directement à une page trop grande

    page_obj = paginator.get_page(page_number)

    # Requête AJAX → renvoyer uniquement le HTML des posts
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "posts/partials/_posts_list.html",
            {"posts": page_obj},
            request=request,
        )
        return JsonResponse({"html": html, "has_next": page_obj.has_next()})

    # Requête classique → rendu complet
    return render(
        request,
        "posts/user_posts.html",
        {"posts": page_obj},
    )
