"""
Django Views.
"""
from datetime import date, timedelta
from operator import attrgetter

from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect

from .models import Animal, SnakeFeeding, GeckoFeeding, AnimalCleaning, AnimalHealth
from .models import Snake, Gecko

from .forms import SnakeFeedingForm, GeckoFeedingForm, AnimalCleaningForm, AnimalHealthForm
from.forms import SnakeForm, GeckoForm, CleaningFilterForm, BasicFilterForm

def index(request):
    animal_instances_list = list(Snake.objects.all()) + list(Gecko.objects.all())
    animal_instances_list.sort(key=lambda inst: inst.animal_name)
    animal_table_entries = list(map(lambda animal: animal.table_entry(),animal_instances_list))

    title = "Pet Overview"
    
    template = loader.get_template('records/table_animals.html')

    context = {
        'animal_table_entries': animal_table_entries,
        'title': title,
    }
    return HttpResponse(template.render(context, request))

def snake_entry(request, animal_id=None):
    instance = None
    if animal_id:
        instance = Snake.objects.get(pk=animal_id)
    if request.method == 'POST':
        form = SnakeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SnakeForm(instance=instance)

        context = {
            'title': f'Snake Entry {animal_id}',
            'form': form,
        }
    return render(request, 'records/form_template.html', context)

def gecko_entry(request, animal_id=None):
    instance = None
    if animal_id:
        instance = Gecko.objects.get(pk=animal_id)
    if request.method == 'POST':
        form = GeckoForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = GeckoForm(instance=instance)

        context = {
            'title': f'Gecko Entry {animal_id}',
            'form': form,
        }
    return render(request, 'records/form_template.html', context)

def snake_feeding_entry(request, feeding_id=None):
    instance = None
    if feeding_id:
        instance = SnakeFeeding.objects.get(pk=feeding_id)
    if request.method == 'POST':
        form = SnakeFeedingForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('feeding_records')
    else:
        form = SnakeFeedingForm(instance=instance)
        if not feeding_id:
            form.initial['feeding_date'] = date.today()

        context = {
            'title': f'Snake Feeding Entry {feeding_id}',
            'form': form,
        }
    return render(request, 'records/form_template.html', context)

def gecko_feeding_entry(request, feeding_id=None):
    instance = None
    if feeding_id:
            instance = GeckoFeeding.objects.get(pk=feeding_id)
    if request.method == 'POST':  
        form = GeckoFeedingForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('feeding_records')
    else:
        form = GeckoFeedingForm(instance=instance)

        context = {
            'title': 'Gecko Feeding Entry',
            'form': form,
        }
    return render(request, 'records/form_template.html', context)

