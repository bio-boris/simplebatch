/*
A KBase module: simplebatch
*/

module simplebatch {
    typedef mapping<string,UnspecifiedObject> app_params;
    typedef list<app_params> batch_params;

    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure {
        batch_params batch_inputs;
        string method_name;
    } SimpleBatchParams;


    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_simplebatch(SimpleBatchParams params) returns (ReportResults output) authentication required;

};
