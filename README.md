# GCP External IP addresses

The script helps with gathering all external IP addresses used in your GCP for auditing purposes.

- Use it with or without a service account key file.
- Gather the data for specific project or all projects in org.
- Upload the data to google sheet for tracking.


## Usage

Install the dependencies

```sh
pip install -r requirements
```
 If you wanted to run the script without using the service account key file enable the application-default login using gcloud
```sh
 gcloud auth application-default login
```
Else if the API access auth to be done via using service acc key file uncomment the line #9 before execution and provice the path on same

Once the requirements are set use below format to scan for specific project-id
```sh
python3 gcp_external_addresses.py project-id-here
```

if you wanted to scan across all projects that belongs to your organization no arguments needs to be passed, ensure permissions for respective account is provided on org level
```sh
python3 gcp_external_addresses.py
```

If the gathered data needs to be uploaded to google sheet remove the docstrings from line #73 & #101
Change the respective lines on #75 & #91 accordingly

## Documentation on resources
| Docs | link |
| ------ | ------ |
| IP-addresses | https://cloud.google.com/compute/docs/ip-addresses |
| REST API  | https://cloud.google.com/compute/docs/reference/rest/v1/addresses |
| Gcloud GLB open ports | https://cloud.google.com/load-balancing/docs/https#open_ports |
| Client libraries for auth | https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev |
| Medium | https://medium.com/google-cloud/before-an-attacker-discovers-your-cloud-be-aware-of-the-endpoints-you-have-exposed-to-the-internet-17d26f1c0aab |
