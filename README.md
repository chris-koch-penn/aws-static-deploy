# AWS Static Site Deployment Tool
This project deploys sites statically to AWS S3 buckets and serves them from behind a Cloundfront CDN with HTTPS setup.

Running the shell script ./upload_site does the following:
1. Creates a TLS certificate through ACM.
2. Uses Route53 DNS to validate that certificate.
3. Creates an S3 bucket.
4. Creates a Cloudfront distribution pointed to that S3 bucket using the ACM certificate.
5. Creates an apex dns record pointing to that Cloudfront.
6. Syncs the specified directory to the S3 bucket.
7. Invalidates the Cloudfront cache.

The main Python script can be run like so with the following arguments:
```bash
python <relative path to aws-static-deploy/src/main.py >  <apex domain name> <path to static site's root> 
```

## Requirements to Deploy
+ The static site's root directory must contain an entrypoint named index.html.
+ Your domain needs to be registered with AWS Route53.
+ Must have have the following environment variables set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION


## MIT License
MIT License, do whatever you want with this project.

This project was inspired by a static site deployment tool originally written in Go somewhere here on Github (I can find the repo anymore).
