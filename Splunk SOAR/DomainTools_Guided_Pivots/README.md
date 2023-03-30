## DomainTools Guided Pivots Playbook

Retrieve the Iris Investigate profile of a domain and automatically identify potential connected infrastructure related to artifacts based on DomainTools Guided Pivot value. The pivot value is set based off of a configurable custom list.

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution. It supports `destinationDnsDomain` and `domain` input parameters.
<br>

#### Before Installing

In this directory there is a csv called `domaintools_guided_pivot.csv` that can be downloaded and used to import into the app under the "Custom Lists" tab on the "Playbooks" feature. With the `domaintoolscreds` asset loaded in, import the csv or create a custom list named `domaintools_guided_pivot` and copy the contents of the csv into the custom list.
**The values in this list control the max value retrieved from each pivot. The numbers can be changed, but the first column should remain unchanged, or the playbook will break.**

#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.
