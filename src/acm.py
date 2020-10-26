from shared import boto_client, quit_on_error

client = boto_client("acm")


def create_ACM_certificate(domain):
    res = client.request_certificate(
        DomainName=domain,
        ValidationMethod="DNS",
        SubjectAlternativeNames=["*." + domain],
    )
    return res["CertificateArn"]


def get_DNS_records_for_validation(arn):
    try:
        res = client.describe_certificate(CertificateArn=arn)
        return res["Certificate"]["DomainValidationOptions"][0]["ResourceRecord"]
    except Exception as e:
        print(e)
        return (
            "Failed to get DNS Validation records. This domain may not be verifiable."
        )


def list_certs(status):
    return client.list_certificates(CertificateStatuses=[status])


def get_cert_arn(domain):
    issued = list_certs("ISSUED")["CertificateSummaryList"]
    pending = list_certs("PENDING_VALIDATION")["CertificateSummaryList"]
    issued = [c["CertificateArn"] for c in issued if c["DomainName"] == domain]
    pending = [c["CertificateArn"] for c in pending if c["DomainName"] == domain]
    if len(issued) == 0:
        if len(pending) == 0:
            quit_on_error(
                (
                    f"No Pending or Issued Certificates found for {domain}."
                    " Try updating your name servers."
                )
            )
        else:
            quit_on_error(
                (
                    f"Certificate for {domain} is pending."
                    " Try updating your name servers and waiting anywhere from"
                    " a few minutes to a few hours."
                )
            )
    else:
        return issued[0]