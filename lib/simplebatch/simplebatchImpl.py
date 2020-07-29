# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.execution_engine2Client import execution_engine2

#END_HEADER


class simplebatch:
    '''
    Module Name:
    simplebatch

    Module Description:
    A KBase module: simplebatch
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        #TODO Get this from config
        ee2_url = "http://ci.kbase.us/services/ee2"
        self.ee2 = execution_engine2(url=ee2_url)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_simplebatch(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of type "SimpleBatchParams" -> structure:
           parameter "batch_inputs" of type "batch_params" -> list of type
           "app_params" -> mapping from String to unspecified object,
           parameter "method_name" of String
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_simplebatch
        report = KBaseReport(self.callback_url)

        #TODO Always request WSID?
        #"simpleapp.simple_add"
        method_name = "simpleapp.simple_add" #params['method_name']
        wsid = "TODO"
        #TODO Get Service_Ver
        service_ver = "dev"
        batched_app_params = params['app_params']


        job_ids = []
        statuses = []

        for i,app_param in enumerate(batched_app_params):
            print(f"About to submit job with params {app_param}")
            rjp = {
                "method": method_name,
                "params": [params],
                "service_ver": service_ver,
                "wsid": wsid,
                "app_id": "RanWithBatch",
            }
            try:
                job_id = self.ee2.run_job(params = rjp)
                status = "queued"
            except Exception:
                job_id = "failed to submit"
                status = "failure"

            job_ids.append(job_id)
            statuses.append(status)

        #TODO Create table with refresh buttons or autorefresh, which uses cookie or environment
        # Send this as a report


        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_simplebatch

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_simplebatch return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
