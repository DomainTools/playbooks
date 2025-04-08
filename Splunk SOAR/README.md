# DomainTools Splunk SOAR Playbooks

Working playbooks for Splunk SOAR.

## How to Contribute

1. Export the DomainTools Splunk SOAR playbook of your choice in the Splunk SOAR UI.
2. Create a new folder (if new playbook) with the same name of the compressed file version of the playbook.

    `e.g. DomainTools_Domain_Risk_Score.tgz > Splunk SOAR/DomainTools_Domain_Risk_Score/`

3. Unzipped the compressed version (make sure you have the original copy of .tgz file after unzipping it.)
4. Copy all the source code to the src/ directory for diff purposes.

    `e.g. DomainTools_Domain_Risk_Score.tgz > Splunk SOAR/DomainTools_Domain_Risk_Score/src/`

5. The exported compressed version of the playbook should be placed in `Splunk SOAR/<your_playbook_name>/<exported_compressed_version_of_the_playbook>.tgz` directory.

    `e.g. Splunk SOAR/DomainTools_Domain_Risk_Score/DomainTools_Domain_Risk_Score.tgz`

6. The playbook directory structure should be:

    ```bash
        ├── Splunk SOAR
        │   ├── DomainTools_Domain_Risk_Score
        │   │   ├── DomainTools_Domain_Risk_Score.tgz
        │   │   ├── src/
        │   │   │   ├──  DomainTools_Domain_Risk_Score.py
        │   │   │   ├──  DomainTools_Domain_Risk_Score.json
        │   │   ├── README.md
    ```

7. After finalizing the changes, commit & push the changes.

## Installation

For the DomainTools playbooks in this repo, an asset called `domaintoolscreds` is needed with
DomainTools API username and key. The playbooks expect this asset to exist to make the API calls needed for the playbook data upon execution. Installation instructions for each playbook is in the README at the root of the playbook’s directory.

### Current Playbooks In This Repo

#### DomainTools Domain Risk Score

Get the Domain Risk Score and throw an Alert for the Analyst to manually review the domain artifact. Users can block the domain. It supports `destinationDnsDomain` and `domain` input parameters.

#### DomainTools Guided Pivots

Retrieve the Iris Investigate profile of the domain and automatically identify potential connected infrastructure related to artifacts based on DomainTools Guided Pivot value. The pivot value is set to 200 and can be tailored per investigation objectives. It supports `destinationDnsDomain` and `domain` input parameters.

#### DomainTools Iris Malicious Tags

Retrieve the Iris Investigate profile of a domain and automatically flag domains that have been tagged as malicious in DomainTools Iris. The list of malicious tags are configurable by the analyst and can be kept up to date for automation. It supports `destinationDnsDomain` and `domain` input parameters.

#### DomainTools Alerting Playbook - Check Domain Risk Score

This playbook call iris ivestigate api with a given `tag`. Check active domains with high risk score then alerts user and outputs all high risk domains in a csv file.

#### DomainTools Alerting Playbook - New Domains

This playbook retrieves domain in Iris Investigate from a given search hash with built-in `first_seen` param. The flow will continue to retrieve new domains based on the scheduled run.

#### DomainTools Monitor Domain Infrastructure

Retrieves the infrastructure details for a domain and stores it in a custom list. The flow will continue to monitor the domain for changes to the risk score based on the run schedule.

#### DomainTools Monitor Domain Risk Score

Retrieves the risk score for a domain and stores it in configurable custom list. The flow will continue to monitor the domain for changes to the risk score based on the run schedule.

#### DomainTools Monitor Domain Search Hash

This playbook retrieves domains from a given hash and imports it to an artifact. The flow will continue to monitor the domain for changes to the risk score based on the run schedule.

#### DomainTools Feeds Domain Discovery

This playbook retrieves newly observed domains from DomainTools Real Time Unified Feeds from a given `sessionID`, `before`, and/or `after` params. It will save the Domain Discovery list in a csv file with naming convention - `domaintools_feed_domain_discovery_<YYYYMMDD>_<hhmmss>.csv`. The flow will continue to retrieve NOD feeds based on the scheduled run.

#### DomainTools Feeds Newly Active Domains (NAD)

This playbook retrieves newly active domains from DomainTools Real Time Unified Feeds from a given `sessionID`, `before`, and/or `after` params. It will save the NAD list in a csv file with naming convention - `domaintools_feed_nad_<YYYYMMDD>_<hhmmss>.csv`. The flow will continue to retrieve NAD feeds based on the scheduled run.

#### DomainTools Feeds Newly Observe Domains (NOD)

This playbook retrieves newly observed domains from DomainTools Real Time Unified Feeds from a given `sessionID`, `before`, and/or `after` params. It will save the NOD list in a csv file with naming convention - `domaintools_feed_nod_<YYYYMMDD>_<hhmmss>.csv`. The flow will continue to retrieve NOD feeds based on the scheduled run.

#### DomainTools Feeds Parsed Domain RDAP

This playbook retrieves newly observed domains from DomainTools Real Time Unified Feeds from a given `sessionID`, `before`, and/or `after` params. It will save the Parsed Domain RDAP list in a csv file with naming convention - `domaintools_feed_parsed_domain_rdap_<YYYYMMDD>_<hhmmss>.csv`. The flow will continue to retrieve NOD feeds based on the scheduled run.

#### Third party made playbooks, that work with DomainTools data

[Investigate](https://github.com/phantomcyber/playbooks/blob/4.2/investigate.py)

Use varied services to execute a wide range of investigative queries across all available assets.

[User Prompt and Block Domains](https://github.com/phantomcyber/playbooks/blob/4.2/user_prompt_and_block_domain.py)

Utilize DomainTools to generate the risk level of a domain, and, if a high enough score, block the domain on OpenDNS Umbrella for 60 minutes, after approval via user prompt of a role.

[Phishing Investigate & Response](https://github.com/phantomcyber/playbooks/blob/4.2/phishing_investigate_and_respond.py)

Use various 3rd party services to investigate and remediate phishing emails with Admin approval.
