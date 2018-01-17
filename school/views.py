from .models import Event
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'school/home.html', {})

def panthers(request):
    return house(request, "panthers")

def lions(request):
    return house(request,"lions")

def tigers(request):
    return house(request,"tigers")

def jaguars(request):
    return house(request,"jaguars")

def house(request,name):
    all_event = quick_sort(Event.objects.all())
    sum = 0
    ranks = []
    for event in all_event:
        ranks.append(event.getRankByName(name))
    context = {
        'sum' : sum,
        'all_events': all_event,
        'name': name,
        'CapName': (name[:1].upper() + name[1:])[:-1],
    }
    return render(request, 'school/house.html', context)

def overview(request):
    all_event = Event.objects.all()
    context = {
        'all_events': quick_sort(all_event),
    }
    return render(request, 'school/overview.html', context)


def scoreCard(request):
    if request.user.is_authenticated():
        all_event = Event.objects.all()
        sumP = 0
        for event in all_event:
            sumP += event.getPantherScore
        sumL = 0
        for event in all_event:
            sumL += event.getLionScore
        sumT = 0
        for event in all_event:
            sumT += event.getTigerScore
        sumJ = 0
        for event in all_event:
            sumJ += event.getJaguarScore
        context = {
            'all_events': quick_sort(all_event),
            'p':sumP,
            'l':sumL,
            't':sumT,
            'j':sumJ,
        }
        return render(request, 'school/scoreCard.html', context)
    else:
        return HttpResponse("<meta http-equiv=\"refresh\" content=\"0; url=/core\" />")

def hasHappened(event_date):
    return not date.today() < event_date

def quick_sort(l):
    length = len(l)
    if length <=1:
        return l
    else:
        pivot = l[(int(length/2))]
        new = []
        for event in range(len(l)):
            if event == int(length/2):
                pass
            else:
                new.append(l[event])
        l = new
        less, more = [], []
        for x in l:
            if x.event_date<pivot.event_date:
                less.append(x)
            else:
                more.append(x)
        return quick_sort(less) + [pivot] + quick_sort(more)


def event_details(request,event_id):
    event = Event.objects.get(pk=event_id)
    context = {
        "event": event,
        "true": True,
    }
    return render(request, 'school/details.html', context)

def main(request):
    return HttpResponse("HUnumunu")