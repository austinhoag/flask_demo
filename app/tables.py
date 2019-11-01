from flask_table import Table, Col, LinkCol

class TestTable(Table):
    border = True
    html_attrs = {"style":'font-size:18px'} # gets assigned to table header
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
        