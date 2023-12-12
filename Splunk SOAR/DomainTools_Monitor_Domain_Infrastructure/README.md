## DomainTools Monitor Domain Infrastructure Playbook

Retrieves the infrastructure details for a domain and stores it in a custom list. The flow will continue to monitor the domain for changes to the risk score based on the run schedule.

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution.
<br>

#### Before Installing
In this directory there is a csv called `domaintools_monitored_domain_infrastructure.csv` that can be downloaded and used to import into the app under the "Custom Lists" tab on the "Playbooks" feature. With the `domaintoolscreds` asset loaded in, import the csv or create a custom list named `domaintools_monitored_domain_infrastructure` and copy the contents of the csv into the custom list.

**The values in `domaintools_monitored_domain_infrastructure` list contains the domains to be monitored and it's previous and current value. The domains can be changed, but the first & second column should have a default value of "" or should be empty, or the playbook will break.**


#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.