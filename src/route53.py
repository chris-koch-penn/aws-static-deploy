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


def get_hosted_zone(domain):
	try:
		res = client.list_hosted_zones_by_name(DNSName=domain, MaxItems='1')
		if bool('HostedZones' in res.keys()
			and len(res['HostedZones']) > 0
			and res['HostedZones'][0]['Name'].startswith(domain)):
			return res['HostedZones'][0]
		else:
			raise Exception("Hosted zone for this domain could not be found.")
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


def add_A_record_alias(zoneid, domain_name, value, zoneid_alias):
	try:
		res = client.change_resource_record_sets(
			HostedZoneId=zoneid,
			ChangeBatch={
				'Changes': [
					{
						'Action': 'CREATE',
						'ResourceRecordSet': {
							'AliasTarget': {
								'DNSName': value,
								'EvaluateTargetHealth': False,
								'HostedZoneId': zoneid_alias,
							},
							'Name': domain_name,
							'Type': 'A'
						},
					}
				]
			})
		return res 
	except Exception:
		# TODO: Entering this branch usually means that the A record already exists. We should check to
		# see if this is the case instead of wrapping everything in an error block.
		return