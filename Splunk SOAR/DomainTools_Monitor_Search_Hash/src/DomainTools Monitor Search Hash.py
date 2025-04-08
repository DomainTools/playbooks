"""
This playbook retrieves domains from a given hash and imports it to an artifact. The flow will continue to import domain from a search hash  based on the run schedule.
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

    phantom.act("load hash", parameters=parameters, name="load_hash_1", assets=["domaintoolscreds"], callback=parse_result)

    return


@phantom.playbook_block()
def import_domains_to_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("import_domains_to_artifact() called")

    parse_result__result_count = json.loads(_ if (_ := phantom.get_run_data(key="parse_result:result_count")) != "" else "null")  # pylint: disable=used-before-assignment
    parse_result__result_data = json.loads(_ if (_ := phantom.get_run_data(key="parse_result:result_data")) != "" else "null")  # pylint: disable=used-before-assignment

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.debug(f"dt debug - Importing {parse_result__result_count} domains to artifact")
    uniquely_added_domains = []
    
    for domain in parse_result__result_data:
        cef_data = {"domain": domain }
        artifact_data = dict(
            name=domain,
            cef=cef_data,
            cef_types= {"domain": ["domain"]},
            container_id=container.get("id"),
            data={},
            label="imported domain",
            run_automation=False,
            severity='low',
            source_data_identifier=domain,
            tags=["monitoring_search_hash"],
            type="domain"
        )
        
        rest_artifact = phantom.build_phantom_rest_url('artifact')
        response_json = phantom.requests.post(rest_artifact, json=artifact_data, verify=False).json()
        if response_json.get('message', '') == 'artifact already exists':
            phantom.debug(f"Artifact already exists: '{response_json['existing_artifact_id']}'")
        else:
            uniquely_added_domains.append(domain)

    phantom.debug(f"dt debug - Imported {len(uniquely_added_domains)} domains to artifacts.")
    ################################################################################
    ## Custom Code End
    ################################################################################

    return


@phantom.playbook_block()
def parse_result(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("parse_result() called")

    load_hash_1_result_data = phantom.collect2(container=container, datapath=["load_hash_1:action_result.summary","load_hash_1:action_result.data"], action_results=results)

    load_hash_1_result_item_0 = [item[0] for item in load_hash_1_result_data]
    load_hash_1_result_item_1 = [item[1] for item in load_hash_1_result_data]

    parse_result__result_count = None
    parse_result__result_data = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.debug(f"dt debug - load hash request status: {success}")
    if success:
        result_count = load_hash_1_result_item_0[0]["Connected Domains Count"]
        result_data = load_hash_1_result_item_1[0]
        
        parse_result__result_count = result_count
        parse_result__result_data = [
            result.get("domain")
            for result in result_data or [{}]
        ]
    else:
        # load hash request succeeds > 5000 results
        err_msg = results[0]["action_results"][0]["message"]
        phantom.error(f"dt error - error on querying search hash param. message: {err_msg}")
        parse_result__result_count = 5001
        parse_result__result_data = err_msg
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="parse_result:result_count", value=json.dumps(parse_result__result_count))
    phantom.save_run_data(key="parse_result:result_data", value=json.dumps(parse_result__result_data))

    decision_2(container=container)

    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_2() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["parse_result:custom_function:result_count", ">", 5000]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        monitoring_hash_error(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    import_domains_to_artifact(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def monitoring_hash_error(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("monitoring_hash_error() called")

    # set user and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "parse_result:custom_function:result_data"
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="monitoring_hash_error", parameters=parameters)

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