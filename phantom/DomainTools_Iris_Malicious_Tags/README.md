## DomainTools Iris Malicious Tags Playbook

This playbook retrieves the Iris Investigate profile of a domain and automatically flags domains that have been tagged as malicious in DomainTools Iris. The list of malicious tags are configurable by the analyst and can be kept up to date for automation.

#### Before Installing
In this directory there is a csv called iris_malicious_tags.csv. You will need to copy the contents of this into a custom list on your instance with the same name. The values in the list can be changed to any tags you wish to have flagged.

#### Installation 
After creating the custom list mentioned above, download the tar file in this directory and import the PB using that file. The assets in PB are for your DomainTools credentials. Point the asset to your dt credentials asset, save the PB and give it a shot.