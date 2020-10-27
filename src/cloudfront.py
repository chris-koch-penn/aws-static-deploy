from shared import boto_client, quit_on_error

cloudfront = boto_client("cloudfront")


def create_distribution(domain, cert_arn):
    config = {
        "CallerReference": domain,
        "Aliases": {"Quantity": 1, "Items": ["*." + domain, domain]},
        "DefaultRootObject": "index.html",
        "Comment": domain,
        "Enabled": True,
        "Origins": {
            "Quantity": 1,
            "Items": [
                {
                    "Id": "1",
                    "DomainName": domain + ".s3.amazonaws.com",
                    "S3OriginConfig": {"OriginAccessIdentity": ""},
                }
            ],
        },
        "DefaultCacheBehavior": {
            "TargetOriginId": "1",
            "ViewerProtocolPolicy": "redirect-to-https",
            "TrustedSigners": {"Quantity": 0, "Enabled": False},
            "ForwardedValues": {
                "Cookies": {"Forward": "all"},
                "Headers": {"Quantity": 0},
                "QueryString": False,
                "QueryStringCacheKeys": {"Quantity": 0},
            },
            "MinTTL": 43200,
        },
        "ViewerCertificate": {
            "ACMCertificateArn": cert_arn,
            "SSLSupportMethod": "sni-only",
            "CertificateSource": "acm",
        },
    }
    res = cloudfront.create_distribution(DistributionConfig=config)
    return res


def check_if_distribution_exists(domain):
    res = cloudfront.list_distributions()["DistributionList"]
    if "Items" in res:
        distros = [d for d in res["Items"] if d["Comment"] == domain]
        return len(distros) >= 1
    else:
        return False