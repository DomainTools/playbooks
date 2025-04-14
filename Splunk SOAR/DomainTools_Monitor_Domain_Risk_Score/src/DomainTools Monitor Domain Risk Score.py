"""
This playbook retrieves the risk score for a domain and stores it in a custom list. The flow will continue to monitor the domain for changes to the risk score based on the run schedule.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_monitored_domains_list' block
    get_monitored_domains_list(container=container)

    return

@phantom.playbook_block()
def get_riskscore_threshold(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_riskscore_threshold() called")

    get_riskscore_threshold__riskscore_threshold = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    _, _, riskscore_threshold = phantom.get_list(list_name='domaintools_riskscore_threshold', values='riskscore_threshold')
    get_riskscore_threshold__riskscore_threshold = riskscore_threshold['matches'][0]['value'][1]
    phantom.debug(f"dt debug - current risk score threshold is: {get_riskscore_threshold__riskscore_threshold}")

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_riskscore_threshold:riskscore_threshold", value=json.dumps(get_riskscore_threshold__riskscore_threshold))

    decision_1(container=container)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["get_monitored_domains_list:custom_function:domain_monitored_count", "==", 0]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        no_domain_monitored_risk_score_prompt(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'elif' condition 2
    found_match_2 = phantom.decision(
        container=container,
        logical_operator="and",
        conditions=[
            ["get_monitored_domains_list:custom_function:domain_monitored_count", ">", 0],
            ["get_monitored_domains_list:custom_function:domain_monitored_count", "<=", 100]
        ])

    # call connected blocks if condition 2 matched
    if found_match_2:
        iris_ivestigate_or_enrich(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'elif' condition 3
    found_match_3 = phantom.decision(
        container=container,
        conditions=[
            ["get_monitored_domains_list:custom_function:domain_monitored_count", ">", 100]
        ])

    # call connected blocks if condition 3 matched
    if found_match_3:
        max_limit_domain_monitored_prompt(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def no_domain_monitored_risk_score_prompt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("no_domain_monitored_risk_score_prompt() called")

    # set user and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """Please add at least 1 domain to be monitored. Current count is {0}.\n"""

    # parameter list for template variable replacement
    parameters = [
        "get_monitored_domains_count:custom_function:monitored_domain_count"
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="no_domain_monitored_risk_score_prompt", parameters=parameters)

    return


@phantom.playbook_block()
def max_limit_domain_monitored_prompt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("max_limit_domain_monitored_prompt() called")

    # set user and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """Reduce the number of domains. Max is 100."""

    # parameter list for template variable replacement
    parameters = []

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="max_limit_domain_monitored_prompt", parameters=parameters)

    return


@phantom.playbook_block()
def get_monitored_domains_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_monitored_domains_list() called")

    get_monitored_domains_list__domain_monitored_list = None
    get_monitored_domains_list__domain_monitored_count = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    _, _, domain_monitored_list = phantom.get_list(list_name='domaintools_monitored_domains_risk_score')
    get_monitored_domains_list__domain_monitored_list = domain_monitored_list[1:]
    get_monitored_domains_list__domain_monitored_count = len(get_monitored_domains_list__domain_monitored_list)
    phantom.debug(f"dt debug - currently monitoring {get_monitored_domains_list__domain_monitored_count} domains.")

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_monitored_domains_list:domain_monitored_list", value=json.dumps(get_monitored_domains_list__domain_monitored_list))
    phantom.save_run_data(key="get_monitored_domains_list:domain_monitored_count", value=json.dumps(get_monitored_domains_list__domain_monitored_count))

    get_riskscore_threshold(container=container)

    return


@phantom.playbook_block()
def iris_ivestigate_or_enrich(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("iris_ivestigate_or_enrich() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # You can manually select DT action to used. It can be lookup domain (Iris Investigate) 
    # or enrich domain (Iris Enrich)
    ################################################################################

    parameters = []

    parameters.append({
        "domain": "",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    domain_monitored_list = json.loads(_ if (_ := phantom.get_run_data(key="get_monitored_domains_list:domain_monitored_list")) != "" else "[]") # pylint: disable=used-before-assignment
    parameters = [{"domain": ",".join([domain[0] for domain in domain_monitored_list])}]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("lookup domain", parameters=parameters, name="iris_ivestigate_or_enrich", assets=["domaintoolscreds"], callback=get_current_domain_risk_value)

    return


@phantom.playbook_block()
def get_current_domain_risk_value(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_current_domain_risk_value() called")

    get_monitored_domains_list__domain_monitored_list = json.loads(_ if (_ := phantom.get_run_data(key="get_monitored_domains_list:domain_monitored_list")) != "" else "null")  # pylint: disable=used-before-assignment

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    iris_results = phantom.collect2(
        container=container, 
        datapath=["iris_ivestigate_or_enrich:action_result.data"], 
        action_results=results
    )
    domain_results = {}
    # will unpack the list as the result from collect2 is a list[list[list[dict[any,any]]]]
    # e.g. from this [[[{"sample": "structure"}]]] to [{}]
    results = list(*iris_results[0])
    for result in results:
        domain_name = result.get("domain")
        if domain_name not in domain_results:
            domain_results[domain_name] = {"risk_score": result.get("domain_risk", {}).get("risk_score")}
                
    # get the current domain risk score value
    # then update the current risk score column
    from datetime import datetime
    
    updated_list = []
    for domain in get_monitored_domains_list__domain_monitored_list or []:
        d_name, prev_score, current_score, last_updated = domain
        row = domain
        
        if latest_domain_score := domain_results.get(d_name):
            new_risk_score = latest_domain_score.get("risk_score") or 0
            try:
                # safely convert it to int
                current_score = int(current_score)
            except:
                pass
            
            row = [d_name, current_score, new_risk_score, last_updated]
            # only update when new risk score is not equal to current risk score
            if new_risk_score != current_score:
                new_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row[3] = new_last_updated
            
            # update the current and previous score if prev score is empty
            # assuming it's the playbook first run
            if prev_score in ["", None]:
                row[1] = new_risk_score

        updated_list.append(row)
        
    # update the domain monitored list
    headers = ["domain_name", "prev_risk_score", "current_risk_score", "last_updated"]
    updated_list.insert(0, headers)

    success, _ = phantom.set_list(list_name="domaintools_monitored_domains_risk_score", values=updated_list)
    phantom.debug(f"phantom.set_list results: success: {success}")
 
    ################################################################################
    ## Custom Code End
    ################################################################################

    check_risk_score_change(container=container)

    return


@phantom.playbook_block()
def check_risk_score_change(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("check_risk_score_change() called")

    get_riskscore_threshold__riskscore_threshold = json.loads(_ if (_ := phantom.get_run_data(key="get_riskscore_threshold:riskscore_threshold")) != "" else "null")  # pylint: disable=used-before-assignment

    check_risk_score_change__higher_than_threshold_domains = None
    check_risk_score_change__higher_than_threshold_domains_count = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    higher_than_threshold_domains = []
    _, _, domain_monitored_list = phantom.get_list(list_name='domaintools_monitored_domains_risk_score')
    
    domain_monitored_list = domain_monitored_list[1:]
    for domain in domain_monitored_list or []:
        name, prev_score, current_score, last_updated = domain
        # use try catch to safely convert string to float
        try: 
            prev_score = float(prev_score)
            current_score = float(current_score)
        except ValueError:
            prev_score, current_score = 0, 0
        
        # check if within threshold
        diff = abs(float(current_score) - float(prev_score))
        if diff > float(get_riskscore_threshold__riskscore_threshold or 0):
            higher_than_threshold_domains.append(domain)
    
    check_risk_score_change__higher_than_threshold_domains = higher_than_threshold_domains
    check_risk_score_change__higher_than_threshold_domains_count = len(higher_than_threshold_domains)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="check_risk_score_change:higher_than_threshold_domains", value=json.dumps(check_risk_score_change__higher_than_threshold_domains))
    phantom.save_run_data(key="check_risk_score_change:higher_than_threshold_domains_count", value=json.dumps(check_risk_score_change__higher_than_threshold_domains_count))

    decision_2(container=container)

    return


@phantom.playbook_block()
def send_merge_result(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("send_merge_result() called")

    check_risk_score_change__higher_than_threshold_domains = json.loads(_ if (_ := phantom.get_run_data(key="check_risk_score_change:higher_than_threshold_domains")) != "" else "null")  # pylint: disable=used-before-assignment

    send_merge_result__merge_results = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    alerts = []
    message_body_template = "Domain: {domain}, Previous Risk Score: {prev_score}, Current Risk Score: {current_score}"
    for domain in check_risk_score_change__higher_than_threshold_domains or []:
        name, prev_score, current_score, last_updated = domain
        alerts.append(message_body_template.format(domain=name, prev_score=prev_score, current_score=current_score))
    
    send_merge_result__merge_results = "\n".join(alerts)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="send_merge_result:merge_results", value=json.dumps(send_merge_result__merge_results))

    monitored_domains_risk_score_change_prompt(container=container)

    return


@phantom.playbook_block()
def monitored_domains_risk_score_change_prompt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("monitored_domains_risk_score_change_prompt() called")

    # set user and message variables for phantom.prompt call

    user = container.get('owner_name', None)
    role = None
    message = """The score was change as deteremined by the threshold for the following domains:\n{0}"""

    # parameter list for template variable replacement
    parameters = [
        "send_merge_result:custom_function:merge_results"
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="monitored_domains_risk_score_change_prompt", parameters=parameters)

    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_2() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["check_risk_score_change:custom_function:higher_than_threshold_domains_count", ">", 0]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        send_merge_result(action=action, success=success, container=container, results=results, handle=handle)
        return

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