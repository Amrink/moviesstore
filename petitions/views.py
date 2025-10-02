from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PetitionForm
from .models import Petition, PetitionVote

def petition_list(request):
    # Annotate YES count
    petitions = (Petition.objects
                 .annotate(yes_count=Count('votes', filter=Q(votes__vote=True))))
    return render(request, 'petitions/petition_list.html', {'petitions': petitions})

@login_required
def petition_create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, 'Petition created!')
            return redirect('petitions:detail', pk=petition.pk)
    else:
        form = PetitionForm()
    return render(request, 'petitions/petition_form.html', {'form': form})

def petition_detail(request, pk):
    petition = get_object_or_404(
        Petition.objects.annotate(yes_count=Count('votes', filter=Q(votes__vote=True))),
        pk=pk
    )
    user_has_voted = False
    if request.user.is_authenticated:
        user_has_voted = PetitionVote.objects.filter(petition=petition, voter=request.user).exists()
    return render(request, 'petitions/petition_detail.html', {
        'petition': petition,
        'user_has_voted': user_has_voted
    })

@login_required
def vote_yes(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    if request.method == 'POST':
        try:
            PetitionVote.objects.create(petition=petition, voter=request.user, vote=True)
            messages.success(request, 'Your YES vote was recorded.')
        except IntegrityError:
            messages.info(request, 'You have already voted on this petition.')
        return redirect('petitions:detail', pk=petition.pk)
    # If someone GETs this URL, just bounce to detail
    return redirect('petitions:detail', pk=petition.pk)
