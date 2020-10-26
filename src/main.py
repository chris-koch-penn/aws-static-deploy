import route53
import acm
import s3
import cloudfront
import sys

domain = sys.argv[1]
if domain.startswith("www."):
    domain = domain[4:]

rootdir = sys.argv[2]

if "." not in domain:
    print(
        "This is not a valid domain name. It does not contain a TLD. Please try again."
    )
    exit(0)

zone_exists = route53.check_if_zone_exists_by_domain(domain)
if not zone_exists:
    # Create Hosted Zone
    res = route53.create_hosted_zone(domain)
    hosted_zone = res["HostedZone"]
    print(hosted_zone["Id"])

    # Create ACM Certificate and get DNS validation record
    arn = acm.create_ACM_certificate(domain)
    record = acm.get_DNS_records_for_validation(arn)
    print(record)

    # Upload Validation record to Route53
    res = route53.create_DNS_validation_record(record, hosted_zone["Id"])
    print(res)

if not s3.check_if_bucket_exists(domain):
    print("Setting website configurations ...")
    res = s3.create_bucket(domain)
    print(res)
    res = s3.set_bucket_website_config(domain)
    print(res)

files = s3.glob_files(rootdir)
s3.sync_website(domain, rootdir, files)

if not cloudfront.check_if_distribution_exists(domain):
    cert = acm.get_cert_arn(domain)
    res = cloudfront.create_distribution(domain, cert)
    print("Cloudfront Distribution created.")