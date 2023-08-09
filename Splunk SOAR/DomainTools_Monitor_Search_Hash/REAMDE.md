## DomainTools Monitor Search Hash

This playbook retrieves domains from a given hash and imports it to an artifact. The flow will continue to monitor the domain for changes to the risk score based on the run schedule.

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution. Current action selected is `load_hash` and it requires `search_hash` input parameter.
<br>

#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.
