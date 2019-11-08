from django.http import JsonResponse
from django.views.generic import FormView

from easy_datatable.forms import DataTableForm


class DataTableFormView(FormView):
    """ Simple datatable view, use it by subclassing """

    def get_form_class(self):
        if self.form_class:
            if issubclass(self.form_class, DataTableForm):
                return self.form_class
            raise Exception('From is not a subclass of DataTableForm')
        raise Exception('Form not found')

    def form_valid(self, form):
        data, count = form.paging()
        return JsonResponse({'recordsFiltered': count, 'recordsTotal': count, 'data': data}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'recordsFiltered': 0, 'recordsTotal': 0, 'error': 'Data input error, please try again!'},
                            status=400)

    def get_form_kwargs(self):
        kwargs = super(DataTableFormView, self).get_form_kwargs()
        if 'data' in kwargs:
            data = kwargs['data'].copy()
            data.update({
                'order_no': data.get('order[0][column]') or '0',
                'is_asc': True if data.get('order[0][dir]') == 'asc' else False,
                'orderable': True if data.get('columns[0][orderable]') == 'true' else False,
                'start': data.get('start'),
                'length': data.get('length'),
                'search': data.get('search[value]'),
            })
            data._mutable = False
            kwargs['data'] = data
        return kwargs
