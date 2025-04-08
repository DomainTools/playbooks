"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'playbook_iris_enrich_batch_process_domains_1' block
    playbook_iris_enrich_batch_process_domains_1(container=container)

    return

def playbook_iris_enrich_batch_process_domains_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("playbook_iris_enrich_batch_process_domains_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/Iris Enrich Batch Process Domains", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/Iris Enrich Batch Process Domains", container=container, name="playbook_iris_enrich_batch_process_domains_1", callback=alert_high_risk)

    return


def alert_high_risk(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("alert_high_risk() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    # get risk threshold
    success, message, min_risk_score = phantom.get_list(list_name='domaintools_domain_risk', values="min_risk_score")
    min_risk_score = int(min_risk_score['matches'][0]['value'][1])
    
    # get enrich data
    object_data = phantom.get_object(key="iris-enrich-batch-results", playbook_name="Iris Enrich Batch Process Domains")
    phantom.debug(f"dt debug - example playbook retrieved object data: {object_data}")

    # collect high risk domains
    enrich_results = object_data.pop().get('value', {}).get('enrich-process-results')
    action_results = enrich_results.pop().get('action_results').pop().get('data', [])
    high_risk_domains = {}
    phantom.debug(f"dt debug - example playbook batch enrich playbook results: {enrich_results}")

    for result in action_results:
        domain_name = result.get("domain")
        risk_score = result.get("domain_risk", {}).get("risk_score")
        if risk_score > min_risk_score:
            high_risk_domains[domain_name] = risk_score
    
    # build alerts
    alerts = []
    for domain, risk_score in high_risk_domains.items():
        alerts.append(f"Domain: {domain}, Risk Score: {risk_score}")
    phantom.debug(f"dt debug - example playbook alerts: {alerts}")
    
                
    # prompt user high risk domains
    user = container.get('owner_name', None)
    role = None
    message = """The score was change as deteremined by the threshold for the following domains:\n{0}"""

    # save merge_results
    alert_formatted = "\n".join(alerts)
    phantom.save_run_data(key="send_merge_result:merge_results", value=json.dumps(alert_formatted))
    
    # parameter list for template variable replacement
    parameters = [
        "send_merge_result:custom_function:merge_results"
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="batch_playbook_example", parameters=parameters)
                

    ################################################################################
    ## Custom Code End
    ################################################################################

    playbook_iris_enrich_clear_queue_1(container=container)

    return


def playbook_iris_enrich_clear_queue_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("playbook_iris_enrich_clear_queue_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/Iris Enrich Clear Queue", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/Iris Enrich Clear Queue", container=container, name="playbook_iris_enrich_clear_queue_1", callback=playbook_iris_enrich_clear_queue_1_callback)

    return


def playbook_iris_enrich_clear_queue_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("playbook_iris_enrich_clear_queue_1_callback() called")

    
    # Downstream End block cannot be called directly, since execution will call on_finish automatically.
    # Using placeholder callback function so child playbook is run synchronously.


    return


def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    ################################################################################
    ## Custom Code End
    ################################################################################

    return