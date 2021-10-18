## DomainTools Domain Risk Score Playbook
Retrieve the Domain Risk Score and throw an Alert for the Analyst to manually review the domain artifact. Users can block the domain.

#### DomainTools API Asset
**The DomainTools playbooks in this repo will require an asset called `domaintoolsiriscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution.
<br>

#### Before Installing
In this directory there is a csv called `domaintools_domain_risk.csv` that can be downloaded and used to import into the app under the "Custom Lists" tab on the "Playbooks" feature. With the  `domaintoolsiriscreds` asset loaded in, import the csv or create a custom list named `domaintools_domain_risk` and copy the contents of the csv into the custom list.
**The value in the list is the mininmum risk score to alert on, the number can be changed by the analyst, but the first column should not be changed, otherwise the playbook will break.**

#### Installation
Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolsiriscreds` asset, save the playbook, make sure it's active, and give it a shot.
