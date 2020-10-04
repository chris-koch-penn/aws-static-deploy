import acm
import route53
import sys
import pickle

domain = sys.argv[1]
if domain.startswith("www."): 
    domain = domain[4:]

# Create Hosted Zone
res = route53.create_hosted_zone(domain)
hosted_zone = res["HostedZone"]
print(hosted_zone)
pickle.dump(hosted_zone, open("hosted_zone.pkl", "wb"))

# Create ACM Certificate and get DNS validation record
arn = acm.create_ACM_certificate(domain)
records = acm.get_DNS_records_for_validation(arn)
print(records)
pickle.dump(records, open("obj.pkl", "wb"))

# Upload Validation record to Route53


# acm.main(domain)