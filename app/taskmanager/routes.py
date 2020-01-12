from flask import (render_template, request, redirect, Blueprint,
                   session, url_for, flash, Markup,Request,
                   jsonify, send_file)
from app import tables
import time
import pandas as pd
import logging
from datetime import datetime
from app import db_admin, cel
import paramiko
# from app import cel
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

''' Make the file handler to deal with logging to file '''
file_handler = logging.FileHandler('logs/taskmanager_routes.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler() # level already set at debug from logger.setLevel() above

stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

taskmanager = Blueprint('taskmanager',__name__)

@taskmanager.route("/submit_job") 
def submit_jobs(): 
    command = """sbatch --parsable test_slurm_scripts/submit.sh """ 
    port = 22
    username = 'ahoag'
    hostname = 'spock.pni.princeton.edu'
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        
        client.connect(hostname, port=port, username=username, allow_agent=False,look_for_keys=True)

        stdin, stdout, stderr = client.exec_command(command)
        stdout_str = stdout.read().decode("utf-8").strip('\n')
        jobid = int(stdout_str)
        print(jobid)
        # jobid = 16046124
        status = 'SUBMITTED'
        entry_dict = {'jobid':jobid,'username':username,'status':status}
        db_admin.SpockJobManager.insert1(entry_dict)    
    finally:
        client.close()

    return "Job submitted"
    # return redirect(url_for('main.home'))

@cel.task()
def status_checker():
    query = db_admin.SpockJobManager() & 'status!="COMPLETED"' & 'status!="FAILED"'
    jobids = query.fetch('jobid')
    jobid = jobids[-1]
    port = 22
    username = 'ahoag'
    hostname = 'spock.pni.princeton.edu'
    command = """sacct -b -P -n -a  -j {} | head -1 | cut -d "|" -f2 """.format(jobid)
    
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        
        client.connect(hostname, port=port, username=username, allow_agent=False,look_for_keys=True)

        stdin, stdout, stderr = client.exec_command(command)
        
        stdout_str = stdout.read().decode("utf-8").strip('\n')
        print(stdout_str)
        
        # jobid = 16046124
        # status = 'SUBMITTED'
        # entry_dict = {'jobid':jobid,'username':username,'status':status}
        # db_admin.SpockJobManager.insert1(entry_dict)    
    finally:
        client.close()
    return stdout_str
    # return (str(jobid),stdout_str)
    # return f"Status for jobids {jobids} checked"

@taskmanager.route("/check_all_statuses") 
def check_all_statuses():
    # query = db_admin.SpockJobManager() & 'status!="COMPLETED"' & 'status!="FAILED"'
    # jobids = 
    # jobids = query.fetch('jobid')
    # jobid = jobids[-1]
    jobids_str = '16046124,16046126,16046129'
    port = 22
    username = 'ahoag'
    hostname = 'spock.pni.princeton.edu'
    time_start = time.time()
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        
        client.connect(hostname, port=port, username=username, allow_agent=False,look_for_keys=True)
        # jobids_str = ','.join(str(jobid) for jobid in jobids)
        # for jobid in jobids:
            # command += """sacct -b -P -n -a  -j {} | head -1 | cut -d "|" -f2; """.format(jobid)
        command = """sacct -X -b -P -n -a  -j {} | cut -d "|" -f2""".format(jobids_str)
        stdin, stdout, stderr = client.exec_command(command)
        stdout_str = stdout.read().decode("utf-8").replace('\n',',')
        status_codes = stdout_str.split(',')
        
        # jobid = 16046124
        # status = 'SUBMITTED'
        # entry_dict = {'jobid':jobid,'username':username,'status':status}
        # db_admin.SpockJobManager.insert1(entry_dict)    
    finally:
        client.close()
    time_end = time.time()
    print(f"Took {time_end-time_start} seconds" )
    return stdout_str
    # return (str(jobid),stdout_str)
    # return f"Status for jobids {jobids} checked"
