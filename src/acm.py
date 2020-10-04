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
	res = client.describe_certificate(CertificateArn=arn)
	records = res["Certificate"]["DomainValidationOptions"]["ResourceRecord"]
	return records