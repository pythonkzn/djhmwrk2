import datetime
import os

from django.shortcuts import render
from app import settings


def file_list(request, year=None, month=None, day=None):
    template_name = 'index.html'
    file_listing = []
    file_names = os.listdir(settings.FILES_PATH)
    if year:
        url_date = datetime.date(year, month, day)
    else:
        url_date = None
    for name in file_names:
        file_dict = {}
        file_dict['name'] = name
        file_data = os.stat('files/' + name)
        file_dict['ctime'] = datetime.date.fromtimestamp(file_data.st_ctime)
        file_dict['mtime'] = datetime.date.fromtimestamp(file_data.st_mtime)
        if url_date is not None:
            if file_dict['mtime'] == url_date:
                file_listing.append(file_dict)
        else:
            file_listing.append(file_dict)
    context = {
        'files': sorted(file_listing, key=lambda k: k['mtime']),
        'date': url_date
    }
    return render(request, template_name, context)


def file_content(request, name):
    content = ''
    try:
        with open('files/' + name, 'r') as f:
            content = f.read()
            temp_path = 'file_content.html'
    except:
        temp_path = 'error.html'

    return render(
        request,
        temp_path,
        context={'file_name': name, 'file_content': content}
    )
