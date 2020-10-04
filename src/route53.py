from shared import boto_client
from uuid import uuid4
client = boto_client("route53")

def get_DNS_zones():
	# Get hosted zones
	zones = client.list_hosted_zones()
	return zones

def create_hosted_zone(domain):
	res = client.create_hosted_zone(
		Name=domain,
		CallerReference=str(uuid4()),
		HostedZoneConfig={ 'PrivateZone': False }
	)
	return res

def create_DNS_validation_record(dns_record, ):
	response = client.change_resource_record_sets()
	# response = client.change_resource_record_sets(
    # HostedZoneId='string',
    # ChangeBatch={
	# 		'Changes': [
	# 			{
	# 				'Action': 'CREATE',
	# 				'ResourceRecordSet': {
	# 					'Name': 'string',
	# 					'Type': 'CNAME',
	# 					'SetIdentifier': 'string',
	# 					'ResourceRecords': [
	# 						{
	# 							'Value': 'string'
	# 						},
	# 					],
	# 					'AliasTarget': {
	# 						'HostedZoneId': 'string',
	# 						'DNSName': 'string',
	# 						'EvaluateTargetHealth': True|False
	# 					},
	# 					'HealthCheckId': 'string',
	# 					'TrafficPolicyInstanceId': 'string'
	# 				}
	# 			},
	# 		]
	# 	}
	# )