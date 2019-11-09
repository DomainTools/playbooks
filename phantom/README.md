## DomainTools Phantom Playbooks

Welcome to our Phantom playbooks. These playbooks are ready for you to use, just import them into your phantom instance. 

Most of these playbooks are keyed off of a Phantom Custom List. You can create custom lists under the playbooks page in Phantom. A custom list with the correct name and attributes will be provided with these playbooks. You will have to create the list manually on your instance before importing the playbook. Documentation can be found in a README in the individual PB folders as well as the PB itself.

When you import the playbook, be sure to adjust the playbook settings to your liking. All playbooks are set to inactive. You will need to update the DomainTools creds asset, along with ensuring the playbook is connected to the custom list.

### Current Playbooks In This Repo

##### DomainTools Domain Risk Score
This playbook retrieves the Domain Risk Score and throws an Alert for the Analyst to manually review the domain artifact. Users can block the domain 
##### DomainTools Guided Pivots
This playbook retrieves the Iris Investigate profile of domain and automatically identifies potential connected infrastructure related to artifacts based on DomainTools Guided Pivot value. The pivot value is set to 200 and can be tailored per investigation objectives.
##### DomainTools Iris Malicious Tags
This playbook retrieves the Iris Investigate profile of a domain and automatically flags domains that have been tagged as malicious in DomainTools Iris. The list of malicious tags are configurable by the analyst and can be kept up to date for automation

### DomainTools Related Playbooks (3rd party Developed)
[Investigate](https://github.com/phantomcyber/playbooks/blob/4.2/investigate.py)

This playbook uses varied services to execute a wide range of investigative queries across all available assets.

[User Prompt and Block Domains](https://github.com/phantomcyber/playbooks/blob/4.2/user_prompt_and_block_domain.py)

This playbook utilizes DomainTools to generate the risk level of a domain, and, if a high enough score, blocks the domain on OpenDNS Umbrella for 60 minutes, after approval via user prompt of a role.

[Phishing Investigate & Response](https://github.com/phantomcyber/playbooks/blob/4.2/phishing_investigate_and_respond.py)
 
This playbook uses various 3rdf party services to investigates and remediates phishing emails with Admin approval 
