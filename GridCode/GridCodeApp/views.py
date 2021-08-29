from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from GridCodeApp.forms import FileHandlerForm
from GridCodeApp.models import FileHandler
from django.template import loader
import h5py
mode = 'r'

def index(request):
    return render(request, 'index.html')

def upload(request):
    context = {}
    get_files = FileHandler.objects.all().last()   #FileHandler it's the name of class which can query our database
    context = {'get_files': get_files}          # We use context to pass data to the HTML template
    keys = []                                   # It will hold all of the keys that the HDF5 file holds, ie: 'E1p14162_DV_1p5_1em3_1'
    with h5py.File(f'media/{str(get_files.file_upload)}', mode) as hdf:
        for key in hdf.keys():
            keys.append(key)
            G_items = dict(hdf.get(key).items())
        hdf.close()
    template = loader.get_template('upload.html')
    context['keys'] = keys
    return HttpResponse(template.render(context, request))

class IndexView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_files = FileHandler.objects.all()
        context = {'form': FileHandlerForm, 'get_files': get_files}
        return context
    def post(self, request, **kwargs):
        context = {}
        if request.method == 'POST':
            form = FileHandlerForm(request.POST, request.FILES)
            if form.is_valid():
                FileHandler.objects.get_or_create(file_upload=form.cleaned_data.get('file_upload'))
                return redirect('upload')
            else:
                context['form'] = form
        else:
            context['form'] = form
        return redirect('index')

def get_group(request, val):
    context = {}
    data_sections = {}
    get_files = FileHandler.objects.all().last()
    with h5py.File(f'media/{str(get_files.file_upload)}', mode) as hdf:
        data_points = hdf[val]
        max_labels = 0
        for i, section in enumerate(data_points):
            data_of_section = list(data_points.get(section))[::120]
            if len(data_of_section) > max_labels:
                max_labels = len(data_of_section)
            data_sections[section] = data_of_section
        context['range'] = range(max_labels)
        test = []
        for key in data_sections.keys():
            val = data_sections[key]
            test.append(val)
        context['data_sections'] = test
        context['keys'] = list(data_sections.keys())
        print(test)
        template = loader.get_template('chart.html')
        return HttpResponse(template.render(context, request))
    raise Http404()
