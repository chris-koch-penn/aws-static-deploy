from shared import quit_on_error, extract_zoneid
import cloudfront
import route53
import acm
import s3
import time
import sys

domain = sys.argv[1]
if domain.startswith("www."):
    domain = domain[4:]

rootdir = sys.argv[2]

if "." not in domain:
    quit_on_error("This is not a valid domain name. It does not contain a TLD. \
        Please try again.")

#Create Hosted Zone if it does not exist.
zone_exists = route53.check_if_zone_exists_by_domain(domain)
if not zone_exists:
    # Create Hosted Zone.
    res = route53.create_hosted_zone(domain)
    hosted_zone = res["HostedZone"]
    quit_on_error("Please log in to AWS, find the DNS nameservers in the hosted zone for this domain, and \
        point your domain's DNS at the nameservers.")


# Create ACM Certificate and get DNS validation record.
cert = acm.get_cert_arn(domain, True)
hosted_zone = route53.get_hosted_zone(domain)
zone_id = extract_zoneid(hosted_zone)
if not cert:
    # Create and get record.
    arn = acm.create_ACM_certificate(domain)
    record = acm.get_DNS_records_for_validation(arn)

    # Upload Validation record to Route53.
    if not zone_id:
        quit_on_error("Could not find Hosted Zone for this domain.")
    else:
        res = route53.create_DNS_validation_record(record, zone_id)
        print(res)


# Create and configure S3 bucket.
if not s3.check_if_bucket_exists(domain):
    print("Setting website configurations ...")
    res = s3.create_bucket(domain)
    res = s3.set_bucket_website_config(domain)

# Sync with S3 bucket.
s3.set_public_policy(domain)
files = s3.glob_files(rootdir)
s3.sync_website(domain, rootdir, files)

# Invalidate the current distribution.
if cloudfront.check_if_distribution_exists(domain):
    cloudfront.create_invalidation(domain)
    print("Stale Cloudfront distribution invalidated.")

# Create new Cloudfront distribution.
cert = acm.get_cert_arn(domain)
try:
    res = cloudfront.create_distribution(domain, cert)
    cloudfront_url = res["Distribution"]["DomainName"]
    cloudfront_zone_id = "Z2FDTNDATAQYW2"
    res2 = route53.add_A_record_alias(zone_id, domain, cloudfront_url, cloudfront_zone_id)
except:
    pass

print("Cloudfront distribution created.")