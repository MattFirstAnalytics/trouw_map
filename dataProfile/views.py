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
        data['map_file'] = 'BEA'
    data['company_name'] = company_name
    data['data_source'] = page_heading
    data['filters'] = views_functions.get_unique_lists(data['map_file'])
    print(data)
    return render(request, 'dataProfile/map.html', data)