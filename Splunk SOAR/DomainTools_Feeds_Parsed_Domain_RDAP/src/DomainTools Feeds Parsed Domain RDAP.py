"""
Domain Discovery feeds playbook
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'parsed_domain_rdap_feed' block
    parsed_domain_rdap_feed(container=container)

    return

@phantom.playbook_block()
def parsed_domain_rdap_feed(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("parsed_domain_rdap_feed() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "session_id": "dt-integrations",
        "top": 3,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("domain rdap feed", parameters=parameters, name="parsed_domain_rdap_feed", assets=["domaintoolscreds"], callback=output_parsed_domain_rdap_list)

    return


@phantom.playbook_block()
def output_parsed_domain_rdap_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("output_parsed_domain_rdap_list() called")

    parsed_domain_rdap_feed_result_data = phantom.collect2(container=container, datapath=["parsed_domain_rdap_feed:action_result.data"], action_results=results)

    parsed_domain_rdap_feed_result_item_0 = [item[0] for item in parsed_domain_rdap_feed_result_data]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    from datetime import datetime
    import csv
     
    event_name = container.get("name")
    file_name = f"domaintools_feed_parsed_domain_rdap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    phantom.debug(f"dt debug - exporting Parsed Domain RDAP list to {file_name} file.")
    
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w", newline='') as report_csv_file:
        headers = ["domain", "timestamp", "parsed_record"]
        writer = csv.DictWriter(report_csv_file, fieldnames=headers)
        
        writer.writeheader()
        for data in parsed_domain_rdap_feed_result_item_0[0] or []:
            final_row = {
                "domain": data.get("domain"),
                "timestamp": data.get("timestamp"),
                "parsed_record": data.get("parsed_record", {}).get("parsed_fields")
            } 
            writer.writerow(final_row)

    success, message, vault_id = phantom.vault_add(container=container, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)
    
    if not success:
        phantom.error(f"dt error - Error creating {file_name} file. Message: {message}")
        return

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_block_result(key="output_parsed_domain_rdap_list__inputs:0:parsed_domain_rdap_feed:action_result.data", value=json.dumps(parsed_domain_rdap_feed_result_item_0))

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