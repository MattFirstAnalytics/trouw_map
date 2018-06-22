from django.shortcuts import render
import glob
import os
from . import profiler
from . import views_functions

# global variables
company_name = 'Trouw'
page_heading = 'Distribution Map'
data_path = os.getcwd() + '/dataProfile/static/data/output/'

# request functions
def map(request):
    data = {}
    try:
        data['map_file'] = request.GET["file"]
    except:
        data['map_file'] = 'bea'
    data['company_name'] = company_name
    data['data_source'] = page_heading
    return render(request, 'dataProfile/map.html', data)