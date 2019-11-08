#!/usr/bin/python
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import QuerySet


class DataTableForm(forms.Form):
    """ Simple datatable form, use it by subclassing """

    search = forms.CharField(required=False)
    order_no = forms.CharField()
    is_asc = forms.BooleanField(required=False)
    orderable = forms.BooleanField()
    start = forms.CharField()
    length = forms.CharField()

    mapping = {}
    extra_hidden_fields = []
    default_order_name = None

    def __init__(self, *args, **kwargs):
        super(DataTableForm, self).__init__(*args, **kwargs)
        hidden_list = ['search', 'order_no', 'is_asc', 'orderable', 'start', 'length']
        if self.extra_hidden_fields:
            hidden_list.extend(self.extra_hidden_fields)
        hidden_fields = {name for name in self.fields.keys() if name in hidden_list}
        for fields_name in hidden_fields:
            self.fields[fields_name].widget = forms.HiddenInput()

    def paging(self):
        queryset = self.get_queryset()
        start = self.cleaned_data.get('start') or 0
        length = self.cleaned_data.get('length') or 10
        page = int(start) / int(length) + 1
        paginator = Paginator(queryset, length)
        try:
            p = paginator.page(page)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)
        return self.handle_data(p), queryset.count() if isinstance(queryset, QuerySet) else len(queryset)

    def handle_data(self, data):
        """ Customized by overriding handle_data """
        return list(data)

    def get_order(self):
        name = self.default_order_name if self.default_order_name else 'id'
        orderable = self.cleaned_data.get('orderable')
        order_no = self.cleaned_data.get('order_no')
        if orderable and order_no in self.mapping:
            is_asc = self.cleaned_data.get('is_asc')
            name = self.mapping[order_no]
            name = name if is_asc else '-{}'.format(name)
        return name

    def get_queryset(self):
        raise NotImplementedError
