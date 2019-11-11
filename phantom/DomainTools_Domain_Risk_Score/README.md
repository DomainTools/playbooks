## DomainTools Guided Pivots Playbook

This playbook retrieves the Domain Risk Score and throws an Alert for the Analyst to manually review the domain artifact. Users can block the domain.

#### Before Installing
In this directory there is a csv called domaintools_domain_risk_score.csv. You will need to copy the contents of this into a custom list on your instance with the same name. The name in the first column are used by custom code on the decision block in the PB. The second column is the minimum risk score you would like to alert on.

#### Installation 
After creating the custom list mentioned above, download the tar file in this directory and import the PB using that file. The assets in PB are for your DomainTools credentials. Point the asset to your dt credentials asset, change the manual response block to send a prompt to your desired role or user, and give it a shot.