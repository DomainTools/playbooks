"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'domain_hotlist_feed_1' block
    domain_hotlist_feed_1(container=container)

    return

@phantom.playbook_block()
def domain_hotlist_feed_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("domain_hotlist_feed_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "before": "",
        "session_id": "integrations-testing",
        "top": "",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("domain hotlist feed", parameters=parameters, name="domain_hotlist_feed_1", assets=["domaintoolscreds"], callback=output_domain_risk_list)

    return


@phantom.playbook_block()
def output_domain_risk_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("output_domain_risk_list() called")

    domain_hotlist_feed_1_result_data = phantom.collect2(container=container, datapath=["domain_hotlist_feed_1:action_result.data"], action_results=results)

    domain_hotlist_feed_1_result_item_0 = [item[0] for item in domain_hotlist_feed_1_result_data]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    from datetime import datetime
    import csv
     
    event_name = container.get("name")
    file_name = f"domaintools_feed_domain_hotlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    phantom.debug(f"dt debug - exporting Domain Hotlist to {file_name} file.")
    
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w", newline='') as report_csv_file:
        headers = ["domain", "timestamp", "phishing_risk", "malware_risk", "spam_risk", "proximity_risk", "overall_risk", "expires"]
        writer = csv.DictWriter(report_csv_file, fieldnames=headers)
        
        writer.writeheader()
        for data in domain_hotlist_feed_1_result_item_0[0] or []:
            writer.writerow(data)
            
            # Define the CEF data in a Python dictionary
            cef_data = {
                "destinationDnsDomain": data.get("domain"),
                "timestamp": data.get("timestamp"),
                "phishing_risk": data.get("phishing_risk"),
                "malware_risk": data.get("malware_risk"),
                "spam_risk": data.get("spam_risk"),
                "proximity_risk": data.get("proximity_risk"),
                "overall_risk": data.get("overall_risk"),
                "expires": data.get("expires"),
            }
            # Use the dictionary to create a new artifact
            phantom.add_artifact(
                container=container,
                label="domaintools-realtime-feeds",
                severity="high",
                name="Domain Hotlist Feed",
                cef_data=cef_data
            )

    success, message, vault_id = phantom.vault_add(container=container, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)
    
    if not success:
        phantom.error(f"dt error - Error creating {file_name} file. Message: {message}")
        return


    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_block_result(key="output_domain_risk_list__inputs:0:domain_hotlist_feed_1:action_result.data", value=json.dumps(domain_hotlist_feed_1_result_item_0))

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