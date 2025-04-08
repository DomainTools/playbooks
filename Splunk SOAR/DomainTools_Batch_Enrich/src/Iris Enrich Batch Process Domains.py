"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'build_domain_batch' block
    build_domain_batch(container=container)

    return

def build_domain_batch(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("build_domain_batch() called")

    build_domain_batch__domains_to_enrich = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    build_domain_batch__domains_to_enrich = []
    queue = phantom.get_list(list_name="iris_enrich_batch_queue")
    for artifact in queue[2]:
        if artifact[1]:
            phantom.debug(f"dt debug - artifact to enrich: {artifact}")
            build_domain_batch__domains_to_enrich.append(artifact[1])
    phantom.debug(f"dt debug - domain batch: {build_domain_batch__domains_to_enrich}")
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="build_domain_batch:domains_to_enrich", value=json.dumps(build_domain_batch__domains_to_enrich))

    enrich_domain_1(container=container)

    return


def enrich_domain_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("enrich_domain_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    domain_formatted_string = phantom.format(
        container=container,
        template="""{0}\n""",
        parameters=[
            ""
        ])

    parameters = []

    if domain_formatted_string is not None:
        parameters.append({
            "domain": domain_formatted_string,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    # @todo figure out how to pass list of domains from previous actions. possibly create temp artifact?
    domains_to_enrich = phantom.get_run_data(key='build_domain_batch:domains_to_enrich')
    domain_string = ','.join(json.loads(domains_to_enrich))

    parameters = []
    parameters.append({'domain': domain_string})

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("enrich domain", parameters=parameters, name="enrich_domain_1", assets=["domaintoolsiriscreds"], callback=save_results)

    return


def save_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("save_results() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    # Write your custom code here...
    playbook_results = {}
    summary = phantom.get_summary()
    phantom.debug(f"dt debug - result summary {summary}")
    
    if result := summary.get("result"):
        for action_result in result:
            if action_run_id := action_result.get("action_run_id"):
                action_results = phantom.get_action_results(action_run_id=action_run_id, flatten=False)
                playbook_results['enrich-process-results'] = action_results
                
                phantom.debug(f"dt debug - action_run_id {action_run_id}")
                phantom.debug(f"dt debug - action_results {action_results}")
                
    
    phantom.save_object(key="iris-enrich-batch-results", value=playbook_results, auto_delete=False, playbook_name="Iris Enrich Batch Process Domains")

    ################################################################################
    ## Custom Code End
    ################################################################################

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