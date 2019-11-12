import mock
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.test import TestCase

from simple_datatable import DataTable


class DataTableTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'order[0][column]': '0',
            'order[0][dir]': 'desc',
            'columns[0][data]': 'xxx',
            'columns[0][name]': '',
            'columns[0][search][regex]': 'false',
            'columns[0][search][value]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'false',
            'search[value]': 'abc',
            'search[regex]': 'false',
            'start': '0',
            'length': '10',
            'draw': '1',
        }

    def setUp(self):
        self.dt = DataTable(self.data)

    def test_parsed(self):
        self.assertEqual({
            'columns': {
                '0': {
                    'data': 'xxx',
                    'name': '',
                    'orderable': 'false',
                    'searchable': 'true',
                    'search': {
                        'regex': 'false',
                        'value': ''
                    },
                }
            },
            'order': {
                '0': {
                    'column': '0',
                    'dir': 'desc'
                }
            },
            'search': {
                'regex': 'false',
                'value': 'abc'
            },
            'start': '0',
            'length': '10',
            'draw': '1',
        }, self.dt.parsed)

    def test_search(self):
        self.assertEqual('abc', self.dt.search)

    def test_start(self):
        self.assertEqual(0, self.dt.start)

    def test_length(self):
        self.assertEqual(10, self.dt.length)

    def test_page(self):
        self.assertEqual(1, self.dt.page)

    def test_paging(self):
        p, count = self.dt.paging([])
        self.assertEqual(0, count)
        self.assertIsNotNone(p)

        with mock.patch('django.core.paginator.Paginator.page') as mocked:
            mocked.side_effect = [PageNotAnInteger, ['fake return']]
            p, count = self.dt.paging([])
            self.assertEqual(0, count)
            self.assertEqual(['fake return'], p)

        with mock.patch('django.core.paginator.Paginator.page') as mocked:
            mocked.side_effect = [EmptyPage, ['fake return']]
            p, count = self.dt.paging([])
            self.assertEqual(0, count)
            self.assertEqual(['fake return'], p)

    if """ get_order_by """:
        def test_get_order_by(self):
            self.assertEqual([('xxx', 'desc', 'abc')], self.dt.get_order_by(mapping={'xxx': 'abc'}))

        def test_get_order_by_for_db(self):
            self.assertEqual([], self.dt.get_order_by(mapping={}, is_db_sort=True))
            self.assertEqual(['-db_xxx'], self.dt.get_order_by(mapping={'xxx': 'db_xxx'}, is_db_sort=True))

    if """ sort_list """:
        def test_sort_list_for_string(self):
            list_to_sort = [{'xxx': 'e'}, {'xxx': 'a'}, {'xxx': 'd'}, {'xxx': 'b'}, {'xxx': 'c'}]
            self.dt.sort_list(mapping={'xxx': True}, list_to_sort=list_to_sort)
            self.assertEqual([{'xxx': 'e'}, {'xxx': 'd'}, {'xxx': 'c'}, {'xxx': 'b'}, {'xxx': 'a'}], list_to_sort)

        def test_sort_list_for_not_string(self):
            list_to_sort = [{'xxx': 5}, {'xxx': 1}, {'xxx': 4}, {'xxx': 2}, {'xxx': 3}]
            self.dt.sort_list(mapping={'xxx': False}, list_to_sort=list_to_sort)
            self.assertEqual([{'xxx': 5}, {'xxx': 4}, {'xxx': 3}, {'xxx': 2}, {'xxx': 1}], list_to_sort)
