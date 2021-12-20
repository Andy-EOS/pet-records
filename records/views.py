"""
Django Views.
"""
from datetime import date, timedelta, datetime
import time
from operator import attrgetter
import pandas as pd
import json

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
        if not feeding_id:
            form.initial['feeding_date'] = date.today()

        context = {
            'title': 'Gecko Feeding Entry',
            'form': form,
        }
    return render(request, 'records/form_template.html', context)

def feeding_records(request):

    query1 = SnakeFeeding.objects.all()
    query2 = GeckoFeeding.objects.all()

    names = list(map(lambda animal: animal.animal_name, Animal.objects.all()))

    default_filter_from_date = date.today() - timedelta(weeks=12)
    if request.method != 'POST':
        query1 = query1.filter(feeding_date__gte=default_filter_from_date)
        query2 = query2.filter(feeding_date__gte=default_filter_from_date)


    names_list = []
    for name in names:
        names_list.append((name, name))

    form = BasicFilterForm()
    form.fields['name'].choices = names_list
    form.initial = {
        'name':names,
        'date_from': default_filter_from_date,
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
        if not cleaning_id:
            form.initial['date_cleaned'] = date.today()

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
        if not health_id:
            form.initial['date'] = date.today()

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

    default_filter_from_date = date.today() - timedelta(weeks=12)
    if request.method != 'POST':
        query = query.filter(date_cleaned__gte=default_filter_from_date)

    form = CleaningFilterForm()
    form.fields['name'].choices = names_list
    form.initial = {
        'name':names,
        'date_from': default_filter_from_date,
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

    default_filter_from_date = date.today() - timedelta(weeks=26)
    if request.method != 'POST':
        query = query.filter(date__gte=default_filter_from_date)

    form = BasicFilterForm()
    form.fields['name'].choices = names_list
    form.initial = {
        'name':names,
        'date_from': default_filter_from_date,
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

def weights_graph(request):


    title = "Animal Weights"
    
    template = loader.get_template('records/graph.html')
    

    df = pd.DataFrame(AnimalHealth.objects.all().select_related().values('animal__animal_name', 'date', 'weight'))

    df.rename(columns = {'animal__animal_name':'name'}, inplace = True)
    df = df[df['weight'] > 0]

    df = df.sort_values('date')
    names = df['name'].unique()
    data = []

    for name in names:
        pet = df[df['name'] == name]
        dates = list(pet['date'])
        for i in range(len(dates)):
            dates[i] = time.mktime(dates[i].timetuple()) * 1000
        weights = list(pet['weight'])
        data_list = []
        for i in range(len(weights)):
            data_list.append([dates[i],weights[i]])
        data_dict = {
            "name": name,
            "data": data_list,
        }
        data.append(data_dict)

    graph_data = json.dumps(data)



    context = {
        'title': title,
        'graph_data': graph_data,
        'y_label' : "Weight (g)",

    }
    return HttpResponse(template.render(context, request))

def food_graph(request):


    title = "Food Eaten Graph"
    
    template = loader.get_template('records/graph.html')
    

    df = pd.DataFrame(GeckoFeeding.objects.all().select_related().values('animal__animal_name', 'feeding_date', 'quantity_eaten'))

    df.rename(columns = {'animal__animal_name':'name'}, inplace = True)
    df.rename(columns = {'feeding_date':'date'}, inplace = True)
    df.rename(columns = {'quantity_eaten':'eaten'}, inplace = True)
    df = df[df['eaten'] > 0]

    df = df.sort_values('date')
    names = df['name'].unique()
    data = []

    for name in names:
        pet = df[df['name'] == name]
        dates = list(pet['date'])
        for i in range(len(dates)):
            dates[i] = time.mktime(dates[i].timetuple()) * 1000
        eatens = list(pet['eaten'])
        data_list = []
        for i in range(len(eatens)):
            data_list.append([dates[i],eatens[i]])
        data_dict = {
            "name": name,
            "data": data_list,
        }
        data.append(data_dict)

    graph_data = json.dumps(data)



    context = {
        'title': title,
        'graph_data': graph_data,
        'y_label' : "Number Eaten",

    }
    return HttpResponse(template.render(context, request))