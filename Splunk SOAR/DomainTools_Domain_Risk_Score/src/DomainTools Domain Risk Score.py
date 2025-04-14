"""
This playbook retrieves the Domain Risk Score and throws an Alert for the Analyst to manually review the domain artifact. Users can block the domain.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'domain_reputation' block
    domain_reputation(container=container)

    return

@phantom.playbook_block()
def domain_reputation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("domain_reputation() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "domain": "",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Manually add the custom artifact datapath from this list. It should be in alphabetical order to make it work
    datapaths = ["artifact:*.cef.destinationDnsDomain","artifact:*.cef.domain","artifact:*.id"]
    
    # Indices below are based on the position of the element in the `datapaths` variable above
    DESTINATION_DNS_DOMAIN_ARTIFACT_INDEX = 0
    DOMAIN_ARTIFACT_INDEX = 1
    ARTIFACT_ID_INDEX = 2

    container_artifact_data = phantom.collect2(container=container, datapath=datapaths)

    # Empty `parameters` variable
    parameters = []

    # build parameters list for 'domain_reputation' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[DESTINATION_DNS_DOMAIN_ARTIFACT_INDEX] is not None:
            parameters.append({
                "domain": container_artifact_item[DESTINATION_DNS_DOMAIN_ARTIFACT_INDEX],
                "context": {'artifact_id': container_artifact_item[ARTIFACT_ID_INDEX]},
            })
        elif container_artifact_item[DOMAIN_ARTIFACT_INDEX] is not None:
            parameters.append({
                "domain": container_artifact_item[DOMAIN_ARTIFACT_INDEX],
                "context": {'artifact_id': container_artifact_item[ARTIFACT_ID_INDEX]},
            })

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("domain reputation", parameters=parameters, name="domain_reputation", assets=["domaintoolscreds"], callback=get_min_risk_score)

    return


@phantom.playbook_block()
def get_min_risk_score(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_min_risk_score() called")

    get_min_risk_score__min_risk_score = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    success, message, min_risk_score = phantom.get_list(list_name='domaintools_domain_risk', values="min_risk_score")
    get_min_risk_score__min_risk_score = min_risk_score['matches'][0]['value'][1]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_min_risk_score:min_risk_score", value=json.dumps(get_min_risk_score__min_risk_score))

    decision_1(container=container)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["domain_reputation:action_result.summary.domain_risk", ">=", "get_min_risk_score:custom_function:min_risk_score"]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        high_risk_domain_spotted(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def high_risk_domain_spotted(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("high_risk_domain_spotted() called")

    # set user and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """Heads up, High-Risk Domain Alert! {1}{0} has a score of {1}{0}{1}"""

    # parameter list for template variable replacement
    parameters = [
        "domain_reputation:action_result.parameter.domain",
        "domain_reputation:action_result.summary.domain_risk"
    ]

    # responses
    response_types = [
        {
            "prompt": "",
            "options": {
                "type": "message",
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="high_risk_domain_spotted", parameters=parameters, response_types=response_types)

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