"""
This playbook servers as a function that can be use by another playbook. It works by taking a domain input then checking DNSDB Farsight for all Subdomains and Resource Records associated with the domain. This playbook accepts 5 parameters.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_input_parameters' block
    get_input_parameters(container=container)

    return

@phantom.playbook_block()
def get_input_parameters(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_input_parameters() called")

    playbook_input_dt_domain = phantom.collect2(container=container, datapath=["playbook_input:dt_domain"])
    playbook_input_subdomain_only = phantom.collect2(container=container, datapath=["playbook_input:subdomain_only"])
    playbook_input_time_first_after = phantom.collect2(container=container, datapath=["playbook_input:time_first_after"])
    playbook_input_limit = phantom.collect2(container=container, datapath=["playbook_input:limit"])
    playbook_input_output_result_to_html = phantom.collect2(container=container, datapath=["playbook_input:output_result_to_html"])

    playbook_input_dt_domain_values = [item[0] for item in playbook_input_dt_domain]
    playbook_input_subdomain_only_values = [item[0] for item in playbook_input_subdomain_only]
    playbook_input_time_first_after_values = [item[0] for item in playbook_input_time_first_after]
    playbook_input_limit_values = [item[0] for item in playbook_input_limit]
    playbook_input_output_result_to_html_values = [item[0] for item in playbook_input_output_result_to_html]

    get_input_parameters__dt_playbook_params = None
    get_input_parameters__output_result_to_html = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    six_hours_ago = "-21600"
    
    DEFAULT_TIME_FIRST_AFTER = six_hours_ago
    DEFAULT_REQUEST_LIMIT = 500
    
    phantom.debug(f"dt debug - Retrieving data for this domains: {playbook_input_dt_domain_values}")
    
    def _is_validate_true_false(value):
        try:
            return (
                value in (None, "") or str(value).lower() == "true" or str(value).lower() == "false"
            )
        except (AttributeError, ValueError) as e:
            return False
    
    def _is_positive_number(value):
        try:
            return int(value) >= 0
        except (AttributeError, ValueError) as e:
            return False
        
    # 'subdomain_only' -> defaults to False 
    phantom.debug(f"dt debug - Validating playbook inputs.")
    subdomain_only = False
    if playbook_input_subdomain_only_values:
        if not _is_validate_true_false(playbook_input_subdomain_only_values[0]):
            phantom.error("dt error - Invalid Value for 'subdomain'. Must be (True/False). Leave it blank for default value of False")
            return
        subdomain_only = bool(playbook_input_subdomain_only_values[0])

    time_first = DEFAULT_TIME_FIRST_AFTER 
    if playbook_input_time_first_after_values and playbook_input_time_first_after_values[0]:
        time_first = playbook_input_time_first_after_values[0]
        
    limit = DEFAULT_REQUEST_LIMIT
    if playbook_input_limit_values[0]:
        if not _is_positive_number(playbook_input_limit_values[0]):
            phantom.error("dt error - Invalid Value for 'limit'. Must be a positive number. Leave it blank for default value of 500.")
            return
        limit = playbook_input_limit_values[0]
    
    # 'output_result_to_html' -> defaults to True
    output_result_to_html = True 
    if playbook_input_output_result_to_html_values:
        if not _is_validate_true_false(playbook_input_subdomain_only_values[0]):
            phantom.error("dt error - Invalid Value for 'output_result_to_html'. Must be (True/False). Leave it blank for default value of False")
            return
        output_result_to_html = bool(playbook_input_output_result_to_html_values[0])
    
    parameters = {
        "dt_domains": playbook_input_dt_domain_values,
        "subdomain_only": subdomain_only,
        "time_first": time_first,
        "limit": limit
    }
    
    phantom.debug(f"dt debug - Playbook current parameters: {parameters}")
    get_input_parameters__dt_playbook_params = parameters
    phantom.debug(f"dt debug - Outputting results to html: {output_result_to_html}")
    get_input_parameters__output_result_to_html = output_result_to_html
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="get_input_parameters:dt_playbook_params", value=json.dumps(get_input_parameters__dt_playbook_params))
    phantom.save_run_data(key="get_input_parameters:output_result_to_html", value=json.dumps(get_input_parameters__output_result_to_html))

    rrset_lookup_1(container=container)

    return


@phantom.playbook_block()
def rrset_lookup_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("rrset_lookup_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "limit": 200,
        "owner_name": "",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    parameters = []
    dt_playbook_params = json.loads(_ if (_ := phantom.get_run_data(key="get_input_parameters:dt_playbook_params")) != "" else "{}")  # pylint: disable=used-before-assignment
    subdomain_only = dt_playbook_params.get("subdomain_only")
    
    for domain in dt_playbook_params.get("dt_domains") or []:
        owner_name = f"*.{domain}" if subdomain_only else domain
        param_data = {
            "owner_name": owner_name,
            "limit": dt_playbook_params.get("limit"),
            "type": "A",
            "time_first_after": dt_playbook_params.get("time_first")
        }
        parameters.append(param_data)
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("rrset lookup", parameters=parameters, name="rrset_lookup_1", assets=["dan dnsdb key"], callback=parse_results)

    return


@phantom.playbook_block()
def parse_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("parse_results() called")

    parse_results__parsed_dnsdb_result = None
    parse_results__result_count = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    results = []
    summary = phantom.get_summary()
    if result := summary.get("result"):
        for action_result in result:
            if action_run_id := action_result.get("action_run_id"):
                action_results = phantom.get_action_results(action_run_id=action_run_id, flatten=False)
                for ar in action_results.pop().get("action_results") or []:
                    data = {
                       "dt_domain": ar.get("parameter", {}).get("owner_name", "").replace("*.", ""),
                       "data": ar.get("data") or [],
                       "count": ar.get("summary", {}).get("total_items") or 0
                    }
                    results.append(data)
    
    if not results:
        parse_results__result_count = 0
        return
    
    dt_playbook_params = json.loads(_ if (_ := phantom.get_run_data(key="get_input_parameters:dt_playbook_params")) != "" else "{}")  # pylint: disable=used-before-assignment
    if dt_playbook_params.get("subdomain_only"):
        for result in results:
            dnsdb_rrname = set(data.get("rrname") for data in result["data"])
            # override key "data" and "count" as we only getting unique values
            result["data"] = [{"rrname": rrname} for rrname in dnsdb_rrname]
            result["count"] = len(dnsdb_rrname)
    else: # format epoch seconds 
        from datetime import datetime
        _epoch_converter = lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')
        for result in results:
            result["data"] = [{**result, "time_first": _epoch_converter(result["time_first"])} for result in result["data"]]
    
    parse_results__parsed_dnsdb_result = results
    parse_results__result_count = len(results)
    phantom.debug(f"dt debug - discovered {parse_results__result_count} dnsdb domain records.")
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="parse_results:parsed_dnsdb_result", value=json.dumps(parse_results__parsed_dnsdb_result))
    phantom.save_run_data(key="parse_results:result_count", value=json.dumps(parse_results__result_count))

    decision_2(container=container)

    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_2() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["get_input_parameters:custom_function:output_result_to_html", "==", True]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        output_result_to_html(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def output_result_to_html(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("output_result_to_html() called")

    parse_results__parsed_dnsdb_result = json.loads(_ if (_ := phantom.get_run_data(key="parse_results:parsed_dnsdb_result")) != "" else "null")  # pylint: disable=used-before-assignment

    output_result_to_html__output_file_name = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    dt_playbook_params = json.loads(_ if (_ := phantom.get_run_data(key="get_input_parameters:dt_playbook_params")) != "" else "{}")  # pylint: disable=used-before-assignment
    phantom.debug(f"dt debug - Saving results to a html file...")
    html_body = phantom.render_template(
        """
        <!DOCTYPE html>
