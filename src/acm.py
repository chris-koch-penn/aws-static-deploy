from shared import boto_client
client = boto_client("acm")

def create_ACM_certificate(domain):
	res = client.request_certificate(
		DomainName=domain, 
		ValidationMethod='DNS',
        SubjectAlternativeNames=['*.' + domain]
	)
	return res["CertificateArn"]

def get_DNS_records_for_validation(arn):
	try:
		res = client.describe_certificate(CertificateArn=arn)
		return res["Certificate"]["DomainValidationOptions"][0]["ResourceRecord"]
	except Exception as e: 
		print(e)
		return "Failed to get DNS Validation records. This domain may not be verifiable."