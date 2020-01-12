from flask_table import Table, Col, LinkCol, create_table, NestedTableCol
from flask import url_for
from app.main.utils import table_sorter
from functools import partial

class TestTable(Table):
    border = True
    html_attrs = {"style":'font-size:18px; '} # gets assigned to table header
    column_html_attrs = {'style':'text-align: center; min-width:10px', 'bgcolor':"#FF0000"} # gets assigned to both th and td
    classes = ["table-striped"] # gets assigned to table classes. 
    username = Col('username',column_html_attrs=column_html_attrs)
    age = Col('age',column_html_attrs=column_html_attrs)
    sex = Col('sex',column_html_attrs=column_html_attrs)

class TestWideTable(Table):
    border = True
    html_attrs = {"style":'font-size:18px; overflow-x:auto;'} # gets assigned to table header
    column_html_attrs = {'style':'text-align: center; min-width:10px', 'bgcolor':"#FF0000"} # gets assigned to both th and td
    classes = ["table-striped"] # gets assigned to table classes. 
    username = Col('username',column_html_attrs=column_html_attrs)
    age = Col('age',column_html_attrs=column_html_attrs)
    sex = Col('sex',column_html_attrs=column_html_attrs)

class CheckBoxCol(Col):
    def __init__(self, *args, checked=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.checked = checked

    def td_format(self, content):
        html = '<input type="checkbox" name="{}" value="{}"{}>'.format(content['name'],
                                                                       content['value'],
                                                                       ' checked' if self.checked else '')
        return html

class CheckBoxTable(Table):
    border = True
    html_attrs = {"style":'font-size:18px'} # gets assigned to table header
    column_html_attrs = {'style':'text-align: center; min-width:10px',} # gets assigned to both th and td
    # classes = ["table-striped"] # gets assigned to table classes. 
    channel = Col('channel')
    registration = CheckBoxCol('Registration')
    injection_detection = CheckBoxCol('Injection detection')
    # probe_detection = CheckBoxCol('Probe detection')
    # cell_detection = CheckBoxCol('Cell detection')
    # # channel555 = OptCol('555',choices={True:'Yes',False:'No'},column_html_attrs=column_html_attrs)
        

def create_dynamic_table(contents,name='Dynamic Table', **sort_kwargs):
    def dynamic_sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('main.dynamic_flask_table', sort=col_key, direction=direction)

    options = dict(
        border = True,
        allow_sort = True,
        no_items = "No Samples",
        html_attrs = {"style":'font-size:18px'}, 
        table_id = 'vert_table',
        classes = ["table-striped"]
        ) 

    table_class = create_table(name,options=options)
    table_class.sort_url = dynamic_sort_url
    sort = sort_kwargs.get('sort_by')
    reverse = sort_kwargs.get('sort_reverse')

    table_class.add_column('state',Col('state'))
    if "Mercer" not in contents.fetch('county'):
        table_class.add_column('county',Col('county'))
    sorted_contents = sorted(contents.fetch(as_dict=True),
            key=partial(table_sorter,sort_key=sort),reverse=reverse)
    table = table_class(sorted_contents)
    table.sort_by = sort
    table.sort_reverse = reverse
    
    return table        

class EmptyCol(Col):
    def td_format(self):
        return ''

def create_custom_border_table(contents,name='Dynamic Table', **sort_kwargs):
    def dynamic_sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('main.flask_table_custom_border', sort=col_key, direction=direction)

    def get_tr_attrs(self, item):
        if item:
            return {'style': 'outline: thin solid'}
        else:
            return {}
    options = dict(
        border = True,
        allow_sort = True,
        no_items = "No Samples",
        html_attrs = {"style":'font-size:18px'}, 
        table_id = 'vert_table',
        classes = ["table-striped"]
        ) 

    table_class = create_table(name,options=options)
    table_class.sort_url = dynamic_sort_url
    sort = sort_kwargs.get('sort_by')
    reverse = sort_kwargs.get('sort_reverse')

    table_class.add_column('state',Col('state'))
    table_class.add_column('clearing parameters',EmptyCol('clearing parameters'))
    table_class.add_column('county',Col('county'))
    sorted_contents = sorted(contents.fetch(as_dict=True),
            key=partial(table_sorter,sort_key=sort),reverse=reverse)
    table = table_class(sorted_contents)
    table.sort_by = sort
    table.sort_reverse = reverse
    
    return table        


class CustomTestColumn(Col):
    def td_format(self, content):
        if content == 'yes':
            return 'You betcha'
        elif content == 'no':
            return "No way"
        else:
            return "Other"

class CustomTestTable(Table):
    border = True
    testcol = CustomTestColumn('test column')

class TestTableCustomRows(Table):
    def get_tr_attrs(self, item):
        if item['age'] == 22:
            return {'bgcolor':"#FCA5A4"}
        else:
            return {}
    border = True
    html_attrs = {"style":'font-size:18px'} # gets assigned to table header
    column_html_attrs = {'style':'text-align: center; min-width:10px',} # gets assigned to both th and td
    classes = ["table-striped"] # gets assigned to table classes. 
    username = Col('username',column_html_attrs=column_html_attrs)
    age = Col('age',column_html_attrs=column_html_attrs)
    sex = Col('sex',column_html_attrs=column_html_attrs)
    

def dynamic_table_custom_rows(contents,name='Dynamic Table Custom Rows', **sort_kwargs):

    def dynamic_get_tr_attrs(self, item, reverse=False):
        if item['age'] ==22:
            return {'bgcolor':'#FCA5A4'}
        else:
            return {}        

    options = dict(
        border = True,
        allow_sort = False,
        no_items = "No data",
        html_attrs = {"style":'font-size:18px'}, 
        classes = ["table-striped"]
        ) 

    table_class = create_table(name,options=options)
    table_class.get_tr_attrs = dynamic_get_tr_attrs
    # print(table_class.tr_attrs)
    table_class.add_column('age',Col('age'))
    table_class.add_column('sex',Col('sex'))
    table = table_class(contents)
    return table

class ColOtherItemLookup(Col):

    def td_contents(self, item, attr_list):
        # by default this does
        # print(i)
        if item['age'] < 25:
            return self.td_format(item['sex'])
        else:
            return ""


class TestTableCustomCol(Table):
   
    border = True
    html_attrs = {"style":'font-size:18px'} # gets assigned to table header
    column_html_attrs = {'style':'text-align: center; min-width:10px',} # gets assigned to both th and td
    classes = ["table-striped"] # gets assigned to table classes. 
    username = Col('username',column_html_attrs=column_html_attrs)
    age = Col('age',column_html_attrs=column_html_attrs)
    sex = ColOtherItemLookup('sex',column_html_attrs=column_html_attrs)
    
class LinkColOtherItemLookup(LinkCol):
    
    def td_contents(self, item, attr_list):
        if item['age'] < 25:
            return '<a href="{url}">{text}</a>'.format(
                url=self.url(item),
                text=self.td_format(self.text(item, attr_list)))
        else:
            return ""


class TestTableCustomLinkCol(Table):
   
    border = True
    html_attrs = {"style":'font-size:18px'} # gets assigned to table header
    column_html_attrs = {'style':'text-align: center; min-width:10px',} # gets assigned to both th and td
    classes = ["table-striped"] # gets assigned to table classes. 
    username = Col('username',column_html_attrs=column_html_attrs)
    age = Col('age',column_html_attrs=column_html_attrs)
    sex = LinkColOtherItemLookup('sex',endpoint='main.home',column_html_attrs=column_html_attrs)
    

class SubItemTable(Table):
    border=True
    col1 = Col('Sub-column 1')
    col2 = Col('Sub-column 2')

class ItemTable(Table):
    border=True
    name = Col('Name')
    description = Col('Description')
    subtable = NestedTableCol('Subtable', SubItemTable)

class ItemTableDynamicSubTable(Table):
    border=True
    name = Col('Name')
    description = Col('Description')
    subtable_options = {
    'table_id':'dynamic_subtable',
    'border':True
    }
    subtable_class = create_table('subtable',options=subtable_options)
    subtable_class.add_column('col1',Col('col1'))
    subtable_class.add_column('col2',Col('col2'))
    subtable = NestedTableCol('Subtable', subtable_class)