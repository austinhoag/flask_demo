from flask_table import Table, Col, LinkCol

class TestTable(Table):
    border = True
    html_attrs = {"style":'font-size:18px'} # gets assigned to table header
    column_html_attrs = {'style':'text-align: center; min-width:10px', 'bgcolor':"#FF0000"} # gets assigned to both th and td
    classes = ["table-striped"] # gets assigned to table classes. 
    username = Col('username',column_html_attrs=column_html_attrs)
    age = Col('age',column_html_attrs=column_html_attrs)
    sex = Col('sex',column_html_attrs=column_html_attrs)