"""
This playbook retrieves the Iris Investigate profile of domain and automatically identifies potential connected infrastructure related to artifacts based on DomainTools Guided Pivot value. The pivot value is set based off of a configurable custom list.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'iris_investigate' block
    iris_investigate(container=container)

    return

@phantom.playbook_block()
def iris_investigate(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("iris_investigate() called")

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

    phantom.act("lookup domain", parameters=parameters, name="iris_investigate", assets=["domaintoolscreds"], callback=get_data_from_custom_list)

    return


@phantom.playbook_block()
def get_data_from_custom_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_data_from_custom_list() called")

    get_data_from_custom_list__max_registrant_contact_name_count = None
    get_data_from_custom_list__max_registrant_org_count = None
    get_data_from_custom_list__max_ssl_info_organization_count = None
    get_data_from_custom_list__max_ssl_info_hash_count = None
    get_data_from_custom_list__max_name_server_host_count = None
    get_data_from_custom_list__max_soa_email_count = None
    get_data_from_custom_list__max_ip_address_count = None
    get_data_from_custom_list__max_name_server_ip_count = None
    get_data_from_custom_list__max_mx_ip_count = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    success, message, domaintools_guided_pivot_list = phantom.get_list(list_name='domaintools_guided_pivot')
    for data in domaintools_guided_pivot_list:
        key = data[0]
        value = data[1]
        
        if key == "max_registrant_contact_name_count":
            get_data_from_custom_list__max_registrant_contact_name_count = value
        elif key == "max_registrant_org_count":
            get_data_from_custom_list__max_registrant_org_count = value
        elif key == "max_ssl_info_organization_count":
            get_data_from_custom_list__max_ssl_info_organization_count = value
        elif key == "max_ssl_info_hash_count":
            get_data_from_custom_list__max_ssl_info_hash_count = value
        elif key == "max_name_server_host_count":
            get_data_from_custom_list__max_name_server_host_count = value
        elif key == "max_soa_email_count":
            get_data_from_custom_list__max_soa_email_count = value
        elif key == "max_ip_address_count":
            get_data_from_custom_list__max_ip_address_count = value
        elif key == "max_name_server_ip_count":
            get_data_from_custom_list__max_name_server_ip_count = value
        elif key == "max_mx_ip_count":
            get_data_from_custom_list__max_mx_ip_count = value

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_data_from_custom_list:max_registrant_contact_name_count", value=json.dumps(get_data_from_custom_list__max_registrant_contact_name_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_registrant_org_count", value=json.dumps(get_data_from_custom_list__max_registrant_org_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_ssl_info_organization_count", value=json.dumps(get_data_from_custom_list__max_ssl_info_organization_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_ssl_info_hash_count", value=json.dumps(get_data_from_custom_list__max_ssl_info_hash_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_name_server_host_count", value=json.dumps(get_data_from_custom_list__max_name_server_host_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_soa_email_count", value=json.dumps(get_data_from_custom_list__max_soa_email_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_ip_address_count", value=json.dumps(get_data_from_custom_list__max_ip_address_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_name_server_ip_count", value=json.dumps(get_data_from_custom_list__max_name_server_ip_count))
    phantom.save_run_data(key="get_data_from_custom_list:max_mx_ip_count", value=json.dumps(get_data_from_custom_list__max_mx_ip_count))

    decision_ns_domain(container=container)
    filter_registrant_name(container=container)
    filter_registrant_org(container=container)
    filter_ssl_org(container=container)
    filter_ssl_hash(container=container)
    filter_soa_email(container=container)
    filter_ip_address(container=container)
    filter_ns_ip(container=container)
    filter_mx_ip(container=container)

    return


@phantom.playbook_block()
def decision_ns_domain(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_ns_domain() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.name_server.*.host.count", "<=", "get_data_from_custom_list:custom_function:max_name_server_host_count"],
            ["iris_investigate:action_result.data.*.name_server.*.host.count", ">", 1]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        pivot_ns_hostname(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def pivot_ns_hostname(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_ns_hostname() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    iris_investigate_result_data = phantom.collect2(container=container, datapath=["iris_investigate:action_result.data.*.name_server.*.host.value","iris_investigate:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'pivot_ns_hostname' call
    for iris_investigate_result_item in iris_investigate_result_data:
        if iris_investigate_result_item[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "nameserver_host",
                "create_date": "",
                "query_value": iris_investigate_result_item[0],
                "expiration_date": "",
                "context": {'artifact_id': iris_investigate_result_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_ns_hostname", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def filter_registrant_name(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_registrant_name() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.registrant_contact.name.count", "<=", "get_data_from_custom_list:custom_function:max_registrant_contact_name_count"],
            ["iris_investigate:action_result.data.*.registrant_contact.name.count", ">", 1]
        ],
        name="filter_registrant_name:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_registrant_name(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def filter_registrant_org(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_registrant_org() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.registrant_org.count", "<=", "get_data_from_custom_list:custom_function:max_registrant_org_count"],
            ["iris_investigate:action_result.data.*.registrant_org.count", ">", 1]
        ],
        name="filter_registrant_org:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_registrant_org(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def filter_ssl_org(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_ssl_org() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.ssl_info.*.organization.count", "<=", "get_data_from_custom_list:custom_function:max_ssl_info_organization_count"],
            ["iris_investigate:action_result.data.*.ssl_info.*.organization.count", ">", 1]
        ],
        name="filter_ssl_org:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_ssl_org(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def filter_ssl_hash(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_ssl_hash() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.ssl_info.*.hash.count", "<=", "get_data_from_custom_list:custom_function:max_ssl_info_hash_count"],
            ["iris_investigate:action_result.data.*.ssl_info.*.hash.count", ">", 1]
        ],
        name="filter_ssl_hash:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_ssl_hash(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def filter_soa_email(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_soa_email() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.soa_email.*.count", "<=", "get_data_from_custom_list:custom_function:max_soa_email_count"],
            ["iris_investigate:action_result.data.*.soa_email.*.count", ">", 1]
        ],
        name="filter_soa_email:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_soa_email(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def filter_ip_address(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_ip_address() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.ip.*.address.count", "<=", "get_data_from_custom_list:custom_function:max_ip_address_count"],
            ["iris_investigate:action_result.data.*.ip.*.address.count", ">", 1]
        ],
        name="filter_ip_address:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_ip_address(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def filter_ns_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_ns_ip() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.name_server.*.ip.*.count", "<=", "get_data_from_custom_list:custom_function:max_name_server_ip_count"],
            ["iris_investigate:action_result.data.*.name_server.*.ip.*.count", ">", 1]
        ],
        name="filter_ns_ip:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_ns_ip(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def filter_mx_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_mx_ip() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        logical_operator="and",
        conditions=[
            ["iris_investigate:action_result.data.*.mx.*.ip.*.count", "<=", "get_data_from_custom_list:custom_function:max_mx_ip_count"],
            ["iris_investigate:action_result.data.*.mx.*.ip.*.count", ">", 1]
        ],
        name="filter_mx_ip:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        pivot_mx_ip(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return


@phantom.playbook_block()
def pivot_registrant_name(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_registrant_name() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_registrant_name = phantom.collect2(container=container, datapath=["filtered-data:filter_registrant_name:condition_1:iris_investigate:action_result.data.*.registrant_name.value"])

    parameters = []

    # build parameters list for 'pivot_registrant_name' call
    for filtered_result_0_item_filter_registrant_name in filtered_result_0_data_filter_registrant_name:
        if filtered_result_0_item_filter_registrant_name[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "registrant",
                "create_date": "",
                "query_value": filtered_result_0_item_filter_registrant_name[0],
                "expiration_date": "",
                "data_updated_after": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_registrant_name", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def pivot_registrant_org(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_registrant_org() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_registrant_org = phantom.collect2(container=container, datapath=["filtered-data:filter_registrant_org:condition_1:iris_investigate:action_result.data.*.registrant_org.value"])

    parameters = []

    # build parameters list for 'pivot_registrant_org' call
    for filtered_result_0_item_filter_registrant_org in filtered_result_0_data_filter_registrant_org:
        if filtered_result_0_item_filter_registrant_org[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "registrant_org",
                "create_date": "",
                "query_value": filtered_result_0_item_filter_registrant_org[0],
                "expiration_date": "",
                "data_updated_after": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_registrant_org", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def pivot_ssl_org(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_ssl_org() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_ssl_org = phantom.collect2(container=container, datapath=["filtered-data:filter_ssl_org:condition_1:iris_investigate:action_result.data.*.ssl_info.*.organization.value"])

    parameters = []

    # build parameters list for 'pivot_ssl_org' call
    for filtered_result_0_item_filter_ssl_org in filtered_result_0_data_filter_ssl_org:
        if filtered_result_0_item_filter_ssl_org[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "ssl_org",
                "query_value": filtered_result_0_item_filter_ssl_org[0],
                "expiration_date": "",
                "data_updated_after": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_ssl_org", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def pivot_ssl_hash(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_ssl_hash() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_ssl_hash = phantom.collect2(container=container, datapath=["filtered-data:filter_ssl_hash:condition_1:iris_investigate:action_result.data.*.ssl_info.*.hash.value"])

    parameters = []

    # build parameters list for 'pivot_ssl_hash' call
    for filtered_result_0_item_filter_ssl_hash in filtered_result_0_data_filter_ssl_hash:
        if filtered_result_0_item_filter_ssl_hash[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "ssl_hash",
                "query_value": filtered_result_0_item_filter_ssl_hash[0],
                "expiration_date": "",
                "data_updated_after": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_ssl_hash", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def pivot_soa_email(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_soa_email() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_soa_email = phantom.collect2(container=container, datapath=["filtered-data:filter_soa_email:condition_1:iris_investigate:action_result.data.*.soa_email.*.value"])

    parameters = []

    # build parameters list for 'pivot_soa_email' call
    for filtered_result_0_item_filter_soa_email in filtered_result_0_data_filter_soa_email:
        if filtered_result_0_item_filter_soa_email[0] is not None:
            parameters.append({
                "status": "Any",
                "pivot_type": "email",
                "create_date": "",
                "query_value": filtered_result_0_item_filter_soa_email[0],
                "expiration_date": "",
                "data_updated_after": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_soa_email", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def pivot_ip_address(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_ip_address() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_ip_address = phantom.collect2(container=container, datapath=["filtered-data:filter_ip_address:condition_1:iris_investigate:action_result.data.*.ip.*.address.value"])

    parameters = []

    # build parameters list for 'pivot_ip_address' call
    for filtered_result_0_item_filter_ip_address in filtered_result_0_data_filter_ip_address:
        if filtered_result_0_item_filter_ip_address[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "ip",
                "create_date": "",
                "query_value": filtered_result_0_item_filter_ip_address[0],
                "data_updated_after": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_ip_address", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def pivot_ns_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_ns_ip() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_ns_ip = phantom.collect2(container=container, datapath=["filtered-data:filter_ns_ip:condition_1:iris_investigate:action_result.data.*.name_server.*.ip.*.value"])

    parameters = []

    # build parameters list for 'pivot_ns_ip' call
    for filtered_result_0_item_filter_ns_ip in filtered_result_0_data_filter_ns_ip:
        if filtered_result_0_item_filter_ns_ip[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "nameserver_ip",
                "create_date": "",
                "query_value": filtered_result_0_item_filter_ns_ip[0],
                "expiration_date": "",
                "data_updated_after": "",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_ns_ip", assets=["domaintoolscreds"])

    return


@phantom.playbook_block()
def pivot_mx_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("pivot_mx_ip() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    filtered_result_0_data_filter_mx_ip = phantom.collect2(container=container, datapath=["filtered-data:filter_mx_ip:condition_1:iris_investigate:action_result.data.*.mx.*.ip.*.value"])

    parameters = []

    # build parameters list for 'pivot_mx_ip' call
    for filtered_result_0_item_filter_mx_ip in filtered_result_0_data_filter_mx_ip:
        if filtered_result_0_item_filter_mx_ip[0] is not None:
            parameters.append({
                "tld": "",
                "status": "Any",
                "pivot_type": "mailserver_ip",
                "create_date": "",
                "query_value": filtered_result_0_item_filter_mx_ip[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("pivot action", parameters=parameters, name="pivot_mx_ip", assets=["domaintoolscreds"])

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