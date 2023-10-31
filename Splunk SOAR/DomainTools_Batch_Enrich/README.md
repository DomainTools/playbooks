## DomainTools Batch Enrich Playbooks

Batch enrich a queue of domains using Iris Enrich.

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve DomainTools data via the DomainTools API during playbook execution. It supports `destinationDnsDomain` and `domain` input parameters.
<br>

#### Before Installing

In this directory there are two csv files called `domaintools_domain_risk.csv` and `iris_enrich_batch_queue` that can be downloaded and used to import into the app under the "Custom Lists" tab on the "Playbooks" feature. With the `domaintoolscreds` asset loaded in, import the csv files as custom lists.
* `iris_enrich_batch_queue` - An empty list used as the location to store artifacts to be batch enriched. 
* `domaintools_domain_risk.csv` - The value in the list is the minimum risk score to alert on, used in the `Iris Enrich Batch Example` playbook. The number can be changed by the analyst, but the first column should not be changed, otherwise the playbook will break.**

#### Installation

Download each of the tar files in this directory and import the playbooks using those files. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.

#### Getting Started

* Iris Enrich Batch Add Domains - Run this playbook on an event to add it's artifacts to the `Iris Enrich Batch Queue` custom list.
* Iris Enrich Batch Process Domains - Run this playbook to enrich all artifacts in the `Iris Enrich Batch Queue` custom list in one batch.
* Iris Enrich Clear Queue - Run this playbook to clear the `Iris Enrich Batch Queue` custom list when Iris Enrich is completed.
* Iris Enrich Batch Example - This example shows how to combine the `Iris Enrich Batch Process` and `Iris Enrich Clear Queue` playbooks after using the Iris Enrich batch results to alert any high risk domains.  
