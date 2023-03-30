## DomainTools Iris Malicious Tags Playbook

Retrieve the Iris Investigate profile of a domain and automatically flag domains that have been tagged as malicious in DomainTools Iris. The list of malicious tags are configurable by the analyst and can be kept up to date for automation.

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution. It supports `destinationDnsDomain` and `domain` input parameters.
<br>

#### Before Installing

In this directory there is a csv called `iris_malicious_tags.csv` that can be downloaded and used to import into the app under the "Custom Lists" tab on the "Playbooks" feature. With the `domaintoolscreds` asset loaded in, import the csv or create a custom list named `iris_malicious_tags` and copy the contents of the csv into the custom list.
**This list needs to be filled out/edited with tags that need to be flagged.**

#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.
