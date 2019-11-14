__all__ = ('DataTable', )

import operator
import re

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.functional import cached_property


class DataTable(object):
    """ Simple datatable backend """

    default_start = 0
    default_length = 10
    pattern = re.compile(r"(columns|search|order)(?:\[(\d+)\])?\[(\w+)\](?:\[(\w+)\])?")

    def __init__(self, data):
        self._data = data

    @cached_property
    def parsed(self):
        return self._datatables2dict(self._data)

    @cached_property
    def search(self):
        return self.parsed['search']['value']

    @cached_property
    def start(self):
        start = self.parsed['start']
        return int(start) if start else self.default_start

    @cached_property
    def length(self):
        length = self.parsed['length']
        return int(length) if length else self.default_length

    @cached_property
    def page(self):
        return self.start / self.length + 1

    def _datatables2dict(self, data):
        """
        Parse datatables data to dict

            {
                'order[0][column]': '0',
                'order[0][dir]': 'desc',
                'columns[0][data]': 'xxx',
                'columns[0][name]': '',
                'columns[0][search][regex]': 'false',
                'columns[0][search][value]': '',
                'columns[0][searchable]': 'true',
                'columns[0][orderable]': 'false',
                'search[value]': '',
                'search[regex]': 'false',
                'start': '0',
                'length': '10',
                'draw': '1',
            }

            parse to

            {
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
                    'value': ''
                },
                'start': '0',
                'length': '10',
                'draw': '1',
            }
        """

        parsed = {}
        for column, value in data.items():
            result = self.pattern.match(column)
            if result:
                """
                search[value]             ==> search , None, value , None
                order[0][column]          ==> order  , 0   , column, None
                columns[0][search][regex] ==> columns, 0   , search, regex
                """
                column_name, column_id, key, option_key = result.groups()

                """
                parsed = {
                    'column_name': {}
                }
                """
                column_name_dict = parsed.setdefault(column_name, {})
                if column_id:
                    """
                    parsed = {
                        'column_name': {
                            'column_id': {}
                        }
                    }
                    """
                    column_id_dict = column_name_dict.setdefault(column_id, {})
                    if option_key:
                        """
                        parsed = {
                            'column_name': {
                                'column_id': {
                                    'key': {
                                        'option_key': value
                                    }
                                }
                            }
                        }
                        """
                        column_id_dict.setdefault(key, {}).update({option_key: value})
                    else:
                        """
                        parsed = {
                            'column_name': {
                                'column_id': {
                                    'key': value
                                }
                            }
                        }
                        """
                        column_id_dict[key] = value
                else:
                    """
                    parsed = {
                        'column_name': {
                            'key': value
                        }
                    }
                    """
                    column_name_dict[key] = value
            else:
                """
                parsed = {
                    'column': value
                }
                """
                parsed[column] = value
        return parsed

    def get_order_by(self, mapping, is_db_sort=False, ignored_columns=None):
        if ignored_columns is None:
            ignored_columns = ()

        order_list = []
        if is_db_sort:
            """ To pass the returned list into the .order_by() function, need to put as .order_by(*returned_list) """
            for order, item in sorted(self.parsed['order'].items()):
                column = self.parsed['columns'][item['column']]['data']
                if column in ignored_columns or column not in mapping:
                    continue

                db_column = mapping[self.parsed['columns'][item['column']]['data']]
                if item['dir'] == 'desc':
                    db_column = '-' + db_column
                order_list.append(db_column)
        else:
            for order, item in sorted(self.parsed['order'].items(), reverse=True):
                column = self.parsed['columns'][item['column']]['data']
                order_list.append((column, item['dir'], mapping[column]))

        return order_list

    def sort_list(self, mapping, list_to_sort):
        kwargs = {}
        for order in self.get_order_by(mapping):
            if order[1] == 'desc':
                kwargs['reverse'] = True
            if order[2]:  # True means it is string
                kwargs['key'] = lambda x: '' if x[order[0]] is None else x[order[0]].lower()
            else:  # False means it is not string
                kwargs['key'] = operator.itemgetter(order[0])
            list_to_sort.sort(**kwargs)
            kwargs.clear()

    def paging(self, object_list, *args, **kwargs):
        paginator = Paginator(object_list=object_list, per_page=self.length, *args, **kwargs)
        try:
            p = paginator.page(self.page)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            p = paginator.page(paginator.num_pages)
        return self.handle_data(p), paginator

    def handle_data(self, data):
        """ Customized by overriding handle_data """
        return list(data)
