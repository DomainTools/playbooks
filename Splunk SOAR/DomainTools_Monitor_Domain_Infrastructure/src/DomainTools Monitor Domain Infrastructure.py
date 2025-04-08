"""
This playbook retrieves the infrastructure details for a domain and stores it in a custom list. The flow will continue to monitor the domain for changes to the infrastructure based on the run schedule.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_monitored_infrastructure_list' block
    get_monitored_infrastructure_list(container=container)

    return

@phantom.playbook_block()
def get_monitored_infrastructure_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_monitored_infrastructure_list() called")

    get_monitored_infrastructure_list__monitored_domain_infra_list = None
    get_monitored_infrastructure_list__monitored_domain_infra_list_count = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here... 
    _, _, monitored_domain_infra_list = phantom.get_list(list_name='domaintools_monitored_domain_infrastructure')
    get_monitored_infrastructure_list__monitored_domain_infra_list = monitored_domain_infra_list[1:] # ignore the first row as it is the header
    get_monitored_infrastructure_list__monitored_domain_infra_list_count = len(monitored_domain_infra_list[1:])
    phantom.debug(f"dt debug - Currently monitoring {get_monitored_infrastructure_list__monitored_domain_infra_list_count} domain(s).")
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_monitored_infrastructure_list:monitored_domain_infra_list", value=json.dumps(get_monitored_infrastructure_list__monitored_domain_infra_list))
    phantom.save_run_data(key="get_monitored_infrastructure_list:monitored_domain_infra_list_count", value=json.dumps(get_monitored_infrastructure_list__monitored_domain_infra_list_count))

    iris_invesitage_or_enrich(container=container)

    return


@phantom.playbook_block()
def iris_invesitage_or_enrich(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("iris_invesitage_or_enrich() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "domain": "",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    monitored_domain_infra_list = json.loads(phantom.get_run_data(key="get_monitored_infrastructure_list:monitored_domain_infra_list"))
    parameters = [{
        "domain": ",".join([domain[0] for domain in monitored_domain_infra_list])
    }]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("enrich domain", parameters=parameters, name="iris_invesitage_or_enrich", assets=["domaintoolscreds"], callback=compare_results)

    return


@phantom.playbook_block()
def compare_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("compare_results() called")

    get_monitored_infrastructure_list__monitored_domain_infra_list = json.loads(_ if (_ := phantom.get_run_data(key="get_monitored_infrastructure_list:monitored_domain_infra_list")) != "" else "null")  # pylint: disable=used-before-assignment

    compare_results__has_infra_changes = None
    compare_results__has_infra_changes_count = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    iris_results = phantom.collect2(
        container=container, 
        datapath=["iris_invesitage_or_enrich:action_result.data"], 
        action_results=results
    )
    
    # will unpack the list as the result from collect2 is a list[list[list[dict[any,any]]]]
    # e.g. from this [[[{"sample": "structure"}]]] to [{}]
    results = list(*iris_results[0])
    current_domain_infra = {}
    for result in results:
        domain = result.get("domain")
        registrant_org = result.get("registrant_org")
        ns = result.get("name_server")
        mx = result.get("mx")
        asn = [ip.get("asn", [{}])[0].get("value") for ip in result.get("ip")]
        ssl_info = result.get("ssl_info")
        
        # this will make sure unique domains is only added 
        # just in case there will be 2 same domains in the params
        if domain not in current_domain_infra:
            current_domain_infra[domain] = {
                "registrant_org": registrant_org,
                "name_server": ns,
                "mx": mx,
                "asn": asn,
                "ssl_info": ssl_info
            }
    
    # arrange new rows the table/custom list with the updated values
    from datetime import datetime
    
    has_infra_changes = []
    updated_list = []
    for row in get_monitored_infrastructure_list__monitored_domain_infra_list:
        domain, prev, current, last_updated = row
        prev = json.loads(prev or "{}") 
        current = json.loads(current or "{}")
        new_row = [domain, prev, current]
        phantom.debug(f"dt debug - updating {domain}")
        
        if latest_domain_infra := current_domain_infra.get(domain):     
            # convert to json string
            latest_domain_infra_str = json.dumps(latest_domain_infra)
            current_str = json.dumps(current)
            
            new_row = [domain, current_str, latest_domain_infra_str, last_updated]
            
            # detect changes should fall if prev has value.
            if latest_domain_infra != current and prev:
                phantom.debug(f"dt debug - detected changes in {domain}")
                new_row[3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                has_infra_changes.append(new_row)
            
            # update the current and previous infra if prev infra is None
            # assuming it's the playbook first run
            if not prev:
                new_row[1] = latest_domain_infra
                
        updated_list.append(new_row)

    # update the table/custom list
    headers = ["domain_name", "prev_infrastructure", "current_infrastructure", "last_updated"]
    updated_list.insert(0, headers)
    
    success, _ = phantom.set_list(list_name="domaintools_monitored_domain_infrastructure", values=updated_list)
    phantom.debug(f"dt debug - phantom.set_list results: success: {success}")
    
    compare_results__has_infra_changes = has_infra_changes
    compare_results__has_infra_changes_count = len(has_infra_changes)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="compare_results:has_infra_changes", value=json.dumps(compare_results__has_infra_changes))
    phantom.save_run_data(key="compare_results:has_infra_changes_count", value=json.dumps(compare_results__has_infra_changes_count))

    decision_1(container=container)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["compare_results:custom_function:has_infra_changes_count", ">", 0]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        check_for_changed_domains(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def check_for_changed_domains(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("check_for_changed_domains() called")

    compare_results__has_infra_changes = json.loads(_ if (_ := phantom.get_run_data(key="compare_results:has_infra_changes")) != "" else "null")  # pylint: disable=used-before-assignment

    check_for_changed_domains__merge_results = None
    check_for_changed_domains__event_name = None
    check_for_changed_domains__file_name = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    alerts = []
    for results in compare_results__has_infra_changes or []:
        domain, _, _, _ = results
        alerts.append(domain)
    check_for_changed_domains__merge_results = ", ".join(alerts)
    check_for_changed_domains__event_name = container.get("name")
    
    # save filename as data to use by the nxt actions
    from datetime import datetime
    check_for_changed_domains__file_name = f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="check_for_changed_domains:merge_results", value=json.dumps(check_for_changed_domains__merge_results))
    phantom.save_run_data(key="check_for_changed_domains:event_name", value=json.dumps(check_for_changed_domains__event_name))
    phantom.save_run_data(key="check_for_changed_domains:file_name", value=json.dumps(check_for_changed_domains__file_name))

    monitored_domains_infrastructure_change_prompt(container=container)
    merge_results(container=container)

    return


@phantom.playbook_block()
def monitored_domains_infrastructure_change_prompt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("monitored_domains_infrastructure_change_prompt() called")

    # set user and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """Changes are detected in this domains:\n{0}\n\nFor more details go to Event: {1} > \"Files\" tab > Download '{2}'."""

    # parameter list for template variable replacement
    parameters = [
        "check_for_changed_domains:custom_function:merge_results",
        "check_for_changed_domains:custom_function:event_name",
        "check_for_changed_domains:custom_function:file_name"
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=50, name="monitored_domains_infrastructure_change_prompt", parameters=parameters)

    return


