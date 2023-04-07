import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from . import forms
from . import models
from .models import Record, Persone


class HomePageView(CreateView):
    template_name = 'telefonbook/home.html'
    form_class = forms.CreatePersoneFrom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["persones"] = models.Persone.objects.all()
        return context


class AddPhoneFormView(CreateView):
    template_name = 'telefonbook/add_persone.html'
    form_class = forms.CreatePersoneFrom
    success_url = reverse_lazy('home')

    def get_success_url(self) -> str:
        phone_numbers = self.request.POST.get('phones')
        for phone_number in phone_numbers.split('\n'):
            models.Phone.objects.create(phone=phone_number, contact=self.object)
        return super().get_success_url()


class DeletePhoneView(DeleteView):
    model = models.Persone
    template_name = "telefonbook/delete_persone.html"
    success_url = reverse_lazy('home')


class ListRecordView(CreateView):
    template_name = 'telefonbook/list.html'
    form_class = forms.CreateRecordFrom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["records"] = models.Record.objects.all()
        return context


class AddRecordFormView(CreateView):
    template_name = 'telefonbook/add_record.html'
    form_class = forms.CreateRecordFrom
    success_url = reverse_lazy('list')


class DeleteRecordView(DeleteView):
    model = models.Record
    template_name = "telefonbook/delete_record.html"
    success_url = reverse_lazy('list')


def delete_item(request, pk):
    item = Record.objects.get(pk=pk)
    if request.user == item.user or request.user.is_superuser:
        Record.objects.filter(id=pk).delete()
        status = True
    else:
        status = False
    return JsonResponse({'status': status})


def add_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item = Record(name=data['name'], description=data['description'], colors_id=data['colors'], user=request.user)
        item.save()
        return JsonResponse({'name': item.name, 'description': item.description, 'colors': model_to_dict(item.colors)})


def delete_phone(request, pk):
    persone = Persone.objects.get(pk=pk)
    if request.user == persone.user or request.user.is_superuser:
        Persone.objects.filter(id=pk).delete()
        status = True
    else:
        status = False
    return JsonResponse({'status': status})


def add_persone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item = Persone(name=data['name'],  user=request.user)
        item.save()
        return JsonResponse({'name': item.name})
