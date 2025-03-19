## DomainTools Feeds NOD Plabook

This playbook retrieves newly observed domains from DomainTools Real Time Unified Feeds from a given `sessionID`, `before`, and/or `after` params. It will save the NOD list in a csv file with naming convention - `domaintools_feed_nod_<YYYYMMDD>_<hhmmss>.csv`. The flow will continue to retrieve NOD feeds based on the scheduled run

#### DomainTools API Asset

**The DomainTools playbooks in this repo will require an asset called `domaintoolscreds`** for a DomainTools API username and key. This asset is used to retrieve NOD feeds data via the DomainTools API during playbook execution. Current action selected is `nod_feed` and it requires `sessionID`, `before`, and/or `after` input parameters. Optional input parameters are `domain` and `top`.
<br>

#### Installation

Download the tar file in this directory and import the playbook using that file. The asset accessed in the playbook is for DomainTools API credentials. Point the playbook to the `domaintoolscreds` asset, save the playbook, make sure it's active, and give it a shot.