def feeding_records(request):

    query1 = SnakeFeeding.objects.all()
    query2 = GeckoFeeding.objects.all()

    names = list(map(lambda animal: animal.animal_name, Animal.objects.all()))

    names_list = []
    for name in names:
        names_list.append((name, name))

    form = BasicFilterForm()
    form.fields['name'].choices = names_list
    form.initial = {
        'name':names,
        'date_from': date.today() - timedelta(weeks=12),
        'date_to': date.today(),
    }

    if request.method == 'POST':

        if 'name' in request.POST:
            names = request.POST.getlist('name')
        else:
            names = []
        form.initial['name'] = names
        query1 = query1.filter(animal__animal_name__in=names)
        query2 = query2.filter(animal__animal_name__in=names)

        if request.POST['date_from']:
            date_from = request.POST.get('date_from')
            form.initial['date_from'] = date_from
            query1 = query1.filter(feeding_date__gte=date_from)
            query2 = query2.filter(feeding_date__gte=date_from)

        if request.POST['date_to']:
            date_to = request.POST.get('date_to')
            form.initial['date_to'] = date_to
            query1 = query1.filter(feeding_date__lte=date_to)
            query2 = query2.filter(feeding_date__lte=date_to)


    feeding_instances_list = list(query1.all()) + list(query2.all())
    feeding_instances_list.sort(key=lambda inst: inst.get_date(),reverse=True)
    feeding_table_entries = list(map(lambda feeding: feeding.table_entry(),feeding_instances_list))

    title = "Feeding Overview"
    
    template = loader.get_template('records/table_feeding.html')

    context = {
        'feeding_table_entries': feeding_table_entries,
        'title': title,
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def cleaning_entry(request, cleaning_id=None):
    instance = None
    if cleaning_id:
        instance = AnimalCleaning.objects.get(pk=cleaning_id)
    if request.method == 'POST':
        form = AnimalCleaningForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('cleaning_records')
    else:
        form = AnimalCleaningForm(instance=instance)

        context = {
            'title': f'Animal Cleaning Entry {cleaning_id}',
            'form': form,
        }
    return render(request, 'records/form_template.html', context)

def healthy_entry(request, health_id=None):
    instance = None
    if health_id:
        instance = AnimalHealth.objects.get(pk=health_id)
    if request.method == 'POST':
        form = AnimalHealthForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('health_records')
    else:
        form = AnimalHealthForm(instance=instance)

        context = {
            'title': f'Animal Health Entry {health_id}',
            'form': form,
        }
    return render(request, 'records/form_template.html', context)

def cleaning_records(request):

    query  = AnimalCleaning.objects
    
    names = list(map(lambda animal: animal.animal_name, Animal.objects.all()))
    clean_type = []
    for code, text in AnimalCleaning.CLEANING_TYPE_CHOICES:
        clean_type.append(code)

    names_list = []
    for name in names:
        names_list.append((name, name))

    form = CleaningFilterForm()
    form.fields['name'].choices = names_list
    form.initial = {
        'name':names,
        'date_from': date.today() - timedelta(weeks=12),
        'date_to': date.today(),
        'clean_type': clean_type
    }


    if request.method == 'POST':

        if 'name' in request.POST:
            names = request.POST.getlist('name')
        else:
            names = []
        form.initial['name'] = names
        query = query.filter(animal__animal_name__in=names)

        if 'clean_type' in request.POST:
            clean_type = request.POST.getlist('clean_type')
        else:
            clean_type = []
        form.initial['clean_type'] = clean_type
        query = query.filter(type_of_clean__in=clean_type)

        if request.POST['date_from']:
            date_from = request.POST.get('date_from')
            form.initial['date_from'] = date_from
            query = query.filter(date_cleaned__gte=date_from)

        if request.POST['date_to']:
            date_to = request.POST.get('date_to')
            form.initial['date_to'] = date_to
            query = query.filter(date_cleaned__lte=date_to)
    
    cleaning_instances_list = list(query.all())
    cleaning_instances_list.sort(key=lambda inst: inst.get_date(),reverse=True)
    cleaning_table_entries = list(map(lambda inst: inst.table_entry(),cleaning_instances_list))

    title = "Cleaning Overview"
    headers = ['Date', 'Name', 'Type']
    
    template = loader.get_template('records/table_cleaning.html')
    
    context = {
        'cleaning_table_entries': cleaning_table_entries,
        'headers': headers,
        'title': title,
        'form': form,
    }

    return HttpResponse(template.render(context, request))

def health_records(request):

    query = AnimalHealth.objects.all()

    names = list(map(lambda animal: animal.animal_name, Animal.objects.all()))

    names_list = []
    for name in names:
        names_list.append((name, name))

    form = BasicFilterForm()
    form.fields['name'].choices = names_list
    form.initial = {
        'name':names,
        'date_from': date.today() - timedelta(weeks=26),
        'date_to': date.today(),
    }


    if request.method == 'POST':

        if 'name' in request.POST:
            names = request.POST.getlist('name')
        else:
            names = []
        form.initial['name'] = names
        query = query.filter(animal__animal_name__in=names)

        if request.POST['date_from']:
            date_from = request.POST.get('date_from')
            form.initial['date_from'] = date_from
            query = query.filter(date__gte=date_from)

        if request.POST['date_to']:
            date_to = request.POST.get('date_to')
            form.initial['date_to'] = date_to
            query = query.filter(date__lte=date_to)

    health_instances_list = list(query.all())
    health_instances_list.sort(key=lambda inst: inst.get_date(),reverse=True)
    health_table_entries = list(map(lambda inst: inst.table_entry(),health_instances_list))

    title = "Health Overview"
    headers = ['Date', 'Name', 'Weight','Regurgitated?','Comments']
    
    template = loader.get_template('records/table_health.html')

    context = {
        'health_table_entries': health_table_entries,
        'headers': headers,
        'title': title,
        'form': form,
    }
    return HttpResponse(template.render(context, request))
