from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tickets.forms import TicketForm, ImageForm
from reviews.forms import ReviewForm
from reviews.models import Review
from tickets.models import Ticket, Image
from userfollows.models import UserBlock


@login_required
def view_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # ✅ Vérifie si l’auteur du ticket lié a bloqué l’utilisateur courant
    if UserBlock.objects.filter(user=review.ticket.user, blocked_user=request.user).exists():
        messages.error(request, "❌ Cette critique n'est pas disponible.")
        return redirect("home")

    return render(request, 'reviews/view_review.html', {'review': review})


@login_required
def create_review_with_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and image_form.is_valid() and review_form.is_valid():
            # Création du ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Création de l'image (si uploadée)
            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.ticket = ticket
                image.save()

            # Création de la critique
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            next_url = request.POST.get("next")
            return redirect(next_url or "home")
    else:
        ticket_form = TicketForm()
        image_form = ImageForm()
        review_form = ReviewForm()

    return render(request, "reviews/create_review_with_ticket.html", {
        "ticket_form": ticket_form,
        "image_form": image_form,
        "review_form": review_form,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def create_review_response(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # ✅ Vérifie si l’auteur du ticket a bloqué l’utilisateur courant
    if UserBlock.objects.filter(user=ticket.user, blocked_user=request.user).exists():
        messages.error(request, "❌ Vous ne pouvez pas répondre à ce ticket.")
        return redirect("home")

    # ✅ Vérifie si le ticket a déjà une critique
    if Review.objects.filter(ticket=ticket).exists():
        messages.error(request, "❌ Ce ticket a déjà une critique.<br>Vous ne pouvez pas en ajouter une autre.")
        next_url = request.GET.get("next", "home")
        return redirect(next_url)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "✅ Votre critique a bien été publiée.")
            next_url = request.POST.get("next") or request.GET.get("next") or "home"
            return redirect(next_url)
    else:
        form = ReviewForm()

    return render(request, "reviews/create_review_response.html", {
        "ticket": ticket,
        "review_form": form,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        next_url = request.POST.get("next")
        review.delete()
        messages.success(request, "✅ Votre critique a bien été supprimée.")
        return redirect(next_url or "user_posts")

    return render(request, "reviews/delete_review.html", {
        "review": review,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Votre critique a bien été modifiée.")
            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/update_review.html", {
        "form": form,
        "review": review,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def update_review_with_ticket(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket

    # ✅ Gérer le cas où le ticket n’a pas d’image
    try:
        image_instance = ticket.image
    except Image.DoesNotExist:
        image_instance = None

    if request.method == "POST":
        if "delete_review" in request.POST:
            review.delete()
            messages.success(request, "✅ Votre critique a bien été supprimée.")
            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")

        if "delete_ticket" in request.POST:
            ticket.delete()
            messages.success(request, "✅ Votre ticket a bien été supprimé.")
            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")

        # Sinon → bouton Enregistrer
        ticket_form = TicketForm(request.POST, instance=ticket)
        image_form = ImageForm(request.POST, request.FILES, instance=image_instance)
        review_form = ReviewForm(request.POST, instance=review)

        if ticket_form.is_valid() and image_form.is_valid() and review_form.is_valid():
            # Sauvegarde ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Sauvegarde image
            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.ticket = ticket
                image.save()

            # Sauvegarde critique
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "✅ Vos modifications ont bien été enregistrées.")
            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")
    else:
        ticket_form = TicketForm(instance=ticket)
        image_form = ImageForm(instance=image_instance)
        review_form = ReviewForm(instance=review)

    return render(request, "reviews/update_review_with_ticket.html", {
        "ticket_form": ticket_form,
        "image_form": image_form,
        "review_form": review_form,
        "ticket": ticket,
        "review": review,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def delete_review_with_ticket(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket

    if request.method == "POST":
        next_url = request.POST.get("next")
        review.delete()
        ticket.delete()
        messages.success(request, "✅ Le ticket et sa critique ont bien été supprimés.")
        return redirect(next_url or "user_posts")

    return render(request, "reviews/delete_review_with_ticket.html", {
        "review": review,
        "ticket": ticket,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })
