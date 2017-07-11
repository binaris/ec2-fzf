import json
import os
import boto3

KEYS = os.environ["tags"].split(" ")
BUCKET = os.environ["bucket"]


def extract_tag(instance_desc, tag):
    if 'Tags' not in instance_desc:
        return ""
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
        print "Looking up instances in %s" % region

        instance_info = []
        for res in ec2.describe_instances()['Reservations']:
            print "Parsing reservation with %d instances..." % (len(res['Instances']))
            for i in res['Instances']:
                try:
                    e = extract_relevant_instance_info(i)
                    e['region'] = region
                    if e['pub_ip']:
                        instance_info.append(e)
                        print e
                    else:
                        print "Instance %s doesn't have a public IP address." % i['InstanceId']
                except Exception as e:
                    print "Failed to parse instance :(", e

        print "Found %d instances" % len(instance_info)
        return instance_info
    except Exception as e:
        print e
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


#pylint: disable=W0613
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
