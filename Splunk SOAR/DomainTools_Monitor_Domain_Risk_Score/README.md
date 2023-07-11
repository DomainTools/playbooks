## DomainTools Monitor Domain Risk Score Playbook

Retrieves the risk score for a domain and stores it in configurable custom list. The flow will continue to monitor the domain for changes to the risk score based on the run schedule.

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution. 
<br>

#### Before Installing

In this directory there is a csv called `domaintools_monitored_domains.csv` and `domaintools_riskscore_threshold.csv` that can be downloaded and used to import into the app under the "Custom Lists" tab on the "Playbooks" feature. With the `domaintoolscreds` asset loaded in, import the csv or create a custom list named `domaintools_monitored_domains` and `domaintools_riskscore_threshold` and copy the contents of the csv into the custom list.

**The values in `domaintools_monitored_domains` list contains the domains to be monitored and it's previous and current risk score. The domains can be changed, but the first & second column should have the default value of "None", or the playbook will break.**

**The values in `domaintools_riskscore_threshold` list controls the risk score threshold value. The number can be changed, but the first column should remain unchanged, or the playbook will break.**

#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.


#### Scheduling
Go into Administration > Event Settings > Label Settings then add new label with a meaningful name like "run_every_30mins". Go to Apps > search for the splunk Timer app > configure new asset > Ingest Settings > Set it to run on the appropriate schedule(in this case, 30minutes) > Set the 'Label to Apply' to be the label added above in Administration. In your playbook settings, set the "Operatos On" value to also be "run_every_30mins". 
The playbook will now run every time the Timer app creates on of these events, and will execute according to your schedule. 

Reference: _https://community.splunk.com/t5/Splunk-SOAR-f-k-a-Phantom/How-to-schedule-a-Phantom-playbook-to-run-at-specific-intervals/m-p/500565_

### How-to Videos
How to setup/use the playbook: https://www.loom.com/share/c1694449a1e340b2b1df4aaba1ee214b?sid=aa74e89d-2bc1-4076-8472-37cc6bd960f0

How to run the playbook base on a schedule/interval: https://www.loom.com/share/888c088c31594732a5d3cff54f10243a?sid=c9a42e35-9e71-40f4-adc8-0a8c878c1922
