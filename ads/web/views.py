from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ..models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm


def ad_list(request):
    ads = Ad.objects.order_by('-created_at')
    return render(request, 'ad_list.html', {'ads': ads})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    proposals = ad.proposals_received.all()
    return render(request, 'ad_detail.html', {'ad': ad, 'proposals': proposals})


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm()
    return render(request, 'ad_form.html', {'form': form})


@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this ad.")
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads:ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ad_form.html', {'form': form, 'ad': ad})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this ad.")
    if request.method == 'POST':
        ad.delete()
        return redirect('ads:ad_list')
    return render(request, 'ad_confirm_delete.html', {'ad': ad})


@login_required
def proposal_create(request, sender_pk):
    ad_sender = get_object_or_404(Ad, pk=sender_pk)
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = ad_sender
            proposal.status = 'pending'
            proposal.save()
            return redirect('ads:ad_detail', pk=ad_sender.pk)
    else:
        form = ExchangeProposalForm(initial={'ad_receiver': None})
    return render(request, 'ads/proposal_form.html', {'form': form, 'ad': ad_sender})

@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    return render(request, 'ads/proposal_list.html', {'proposals': proposals})
