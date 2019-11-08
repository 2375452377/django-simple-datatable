# Django easy datatable
[![travis_img]][travis_url]
[![coverage_img]][coverage_url]

datatable Django 后台处理的简易实现

## 快速使用
* 继承 `easy_datatable.forms.DataTableForm` 类，重写 `get_queryset` 方法，返回可以被 `django.core.paginator.Paginator` 类处理的数据
* 如果需要排序功能，重写 `mapping` 字段，`key` 为前端 `datatable` 的数据，表示第几列，`value` 为这列对应 `Modle` 的字段

    ```python
    class UserDataTableForm(DataTableForm):
        mapping = {'0': 'id', '1': 'username'}

        def get_queryset(self):
            return User.objects.values('id', 'username')
    ```
* 继承 `easy_datatable.views.DataTableFormView` 类，重写 `form_class`，`form_class` 必须为 `easy_datatable.forms.DataTableForm` 的子类

    ```python
    class UserDataTableFormView(DataTableFormView):
        form_class = UserDataTableForm
        template_name = 'your_app/your_template.html'
    ```

[travis_url]:https://travis-ci.org/2375452377/django-easy-datatable/
[travis_img]:https://img.shields.io/travis/2375452377/django-easy-datatable/master.svg
[coverage_img]:https://coveralls.io/repos/github/2375452377/django-easy-datatable/badge.svg?branch=master
[coverage_url]:https://coveralls.io/github/2375452377/django-easy-datatable?branch=master
