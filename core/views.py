from django.shortcuts import render
from django.db.models import Subquery, OuterRef
from django.views.generic.edit import CreateView

from .forms import SoftwareVersionForm, ComponentForm, StatusForm
from .models import Tractor, Component, SoftwareVersion, Assembly


def search_status_versions(tractors):
    tractors_info = []
    NAMES_CHOICES = ['EN', 'TB', 'SC', 'HD', 'DP', 'CN']
    for eachTractor in tractors:
        tractor_status = 'green'
        components_info = [{'name': '—', 'designation_comp': '—',
                            'version': '—', 'status': 'gray'}]*6
        for eachVersion in eachTractor.software_versions.all():
            if eachVersion.tractor_model is None:
                thisversions = SoftwareVersion.objects.filter(
                    component__designation = eachVersion.component.designation).order_by('-version')
                status = 'gray'
                if eachVersion.version == thisversions.first().version:
                    status = 'green'
                else:
                    for otherVersion in thisversions:
                        if otherVersion.version == eachVersion.version:
                            status = 'old'
                            if tractor_status != 'critical_old':
                                tractor_status = 'old'
                            break
                        if otherVersion.is_critical:
                            status = 'critical_old'
                            tractor_status = 'critical_old'
                            break
            else:
                thisversions = SoftwareVersion.objects.filter(tractor_model=eachVersion.tractor_model, engine_comp=eachVersion.engine_comp,
                                                              first_number=eachVersion.first_number).order_by('-release_date')
                status = 'green'
                for otherVersion in thisversions:
                    if otherVersion.second_number == eachVersion.second_number and otherVersion.third_number > eachVersion.third_number:
                        if otherVersion.is_critical:
                            status = 'critical_old'
                            tractor_status = 'critical_old'
                            break
                        else:
                            if tractor_status != 'critical_old':
                                tractor_status = 'old'
                            status = 'old'
                    if otherVersion.second_number > eachVersion.second_number:
                        if otherVersion.is_critical:
                            status = 'critical_old'
                            tractor_status = 'critical_old'
                            break
                        else:
                            if tractor_status != 'critical_old':
                                tractor_status = 'old'
                            status = 'old'
            if eachVersion.is_broken:
                status = 'broken'
                tractor_status = 'broken'
            components_info[NAMES_CHOICES.index(eachVersion.component.verbose_name)] = {'name': eachVersion.component.verbose_name, 'designation_comp': eachVersion.component.designation,
                                                                                        'version': eachVersion.version, 'status': status}
        tractors_info.append({'id': eachTractor.id, 'serial_number': eachTractor.serial_number,
                             'name': eachTractor.name, 'components': components_info, 'tractor_status': tractor_status})
    return tractors_info


def filtredTableView(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        tractors = []
        if form.is_valid():
            if form.cleaned_data['status'] == '0':
                tractors = search_status_versions(Tractor.objects.all())
            elif form.cleaned_data['status'] == '1':
                tractors = search_status_versions(Tractor.objects.filter(
                    software_versions__is_broken=True))
            elif form.cleaned_data['status'] == '2':
                tractors = list(filter(
                    lambda x: x['tractor_status'] == 'critical_old' or x['tractor_status'] == 'broken', search_status_versions(Tractor.objects.all())))
            elif form.cleaned_data['status'] == '3':
                tractors = list(
                    filter(lambda x: x['tractor_status'] == 'old', search_status_versions(Tractor.objects.all())))
        context = {'tractors_info': tractors,
                   'form': form}
        return render(request, 'core/tractors.html', context=context)
    else:
        form = StatusForm()
        tractors = search_status_versions(Tractor.objects.all())
        context = {'tractors_info': tractors,
                   'form': form}
        return render(request, 'core/tractors.html', context=context)


class SoftwareVersionCreateView(CreateView):
    model = SoftwareVersion
    form_class = SoftwareVersionForm
    template_name = 'core/software_version_create_form.html'
    success_url = '/software_vis/software_create/'

    def form_valid(self, form):
        form.instance.is_critical = (
            form.cleaned_data['is_critical'] == 'True')
        return super().form_valid(form)


class ComponentCreateView(CreateView):
    models = Component
    form_class = ComponentForm
    template_name = 'core/component_create_form.html'
    success_url = '/software_vis/component_create/'

    
