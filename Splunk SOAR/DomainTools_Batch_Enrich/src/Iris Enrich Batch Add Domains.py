"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'add_artifact_to_queue' block
    add_artifact_to_queue(container=container)

    return

def add_artifact_to_queue(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("add_artifact_to_queue() called")

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.id","artifact:*.cef.destinationDnsDomain"])

    container_artifact_header_item_0 = [item[0] for item in container_artifact_data]
    container_artifact_cef_item_1 = [item[1] for item in container_artifact_data]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    queue = phantom.get_list(list_name="iris_enrich_batch_queue", column_index=1)
    queued_artifacts = []
    for item in queue[2]:
        queued_artifacts.append(item[0])
    queued_artifacts = set(queued_artifacts)
    phantom.debug(f"dt debug - artifacts in queue: {queued_artifacts}")
    phantom.debug(f"dt debug - artifacts in event: {container_artifact_header_item_0}")
    
    for i in range(len(container_artifact_header_item_0)):
        artifact_id = container_artifact_header_item_0[i]
        domain = container_artifact_cef_item_1[i]
        if str(artifact_id) in queued_artifacts:
            phantom.debug(f"dt debug - not adding artifact: {artifact_id} - {domain} to queue")
        else:
            phantom.debug(f"dt debug - adding artifact: {artifact_id} - {domain} to queue")
            phantom.add_list(list_name="iris_enrich_batch_queue", values=[artifact_id, domain])
    

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