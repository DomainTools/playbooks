"""
NAD feeds playbook
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'nad_feed_1' block
    nad_feed_1(container=container)

    return

@phantom.playbook_block()
def nad_feed_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("nad_feed_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "session_id": "dt-integrations",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("nad feed", parameters=parameters, name="nad_feed_1", assets=["domaintoolscreds"], callback=output_nad_list)

    return


@phantom.playbook_block()
def output_nad_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("output_nad_list() called")

    nad_feed_1_result_data = phantom.collect2(container=container, datapath=["nad_feed_1:action_result.data"], action_results=results)

    nad_feed_1_result_item_0 = [item[0] for item in nad_feed_1_result_data]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    from datetime import datetime
    import csv
     
    event_name = container.get("name")
    file_name = f"domaintools_feed_nad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    phantom.debug(f"dt debug - exporting NAD list to {file_name} file.")
    
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w", newline='') as report_csv_file:
        headers = ["domain", "timestamp"]
        writer = csv.DictWriter(report_csv_file, fieldnames=headers)
        
        writer.writeheader()
        for data in nad_feed_1_result_item_0[0] or []:
            writer.writerow(data)

    success, message, vault_id = phantom.vault_add(container=container, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)
    
    if not success:
        phantom.error(f"dt error - Error creating {file_name} file. Message: {message}")
        return
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return