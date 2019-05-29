import datetime
import os

from django.shortcuts import render
from app import settings


def file_list(request, year=None, month=None, day=None):
    template_name = 'index.html'
    file_listing = []
    out_file_list = []
    file_names = os.listdir(settings.FILES_PATH)
    for file in file_names:
        file_dict = {}
        file_dict['name'] = file
        file_data = os.stat('files/' + file)
        file_dict['ctime'] = datetime.date.fromtimestamp(file_data.st_ctime)
        file_dict['mtime'] = datetime.date.fromtimestamp(file_data.st_mtime)
        file_listing.append(file_dict)
    context = {
        'files': file_listing,
        'date': None
    }

    if year is not None:
        context.clear()
        out_file_list = []
        url_date = datetime.date(year, month, day)
        for file in file_listing:
            if file['mtime'] == url_date:
                out_file_list.append(file)
        context = {
            'files': out_file_list,
            'date': url_date
        }

    return render(request, template_name, context)


def file_content(request, name):
    with open('files/' + name, 'r') as file:
        content = file.read()
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    return render(
        request,
        'file_content.html',
        context={'file_name': name, 'file_content': content}
    )
