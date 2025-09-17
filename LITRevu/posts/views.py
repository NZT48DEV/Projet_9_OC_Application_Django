from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tickets.models import Ticket
from reviews.models import Review

@login_required
def user_posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    # Fusionne et trie
    posts = list(tickets) + list(reviews)
    posts = sorted(posts, key=lambda obj: obj.time_created, reverse=True)

    return render(request, "posts/user_posts.html", {"posts": posts})
