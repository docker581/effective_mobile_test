from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from ..models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def ad_list(request):
    ads = Ad.objects.order_by('-created_at')
    
    user_id = request.GET.get('user')
    if user_id:
        ads = ads.filter(user_id=user_id)
    
    return render(request, 'index.html', {'ads': ads})


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    proposals = ExchangeProposal.objects.filter(ad_receiver=ad)
    
    error = request.GET.get('error')
    if error:
        messages.error(request, error)
    
    return render(request, 'ad_detail.html', {
        'ad': ad,
        'proposals': proposals,
    })


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', pk=ad.pk)
    form = AdForm()
    return render(request, 'ad_form.html', {'form': form})


@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого '
                                'объявления')
        return redirect('ad_detail', pk=pk)
    
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено')
            return redirect('ad_detail', pk=pk)
    form = AdForm(instance=ad)
    return render(request, 'ad_form.html', {'form': form, 'ad': ad})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        messages.error(request, 'У вас нет прав на удаление этого объявления')
        return redirect('ad_detail', pk=pk)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление успешно удалено')
        return redirect('index')
    return render(request, 'ad_confirm_delete.html', {'ad': ad})


@login_required
def proposal_create(request, sender_pk):
    ad_receiver = get_object_or_404(Ad, pk=sender_pk)
    
    if ad_receiver.user == request.user:
        messages.error(request, 'Вы не можете предложить обмен для своего '
                               'собственного объявления')
        return redirect('ad_detail', pk=sender_pk)
    
    user_ads = Ad.objects.filter(user=request.user)
    if not user_ads.exists():
        messages.error(request, 'У вас нет собственных объявлений для обмена')
        return redirect('ad_detail', pk=sender_pk)
    
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = form.cleaned_data['ad_sender']
            proposal.ad_receiver = ad_receiver
            proposal.status = 'pending'
            proposal.save()
            messages.success(request, 'Предложение обмена успешно создано')
            return redirect('ad_detail', pk=sender_pk)
    else:
        form = ExchangeProposalForm(initial={'ad_receiver': ad_receiver})
        form.fields['ad_sender'].queryset = user_ads
        form.fields['ad_sender'].label = 'Выберите ваше объявление для обмена'
        form.fields['ad_receiver'].widget = forms.HiddenInput()
    
    return render(request, 'proposal_form.html', {
        'form': form,
        'ad': ad_receiver,
    })

@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    return render(request, 'proposal_list.html', {'proposals': proposals})
