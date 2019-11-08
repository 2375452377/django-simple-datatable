import json

import mock as mock
from django import forms
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.test import TestCase, RequestFactory

from easy_datatable.forms import DataTableForm
from easy_datatable.views import DataTableFormView


class DataTableFormViewTestCase(TestCase):
    def test_get_form_class(self):
        request = RequestFactory().get('/')
        datatable_view = DataTableFormView(request=request)
        with self.assertRaisesMessage(Exception, 'Form not found'):
            datatable_view.get_form_class()

        datatable_view.form_class = forms.Form
        with self.assertRaisesMessage(Exception, 'From is not a subclass of DataTableForm'):
            datatable_view.get_form_class()

        datatable_view.form_class = DataTableForm
        self.assertEqual(DataTableForm, datatable_view.get_form_class())

    def test_get_form_kwargs(self):
        request = RequestFactory().post('/', {'order[0][dir]': 'asc', 'order[0][column]': '1', 'start': '1',
                                              'length': '10', 'search[value]': 'a'})
        datatable_view = DataTableFormView(request=request)
        kwargs = datatable_view.get_form_kwargs()
        data = kwargs['data']
        self.assertEqual(True, data.get('is_asc'))
        self.assertEqual('1', data.get('order_no'))
        self.assertEqual('1', data.get('start'))
        self.assertEqual('10', data.get('length'))
        self.assertEqual('a', data.get('search'))

    def test_form_valid(self):
        request = RequestFactory().post('/', {'order[0][dir]': 'asc', 'order[0][column]': '1', 'start': '1',
                                              'length': '10', 'search[value]': 'a', 'columns[0][orderable]': 'true'})
        datatable_view = DataTableFormView(request=request)
        datatable_view.form_class = DataTableForm
        kwargs = datatable_view.get_form_kwargs()
        form = DataTableForm(**kwargs)
        form.get_queryset = lambda: []
        self.assertTrue(form.is_valid())
        resp = datatable_view.form_valid(form)
        self.assertEqual(200, resp.status_code)
        self.assertEqual({
            'recordsFiltered': 0, 'recordsTotal': 0,
            'data': []
        }, json.loads(resp.content))

    def test_form_invalid(self):
        request = RequestFactory().get('/')
        datatable_view = DataTableFormView(request=request)
        resp = datatable_view.form_invalid(None)
        self.assertEqual(400, resp.status_code)
        self.assertEqual({
            'recordsFiltered': 0, 'recordsTotal': 0,
            'error': 'Data input error, please try again!'
        }, json.loads(resp.content))


class DataTableFormTestCase(TestCase):
    def setUp(self):
        DataTableForm.extra_hidden_fields = ['a']
        DataTableForm.mapping.update({'0': 'id'})
        self.form = DataTableForm({'start': 1, 'length': 10, 'order_no': '0', 'is_asc': 'on', 'orderable': 'true'})
        self.form.is_valid()

    def test_paging(self):
        self.form.get_queryset = lambda: []
        p, count = self.form.paging()
        self.assertEqual(0, count)
        self.assertIsNotNone(p)

        with mock.patch('django.core.paginator.Paginator.page') as mocked:
            mocked.side_effect = [PageNotAnInteger, ['fake return']]
            p, count = self.form.paging()
            self.assertEqual(0, count)
            self.assertEqual(['fake return'], p)

        with mock.patch('django.core.paginator.Paginator.page') as mocked:
            mocked.side_effect = [EmptyPage, ['fake return']]
            p, count = self.form.paging()
            self.assertEqual(0, count)
            self.assertEqual(['fake return'], p)

    def test_get_order(self):
        self.assertEqual('id', self.form.get_order())

    def test_get_queryset(self):
        with self.assertRaises(NotImplementedError):
            self.assertTrue(self.form.is_valid())
            self.form.get_queryset()