<html>
<head>
  <meta http-equiv='X-UA-Compatible' content='IE=edge'>
  <title>DT DNSDB Retrieve Domain Records</title>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      font-family: sans-serif;
      font-size: 14px;
    }

    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
      padding: 5px;
    }

    .wrapper {
      width: 60%;  
      padding: 10px;
    }

    p {
      margin: 7px 0 0 2px;
    }

    .header {
      background-color: #007abd;
      color:white;
    }
    
  </style>
</head>
<body>
  <div class="wrapper">
    <table style="width: 100%;">
      <tr class="header">
        <th>dt_domain</th>
        <th>dnsdb_rrname</th>
        {% if not subdomain_only %}
          <th>dnsdb_rrtype</th>
          <th>dnsdb_rrdata</th>
          <th>dnsdb_time_last_formatted</th>
        {% endif %}
        <th>dnsdb_count</th>
      </tr>
      {% for result in results %}
        <tr>
          <!-- dt_domain column -->
          <td><p style="text-align:center; margin:0;">{{ result.dt_domain }}</p></td>
          <!-- end of dt_domain column -->
          <!-- dnsdb_rrname column -->
          <td>
            {% for dnsdb_data in result.data %}
              <p style="text-align:center; margin:0;">{{ dnsdb_data.rrname }}</p>
            {% endfor %}
          </td>
            <!-- end of dnsdb_rrtype column -->
          {% if not subdomain_only %}
            <!-- dnsdb_rrtype column -->
            <td><p style="text-align:center; margin:0;">A</p></td>
            <!-- end of dnsdb_rrtype column -->
            
            <!-- dnsdb_rrdata column -->
            <td>
              {% for dnsdb_data in result.data %}
                {% for rdata in dnsdb_data.rdata %}
                  <p style="text-align:center; margin:1px;">{{ rdata }}</p>
                {% endfor %}
              {% endfor %}
            </td>
            <!-- end of dnsdb_rrdata column -->
            
            <!-- dnsdb_time_last_formatted column -->
            <td>
              {% for dnsdb_data in result.data %}
                <p style="text-align:center; margin:1px;">{{ dnsdb_data.time_first }}</p>
              {% endfor %}
            </td>
            <!-- end of dnsdb_time_last_formatted column -->
          {% endif %}
          <!-- dnsdb_count column -->
          <td><p style="text-align:center; margin:1px;">{{ result.count }}</p></td>
          <!-- end of dnsdb_count column -->
        </tr>
      {% endfor %}
    </table>
  </div>
