from shared import boto_client, quit_on_error

cloudfront = boto_client("cloudfront")


def create_distribution(domain, cert_arn):
    config = {
        "CallerReference": domain,
        "Aliases": {"Quantity": 1, "Items": [domain]},
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
            # 'CloudFrontDefaultCertificate': True|False,
            # 'IAMCertificateId': 'string',
            "ACMCertificateArn": cert_arn,
            "SSLSupportMethod": "sni-only",
            # 'MinimumProtocolVersion': 'SSLv3'|'TLSv1'|'TLSv1_2016'|'TLSv1.1_2016'|'TLSv1.2_2018'|'TLSv1.2_2019',
            # 'Certificate': 'string',
            # 'CertificateSource': 'cloudfront'|'iam'|'acm'
            "CertificateSource": "acm",
        },
    }
    res = cloudfront.create_distribution(DistributionConfig=config)
    return res


def check_if_distribution_exists(domain):
    res = cloudfront.list_distributions()["DistributionList"]
    print(res)
    if "Items" in res:
        distros = [d for d in res["Items"] if d["DomainName"] == domain]
        return bool(len(distros))
    else:
        return False