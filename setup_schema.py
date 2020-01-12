import datajoint as dj

dj.config['database.host'] = '127.0.0.1'
dj.config['database.port'] = 3306

dj.config['database.user'] = 'ahoag'
dj.config['database.password'] = 'p@sswd'

# schema = dj.schema('ahoag_flask_demo') 
# schema.drop(force=True)
# schema = dj.schema('ahoag_flask_demo')

from schemas import admin