@phantom.playbook_block()
def merge_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("merge_results() called")

    compare_results__has_infra_changes = json.loads(_ if (_ := phantom.get_run_data(key="compare_results:has_infra_changes")) != "" else "null")  # pylint: disable=used-before-assignment

    merge_results__context_data = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    data = []
    for result in compare_results__has_infra_changes:
        domain, prev, current, last_updated = result
        current = json.loads(current or {})
        prev = json.loads(prev or {})
        data.append(
            {
                "domain": domain,
                "prev": prev,
                "current": current,
                "list_keys": [k for k, v in current.items() if isinstance(v, list)]
            }
        )
        
    merge_results__context_data = data
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="merge_results:context_data", value=json.dumps(merge_results__context_data))

    output_to_html(container=container)

    return


@phantom.playbook_block()
def output_to_html(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("output_to_html() called")

    merge_results__context_data = json.loads(_ if (_ := phantom.get_run_data(key="merge_results:context_data")) != "" else "null")  # pylint: disable=used-before-assignment
    check_for_changed_domains__file_name = json.loads(_ if (_ := phantom.get_run_data(key="check_for_changed_domains:file_name")) != "" else "null")  # pylint: disable=used-before-assignment

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    # Write your custom code here...
    phantom.debug("rendering template")
    html_body = phantom.render_template(
        """
<html>
<head>
  <meta http-equiv='X-UA-Compatible' content='IE=edge'>
  <title>Summary Report</title>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      font-family: "Lucida Console", Courier, monospace;
      font-size: 14px;
    }

    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
    }

    .wrapper {
      width: 60%;
      
      padding: 10px;
    }
    p {
      margin: 7px 0 0 2px;
    }
    .content {
      display: flex;
      justify-content: space-between;
      margin: 10px 5px 5px 2px;
    }
    .left {
      width: 40%;
    }
    .right {
      width: 60%;
    }
    
  </style>
</head>
<body>
  <div class="wrapper">
    <table style="width: 100%;">
      <tr style = "background-color: #007abd;color:white;">
        <th style="width:20%;color:white;">Domain</th>
        <th colspan="2" style="width:40%;color:white;">Previous Value</th>
        <th colspan="2" style="width:40%;color:white;">Current Value</th>
      </tr>
      {% for result in results%}
        <tr>
          <td><p style="text-align:center; margin:0;">{{ result.domain }}</p></td>
          <!-- Previous Value Column -->
          <td colspan="2">
            {% for key, val in result.prev.items %}
              {% if key in result.list_keys%}
                {% if key == "asn" %}
                  <div class="content">
                    <div class="left">
                      ASN:
                    </div>
                    <div class="right">
                      <span style="display: inline-block;"> {{ val }} </span>
                    </div>
                  </div>
                {% else %}
                  <div class="content">
                    <div class="left">
                      {{ key | title }}:
                    </div>
                    <div class="right">
                      {% if val %}
                        {% for item in val %}
                          {% for k,v in item.items %}
                            {% if 'value' in v %}
                                <span style="display: inline-block;">{{ k | title }}: {{ v.value }} </span>
                            {% else %}
                                {% if v.0.value %}
                                  <span style="display: inline-block;">{{ k | upper }}: {{ v.0.value }}</span>
                                {% else %}
                                  <br><span style="display: inline-block;">{{ k | title }}: {{ v }}</span>
                                {% endif %}
                            {% endif %}
                          {% endfor %}
                        {% endfor %}
                      {% else %}
                        <span style="display: inline-block;">No Data Found.</span>
                      {% endif %}
                    </div>
                  </div>
                {% endif %}
              {% else %}
                 <div class="content">
                    <div class="left">
                      {{ key | title }}:
                    </div>
                    <div class="right">
                      {% if val %}
                        <span style="display: inline-block;"> {{ val.value }} </span>
                      {% else %}
                        <span style="display: inline-block;"> No Data Found. </span>
                      {% endif %}
                    </div>
                  </div>
              {% endif %}
            {% endfor %}
          </td>
          <!-- Current Value Column -->
          <td colspan="2">
            {% for key, val in result.current.items %}
              {% if key in result.list_keys%}
                {% if key == "asn" %}
                  <div class="content">
                    <div class="left">
                      ASN:
                    </div>
                    <div class="right">
                      <span style="display: inline-block;"> {{ val }} </span>
                    </div>
                  </div>
                {% else %}
                  <div class="content">
                    <div class="left">
                      {{ key | title }}:
                    </div>
                    <div class="right">
                      {% if val %}
                        {% for item in val %}
                          {% for k,v in item.items %}
                            {% if 'value' in v %}
                                <span style="display: inline-block;">{{ k | title }}: {{ v.value }} </span>
                            {% else %}
                                {% if v.0.value %}
                                  <span style="display: inline-block;">{{ k | upper }}: {{ v.0.value }}</span>
                                {% else %}
                                  <br><span style="display: inline-block;">{{ k | title }}: {{ v }}</span>
                                {% endif %}
                            {% endif %}
                          {% endfor %}
                        {% endfor %}
                      {% else %}
                        <span style="display: inline-block;">No Data Found.</span>
                      {% endif %}
                    </div>
                  </div>
                {% endif %}
              {% else %}
                 <div class="content">
                    <div class="left">
                      {{ key | title }}:
                    </div>
                    <div class="right">
                      {% if val %}
                        <span style="display: inline-block;"> {{ val.value }} </span>
                      {% else %}
                        <span style="display: inline-block;"> No Data Found. </span>
                      {% endif %}
                    </div>
                  </div>
              {% endif %}
            {% endfor %}
          </td>
        </tr>
      {% endfor %}
    </table>
  </div>
</body>
</html>

        """,
        {
            'results': merge_results__context_data,
        }
    )
    code_1__html_template = html_body
    html_to_string = "".join([html_body])
    #phantom.debug(html_to_string)
    
    phantom.debug("dt debug - done rendering template")
    ### write to the vault
    # create a file name
    from datetime import datetime
    file_name = check_for_changed_domains__file_name
    # create a tmp file
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w") as report_file:
        report_file.write(html_to_string)
    # write the html to a pdf at the tempfile location
    #if phantom.html_string_to_pdf(html_body, tf.name):
    phantom.vault_add(container=container, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)

    ################################################################################
    ## Custom Code End
    ################################################################################

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    output = {
        "summary_report_datetime": [],
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_playbook_output_data(output=output)

    return