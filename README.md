# Serverless Deploy
For static websites in the root directory:
1. Creates a TLS certificate through ACM
2. Uses route53 DNS to validate that certificate
3. Creates an S3 bucket
4. Creates a cloudfront distribution pointed to that S3 bucket using the ACM certificate
5. Creates an apex dns record pointing to that cloudfront.
6. Syncs the current directory to that S3 bucket.
7. Invalidates the cloudfront cache.

TLDR: Cheap, painless, fast, bulletproof flatfile sites with https and an apex domain.
