from datetime import date, timedelta, datetime
import time
from operator import attrgetter
import pandas as pd
import json

from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect

from .models import Chore
from .forms import ChoreForm
# Create your views here.

def index(request):
    chores_list = list(Chore.objects.all())
    chores_list.sort(key=lambda inst: inst.get_due_in_days())
    chore_table_entries = list(map(lambda chore: chore.table_entry(),chores_list))

    title = "Chores Overview"

    template = loader.get_template('chores/table_chores.html')

    context = {
        'chore_table_entries': chore_table_entries,
        'title': title,
    }
    return HttpResponse(template.render(context, request))

def chore_entry(request, chore_id=None):
    instance = None
    if chore_id:
        instance = Chore.objects.get(pk=chore_id)
    if request.method == 'POST':
        form = ChoreForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ChoreForm(instance=instance)
        if not chore_id:
            form.initial['date_done'] = date.today()

        context = {
            'title': f'Chore Entry {chore_id}',
            'form': form,
        }
    return render(request, 'chores/form_template.html', context)

def chore_done_today(request, chore_id=None):
    instance = None
    if chore_id:
        instance = Chore.objects.get(pk=chore_id)
        instance.date_done = date.today()
        instance.save()
    
    response = redirect('index')
    return response