"""
This playbook call iris ivestigate api with a given &quot;tag&quot;. Check active domains with high risk score then alerts user and outputs all high risk domains in a csv file. \n\nThe flow will continue to retrieve new domains based on the scheduled run
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_iris_tags' block
    get_iris_tags(container=container)

    return

@phantom.playbook_block()
def get_iris_tags(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_iris_tags() called")

    get_iris_tags__iris_tags = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    success, message, iris_tags = phantom.get_list(list_name='domaintools_monitor_iris_tags', values="tags")
    tags = iris_tags['matches'][0]['value'][1]
    if not tags:
        phantom.error("dt debug - you must add atleast one(1) tag in domaintools_monitor_iris_tags list.")
        return
    get_iris_tags__iris_tags = tags
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_iris_tags:iris_tags", value=json.dumps(get_iris_tags__iris_tags))

    pivot_action_1(container=container)

    return


@phantom.playbook_block()
def pivot_action_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_action_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "status": "Any",
        "pivot_type": "",
        "query_value": "",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    parameters = []
    iris_tags = json.loads(phantom.get_run_data(key="get_iris_tags:iris_tags"))
    parameters.append({
        "status": "Any",
        "pivot_type": "tagged_with_any",
        "query_value": iris_tags
    })
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_action_1", assets=["domaintoolscreds"], callback=check_risk_score)

    return


@phantom.playbook_block()
def check_risk_score(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("check_risk_score() called")

    pivot_action_1_result_data = phantom.collect2(container=container, datapath=["pivot_action_1:action_result.data"], action_results=results)

    pivot_action_1_result_item_0 = [item[0] for item in pivot_action_1_result_data]

    check_risk_score__high_risk_domains = None
    check_risk_score__high_risk_domains_count = None
    check_risk_score__dt_min_risk_score = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    queried_domains = []
    for results in pivot_action_1_result_item_0:
        for result in results:
            risk_score = result.get("domain_risk", {}).get("risk_score")
            domain = result.get("domain")
            is_active = result.get("active")
            queried_domains.append({"domain": domain, "risk_score": risk_score, "active": is_active})
            
    phantom.debug(f"dt debug - checking {len(queried_domains)} domains from iris investigate.")
    
    success, message, min_risk_score = phantom.get_list(list_name='domaintools_domain_risk', values="min_risk_score")
    domaintools_min_risk_score = int(min_risk_score['matches'][0]['value'][1])
    
    high_risk_domains = []
    for domain in queried_domains:
        risk_score = int(domain.get("risk_score"))
        is_active = domain.get("active")
        
        if risk_score >= domaintools_min_risk_score and is_active:
            high_risk_domains.append(domain)
        
    check_risk_score__high_risk_domains = high_risk_domains
    check_risk_score__high_risk_domains_count = len(high_risk_domains)
    check_risk_score__dt_min_risk_score = domaintools_min_risk_score
    phantom.debug(f"dt debug - Found {check_risk_score__high_risk_domains_count} high risk domain(s).")
    
       
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="check_risk_score:high_risk_domains", value=json.dumps(check_risk_score__high_risk_domains))
    phantom.save_run_data(key="check_risk_score:high_risk_domains_count", value=json.dumps(check_risk_score__high_risk_domains_count))
    phantom.save_run_data(key="check_risk_score:dt_min_risk_score", value=json.dumps(check_risk_score__dt_min_risk_score))

    decision_1(container=container)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["check_risk_score:custom_function:high_risk_domains_count", ">=", 1]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        output_high_risk_domains(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def output_high_risk_domains(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("output_high_risk_domains() called")

    check_risk_score__high_risk_domains = json.loads(_ if (_ := phantom.get_run_data(key="check_risk_score:high_risk_domains")) != "" else "null")  # pylint: disable=used-before-assignment
    check_risk_score__out_filename = json.loads(_ if (_ := phantom.get_run_data(key="check_risk_score:out_filename")) != "" else "null")  # pylint: disable=used-before-assignment
    check_risk_score__high_risk_domains_count = json.loads(_ if (_ := phantom.get_run_data(key="check_risk_score:high_risk_domains_count")) != "" else "null")  # pylint: disable=used-before-assignment

    output_high_risk_domains__out_filename = None
    output_high_risk_domains__event_name = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    from datetime import datetime
    import csv
     
    event_name = container.get("name")
    file_name = f"alert_high_risk_score_domains_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    phantom.debug(f"dt debug - exporting {check_risk_score__high_risk_domains_count} domain to csv file.")
    
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w", newline='') as report_csv_file:
        headers = ["domain", "risk_score", "active"]
        writer = csv.DictWriter(report_csv_file, fieldnames=headers)
        
        writer.writeheader()
        for domain in check_risk_score__high_risk_domains or []:
            writer.writerow(domain)
            
    success, message, vault_id = phantom.vault_add(container=container, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)
    phantom.debug(f"dt debug - {message}")
    
    if not success:
        phantom.error(f"dt error - Error creating {file_name} file. Message: {message}")
        return
    
    output_high_risk_domains__out_filename = file_name
    output_high_risk_domains__event_name = event_name
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="output_high_risk_domains:out_filename", value=json.dumps(output_high_risk_domains__out_filename))
    phantom.save_run_data(key="output_high_risk_domains:event_name", value=json.dumps(output_high_risk_domains__event_name))

    alert_high_risk_domain(container=container)

    return


@phantom.playbook_block()
def alert_high_risk_domain(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("alert_high_risk_domain() called")

    # set user and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """Found {0} domain with risk score >= {1}. For more details go to Event: {2} > \"Files\" tab > Download '{3}'.\n"""

    # parameter list for template variable replacement
    parameters = [
        "check_risk_score:custom_function:high_risk_domains_count",
        "check_risk_score:custom_function:dt_min_risk_score",
        "output_high_risk_domains:custom_function:event_name",
        "output_high_risk_domains:custom_function:out_filename"
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="alert_high_risk_domain", parameters=parameters)

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