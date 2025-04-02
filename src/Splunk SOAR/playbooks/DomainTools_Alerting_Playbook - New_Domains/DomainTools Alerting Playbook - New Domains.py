"""
This playbook retrieves domain from a given search hash with built-in “first_seen” param. The flow will continue to retrieve new domains based on the scheduled run
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'load_hash_1' block
    load_hash_1(container=container)

    return

@phantom.playbook_block()
def load_hash_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("load_hash_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "search_hash": "",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("load hash", parameters=parameters, name="load_hash_1", assets=["domaintoolscreds"], callback=parse_new_domains)

    return


@phantom.playbook_block()
def parse_new_domains(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("parse_new_domains() called")

    load_hash_1_result_data = phantom.collect2(container=container, datapath=["load_hash_1:action_result.data"], action_results=results)

    load_hash_1_result_item_0 = [item[0] for item in load_hash_1_result_data]

    parse_new_domains__new_domains = None
    parse_new_domains__new_domains_count = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    # Write your custom code here...
    new_domains = []
    for results in load_hash_1_result_item_0:
        for result in results:
            risk_score = result.get("domain_risk", {}).get("risk_score")
            domain = result.get("domain")
            is_active = result.get("active")
            new_domains.append({"domain": domain, "risk_score": risk_score, "active": is_active})
    
    parse_new_domains__new_domains = new_domains
    parse_new_domains__new_domains_count = len(new_domains)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="parse_new_domains:new_domains", value=json.dumps(parse_new_domains__new_domains))
    phantom.save_run_data(key="parse_new_domains:new_domains_count", value=json.dumps(parse_new_domains__new_domains_count))

    decision_1(container=container)

    return


@phantom.playbook_block()
def create_event(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("create_event() called")

    parse_new_domains__new_domains = json.loads(_ if (_ := phantom.get_run_data(key="parse_new_domains:new_domains")) != "" else "null")  # pylint: disable=used-before-assignment

    create_event__container_id = None
    create_event__out_file_name = None
    create_event__container_name = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    from datetime import datetime
    now = datetime.now().strftime("%Y%m%d")
    container_name = f"new_domains_alert_{now}"
    
    # make sure to create one event per day
    rest_url = phantom.get_rest_base_url()
    response = phantom.requests.get(
        f"{rest_url}container?_filter_name='{container_name}'",
        verify=False,
    )
    result = response.json()
    if result.get("count") > 0: # get the current container
        phantom.debug(f"dt debug - {container_name} container exist. Skipping creation of new event.")
        container_id = result.get("data")[0]["id"]
        container_name = result.get("data")[0]["name"]
    else: # create a new one
        phantom.debug(f"dt debug - creating container {container_name}")
        success, message, container_id = phantom.create_container(name=container_name, label='events')
        container = phantom.get_container(container_id)
        container_name = container.get("name")
        phantom.debug(
            f"dt debug - create container results: success: {success}, message: {message}, container_id: {container_id}")
    
    create_event__container_id = container_id
    create_event__out_file_name = f"new_domains_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    create_event__container_name = container_name
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="create_event:container_id", value=json.dumps(create_event__container_id))
    phantom.save_run_data(key="create_event:out_file_name", value=json.dumps(create_event__out_file_name))
    phantom.save_run_data(key="create_event:container_name", value=json.dumps(create_event__container_name))

    output_new_domains_to_csv(container=container)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["parse_new_domains:custom_function:new_domains_count", ">=", 1]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        create_event(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def output_new_domains_to_csv(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("output_new_domains_to_csv() called")

    parse_new_domains__new_domains = json.loads(_ if (_ := phantom.get_run_data(key="parse_new_domains:new_domains")) != "" else "null")  # pylint: disable=used-before-assignment
    create_event__container_id = json.loads(_ if (_ := phantom.get_run_data(key="create_event:container_id")) != "" else "null")  # pylint: disable=used-before-assignment
    create_event__out_file_name = json.loads(_ if (_ := phantom.get_run_data(key="create_event:out_file_name")) != "" else "null")  # pylint: disable=used-before-assignment
    parse_new_domains__new_domains_count = json.loads(_ if (_ := phantom.get_run_data(key="parse_new_domains:new_domains_count")) != "" else "null")  # pylint: disable=used-before-assignment

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    import csv
    
    file_name = create_event__out_file_name
    phantom.debug(f"dt debug - exporting {parse_new_domains__new_domains_count} to csv file.")
    
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w", newline='') as report_csv_file:
        headers = ["domain", "risk_score", "active"]
        writer = csv.DictWriter(report_csv_file, fieldnames=headers)
        
        writer.writeheader()
        for domain in parse_new_domains__new_domains:
            writer.writerow(domain)
            
    phantom.vault_add(container=create_event__container_id, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)

    ################################################################################
    ## Custom Code End
    ################################################################################

    alert_new_domains_found(container=container)

    return


@phantom.playbook_block()
def alert_new_domains_found(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("alert_new_domains_found() called")

    # set user and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """{0} New Domains found:\n\nFor more details go to Event: {1} > \"Files\" tab > Download '{2}'."""

    # parameter list for template variable replacement
    parameters = [
        "parse_new_domains:custom_function:new_domains_count",
        "create_event:custom_function:container_name",
        "create_event:custom_function:out_file_name"
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=15, name="alert_new_domains_found", parameters=parameters)

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