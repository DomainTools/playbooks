"""
This playbook retrieves the Iris Investigate profile of a domain and automatically flags domains that have been tagged as malicious in DomainTools Iris. The list of malicious tags are configurable by the analyst and can be kept up to date for automation
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'domain_iris_lookup' block
    domain_iris_lookup(container=container)

    return

@phantom.playbook_block()
def domain_iris_lookup(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("domain_iris_lookup() called")

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

    phantom.act("lookup domain", parameters=parameters, name="domain_iris_lookup", assets=["domaintoolscreds"], callback=decision_1)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        logical_operator="and",
        conditions=[
            ["domain_iris_lookup:action_result.data.*.tags.*.label", "in", "custom_list:iris_malicious_tags"],
            ["artifact:*.severity", "not in", ["High"]]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        return

    return

@phantom.playbook_block()
def set_severity_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("set_severity_1() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.set_severity(container=container, severity="high")

    container = phantom.get_container(container.get('id', None))

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