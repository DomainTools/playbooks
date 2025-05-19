"""
NOD feeds playbook
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'noh_feed_1' block
    noh_feed_1(container=container)

    return

@phantom.playbook_block()
def noh_feed_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("noh_feed_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "session_id": "",
        "after": -60,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("noh feed", parameters=parameters, name="noh_feed_1", assets=["domaintoolscreds"], callback=output_noh_list)

    return


@phantom.playbook_block()
def output_noh_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("output_noh_list() called")

    noh_feed_1_result_data = phantom.collect2(container=container, datapath=["noh_feed_1:action_result.data"], action_results=results)

    noh_feed_1_result_item_0 = [item[0] for item in noh_feed_1_result_data]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    from datetime import datetime
    import csv
     
    event_name = container.get("name")
    file_name = f"domaintools_feed_noh_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    phantom.debug(f"dt debug - exporting NOH list to {file_name} file.")
    
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w", newline='') as report_csv_file:
        headers = ["domain", "timestamp"]
        writer = csv.DictWriter(report_csv_file, fieldnames=headers)
        
        writer.writeheader()
        for data in noh_feed_1_result_item_0[0] or []:
            writer.writerow(data)

    success, message, vault_id = phantom.vault_add(container=container, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)
    
    if not success:
        phantom.error(f"dt error - Error creating {file_name} file. Message: {message}")
        return
    

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_block_result(key="output_noh_list__inputs:0:noh_feed_1:action_result.data", value=json.dumps(noh_feed_1_result_item_0))

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