</body>
</html>

        """,
        {
            "results": parse_results__parsed_dnsdb_result,
            "subdomain_only": dt_playbook_params.get("subdomain_only") or False
        }
    )
    html_to_string = "".join([html_body])
    
    phantom.debug(f"dt debug - Outputing results...")
    ### write to the vault
    # create a file name
    from datetime import datetime
    file_name = f"dt_dnsdb_domain_records_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    # create a tmp file
    with open(f"/opt/phantom/vault/tmp/{file_name}", "w") as report_file:
        report_file.write(html_to_string)
    # write the html to a pdf at the tempfile location
    #if phantom.html_string_to_pdf(html_body, tf.name):
    phantom.vault_add(container=container, file_location=f"/opt/phantom/vault/tmp/{file_name}", file_name=file_name)
    output_result_to_html__output_file_name = file_name
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="output_result_to_html:output_file_name", value=json.dumps(output_result_to_html__output_file_name))

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    parse_results__parsed_dnsdb_result = json.loads(_ if (_ := phantom.get_run_data(key="parse_results:parsed_dnsdb_result")) != "" else "null")  # pylint: disable=used-before-assignment
    output_result_to_html__output_file_name = json.loads(_ if (_ := phantom.get_run_data(key="output_result_to_html:output_file_name")) != "" else "null")  # pylint: disable=used-before-assignment

    output = {
        "parsed_dnsdb_rrset_lookup_result": parse_results__parsed_dnsdb_result,
        "output_file_name": output_result_to_html__output_file_name,
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