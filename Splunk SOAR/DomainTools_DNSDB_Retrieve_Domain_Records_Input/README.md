## DomainTools DNSDB Retrieve DomainRecords Input Playbook

This playbook servers as a function that can be use by another playbook. It works by taking a domain input then checking DNSDB Farsight for all Subdomains and Resource Records associated with the domain. 
This playbook accepts 5 parameters.


#### DNSDB API Asset

**The DomainTools playbooks in this repo will require an asset of `dnsdb`** for a DNSDB API key. This asset is used to retrieve DNSDB data via the DNSDB Farsight API during playbook execution. 
<br>

#### Playbook Input Parameters

| Name                  | Data Type | Description                                                      |
|-----------------------|-----------|------------------------------------------------------------------|
| dt_domain             | `domain`  | The domain to lookup.                                            |
| subdomain_only        |           | Flag results for subdomain only. Use True or False as value.     |
| time_first_after      |           | Record first seen after (in epoch sec). Default is 10 days ago.  |
| limit                 |           | The query limit. Default is 500                                  |
| output_result_to_html |           | Creates a HTML result in the current container. Default is True. |

#### Playbook Output

| Name                             | Data Type   | Description                                |
|----------------------------------|-------------|--------------------------------------------|
| parsed_dnsdb_rrset_lookup_result |             | The parsed result from dnsdb rrset lookup. |
| output_file_name                 | `file name` | The filename of the html output            |

#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DNSDB Farsight API credentials. Call the playbook to your main playbook, make sure it's active, and give it a shot.
