import datetime

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

from .models import Station,TableIndex,TableBasic

#nowtime
now = timezone.now() + datetime.timedelta(hours=9)
now = now.time()

# Create your views here.
def index(request):
    stations= Station.objects.all()
    context = {
            'stations':stations,
            }
    return render(request, 'tutbusinfo/index.html',context)


def tableindex(request,station_name):
    s = Station.objects.get(name=station_name)
    tables = s.tableindex_set.all()
    context = {
            'station_name':station_name,
            'tables':tables
            }
    return render(request, 'tutbusinfo/tableindex.html',context)


def table(request,station_name,table_name):
    now = timezone.now() + datetime.timedelta(hours=9)
    now = now.time()
    s = Station.objects.get(name=station_name)
    t = s.tableindex_set.get(name=table_name)
    rows = t.tablebasic_set.filter(arrive_station__gte=now).order_by('left_campus')
    context = {
            'now':now,
            'rows':rows,
            }
    return render(request,'tutbusinfo/table.html',context)
