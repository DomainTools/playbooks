## DomainTools Phantom Playbooks

Working playbooks and automation scripts for Splunk Phantom. 

#### Installation
For the DomainTools playbooks in this repo, an asset called `domaintoolsiriscreds` is needed with
DomainTools API username and key. The playbooks expect this asset to exist to make the API calls needed for the playbook data upon execution. Installation instructions for each playbook is in the README at the root of the playbook’s directory.
<br>

#### Current Playbooks In This Repo

##### DomainTools Domain Risk Score
Get the Domain Risk Score and throw an Alert for the Analyst to manually review the domain artifact. Users can block the domain.
##### DomainTools Guided Pivots
Retrieve the Iris Investigate profile of the domain and automatically identify potential connected infrastructure related to artifacts based on DomainTools Guided Pivot value. The pivot value is set to 200 and can be tailored per investigation objectives.
##### DomainTools Iris Malicious Tags
Retrieve the Iris Investigate profile of a domain and automatically flag domains that have been tagged as malicious in DomainTools Iris. The list of malicious tags are configurable by the analyst and can be kept up to date for automation.

#### Third party made playbooks, that work with DomainTools data
[Investigate](https://github.com/phantomcyber/playbooks/blob/4.2/investigate.py)

Use varied services to execute a wide range of investigative queries across all available assets.

[User Prompt and Block Domains](https://github.com/phantomcyber/playbooks/blob/4.2/user_prompt_and_block_domain.py)

Utilize DomainTools to generate the risk level of a domain, and, if a high enough score, block the domain on OpenDNS Umbrella for 60 minutes, after approval via user prompt of a role.

[Phishing Investigate & Response](https://github.com/phantomcyber/playbooks/blob/4.2/phishing_investigate_and_respond.py)
 
Use various 3rd party services to investigate and remediate phishing emails with Admin approval.

