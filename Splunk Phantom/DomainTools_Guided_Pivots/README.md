## DomainTools Guided Pivots Playbook

This playbook retrieves the Iris Investigate profile of domain and automatically identifies potential connected infrastructure related to artifacts based on DomainTools Guided Pivot value. The pivot value is set based off of a configurable custom list.

#### Before Installing
In this directory there is a csv called domaintools_guided_pivot.csv. You will need to copy the contents of this into a custom list on your instance with the same name. The names in the first column are used by custom code on the decision blocks in the PB. The second column are the pivot values that you can adjust to what works best for your needs.

#### Installation 
After creating the custom list mentioned above, download the tar file in this directory and import the PB using that file. The assets in PB are for your DomainTools credentials. Point the asset to your dt credentials asset, save the PB and give it a shot.