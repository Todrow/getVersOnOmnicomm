from django.shortcuts import render

from django.shortcuts import render
from .models import Tractor, Component, SoftwareVersion
from django.db.models import Subquery, OuterRef


def tractor_list(request):
    tractors = Tractor.objects.all()
    tractors_info = []
    NAMES_CHOICES = ['EN', 'TB', 'SC', 'HD', 'DP', 'CN']
    for eachTractor in tractors:
        components_info = [{'name': '—', 'designation_comp': '—',
                            'version': '—', 'status': 'gray'}]*6
        for eachVersion in eachTractor.software_versions.all():
            thisversions = SoftwareVersion.objects.filter(tractor_model=eachVersion.tractor_model, engine_comp=eachVersion.engine_comp,
                                                            first_number=eachVersion.first_number).order_by('-release_date')
            status = 'green'
            for otherVersion in thisversions:
                if otherVersion.second_number == eachVersion.second_number and otherVersion.third_number > eachVersion.third_number:
                    if otherVersion.is_critical:
                        status = 'crirtical_old'
                        break
                    else:
                        status = 'old'
                if otherVersion.second_number > eachVersion.second_number:
                    if otherVersion.is_critical:
                        status = 'crirtical_old'
                        break
                    else:
                        status = 'old'
            if eachVersion.is_broken:
                status = 'broken'
            components_info[NAMES_CHOICES.index(eachVersion.component.verbose_name)] = {'name': eachVersion.component.verbose_name, 'designation_comp': eachVersion.component.designation,
                                   'version': eachVersion.get_version(), 'status': status}
        tractors_info.append({'id': eachTractor.id, 'serial_number': eachTractor.serial_number,
                             'name': eachTractor.name, 'components': components_info})
    context = {'tractors_info': tractors_info,
               'components': list(Component.objects.values_list('designation', flat=True))}
    return render(request, 'core/tractors.html', context=context)
