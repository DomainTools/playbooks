## DomainTools Alerting Playbook - New Domains

This playbook retrieves domain in Iris Investigate from a given search hash with built-in `first_seen` param. The flow will continue to retrieve new domains based on the scheduled run

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution. Current action selected is `load_hash` and it requires `search_hash` input parameter.
<br>

#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.
