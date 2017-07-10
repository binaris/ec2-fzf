import json
import boto3
import os

KEYS = "realm service Name".split(" ")
BUCKET = os.environ["bucket"]

def extract_tag(instance_desc, tag):
    t = [t for t in instance_desc['Tags'] if t['Key'] == tag]
    return t[0]['Value'] if t else ""


def extract_relevant_instance_info(instance_description):
    i = instance_description
    r = {
        "id": i.get("InstanceId"),
        "pub_ip": i.get("PublicIpAddress"),
        "priv_ip": i.get("PrivateIpAddress"),
        "key": i.get("KeyName"),
    }
    for k in KEYS:
        r[k] = extract_tag(i, k)
    return r

def instances_by_region(region):
    try:
        ec2 = boto3.client('ec2', region_name=region)

        instance_info = []
        for res in ec2.describe_instances()['Reservations']:
            for i in res['Instances']:
                e = extract_relevant_instance_info(i)
                e['region'] = region
                if e['pub_ip']:
                    instance_info.append(e)

        return instance_info
    except Exception as e:
        return []

def instance_line(inst):
    keys = KEYS + "priv_ip id region pub_ip key".split(" ")
    return " ".join([inst[k] for k in keys if inst[k]])

def save_in_s3(body):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET,
                  Key='instances.fzf',
                  Body=body.encode('utf-8'))
    print "updated: s3://%s/instances.fzf" % BUCKET


def main(event, context):
    client = boto3.client('ec2')
    regions = client.describe_regions()
    region_names = [r["RegionName"] for r in regions["Regions"]]

    all_instances = []
    for r in region_names:
        all_instances += instances_by_region(r)

    lines = [instance_line(i) for i in all_instances]
    lines = sorted(lines)
    body = "\n".join(lines)
    save_in_s3(body)
    response = {
        "statusCode": 200,
        "body": body
    }

    return response
