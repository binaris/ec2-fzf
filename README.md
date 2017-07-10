# EC2 SSH Fuzzy Finder

Type `ec2` and you'll get an interactive fuzzy finder of all the instances in your EC2 account that have a public IP.

![screenshot](https://cdn.assaflavie.com/monosnap/1._binaris_bash_2017-07-10_15-47-01.png)

ENTER to select an instance and SSH into it.

This script assumes you EC2 SSH private key exists in `~/.ssh/[key-name].pem`.

# How this works

Instead of calling DescribeInstance on demand (which is painfully slow), this project contains a Serverless Lambda function that fetches the entire list of instances every minute and caches it in S3.

The bucket is accessible only to the IAM group `dev`. Tweak this with your org's relevant group name as appropriate.

## Lambda Configuration (per organization)

You can tweak the following to suit your organization:

1. In `serverless.yml` you can change the IAM group name (default is `dev`) that's allowed to see the list of instances this tool caches.
1. In `handler.py` you can tweak the list of EC2 tags that are relevant for you to be able to identify an instance. Look at the `TAGS` const.

To deploy, run `make deploy`. It's a good idea to test locally first with `make run_local`.

# Installing

You'll need [FZF](https://github.com/junegunn/fzf#installation) (the fuzzy finder).

You'll also need the AWS CLI installed locally (`pip install awscli`).

And of course your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_ID` envars should be defined.


