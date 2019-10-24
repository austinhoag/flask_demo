import datajoint as dj

dj.config['database.host'] = '127.0.0.1'
dj.config['database.port'] = 3306

dj.config['database.user'] = 'ahoag'
dj.config['database.password'] = 'p@sswd'

schema = dj.schema('ahoag_flask_demo') 
schema.drop(force=True)
schema = dj.schema('ahoag_flask_demo')

@schema
class State(dj.Lookup):
    definition = """
    # Users of the light sheet microscope
    state: varchar(20)   
    ---
    """
    contents =  [
        ['California'],['Connecticut'],['New Jersey'],['Maine']
    ] 

@schema
class County(dj.Lookup):
    definition = """
    # Users of the light sheet microscope
    county: varchar(20)  
    ---
    -> State
    """
    contents =  [
        ['Yolo','California'],['Los Angeles','California'],['Mercer','New Jersey']
    ] 

print("Successfully created ahoag_flask_demo schema")
  
