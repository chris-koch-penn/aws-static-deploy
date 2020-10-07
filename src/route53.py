from shared import boto_client
from uuid import uuid4
client = boto_client("route53")


def check_if_zone_exists_by_domain(domain):
	try:
		res = client.list_hosted_zones_by_name(DNSName=domain, MaxItems='1')
		return bool('HostedZones' in res.keys()
			and len(res['HostedZones']) > 0
			and res['HostedZones'][0]['Name'].startswith(domain))
	except:
		print("Error checking if Hosted Zone exists for domain.")
		return False

def create_hosted_zone(domain):
	res = client.create_hosted_zone(
		Name=domain,
		CallerReference=str(uuid4()),
		HostedZoneConfig={ 'PrivateZone': False }
	)
	return res

def create_DNS_validation_record(dns_record, zoneid):
	name, value = dns_record["Name"], dns_record["Value"]
	return add_cname_record(name, value, "CREATE", 300, zoneid)

def add_cname_record(name, value, action, ttl, zoneid):
	try:
		return client.change_resource_record_sets(
			HostedZoneId=zoneid,
			ChangeBatch= {
			'Comment': 'add %s -> %s' % (name, value),
			'Changes': [{
				'Action': action,
				'ResourceRecordSet': {
				'Name': name,
				'Type': "CNAME",
				'TTL': ttl,
				'ResourceRecords': [{'Value': value}]
			}}]
		})
	except Exception as e:
		print(e)
		return "Failed to create CName DNS record. Please try again later."