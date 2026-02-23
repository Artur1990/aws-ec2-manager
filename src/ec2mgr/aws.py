from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import boto3


@dataclass(frozen=True)
class InstanceInfo:
    instance_id: str
    name: str
    state: str
    instance_type: str
    public_ip: str
    private_ip: str


def _tag_value(tags: list[dict[str, str]] | None, key: str) -> str:
    if not tags:
        return ""
    for t in tags:
        if t.get("Key") == key:
            return t.get("Value", "") or ""
    return ""


def make_ec2_client(region: str, profile: str | None = None):
    if profile:
        session = boto3.Session(profile_name=profile, region_name=region)
        return session.client("ec2")
    return boto3.client("ec2", region_name=region)


def list_instances(ec2_client) -> list[InstanceInfo]:
    resp = ec2_client.describe_instances()
    out: list[InstanceInfo] = []

    for r in resp.get("Reservations", []):
        for inst in r.get("Instances", []):
            out.append(
                InstanceInfo(
                    instance_id=inst.get("InstanceId", ""),
                    name=_tag_value(inst.get("Tags"), "Name"),
                    state=(inst.get("State") or {}).get("Name", ""),
                    instance_type=inst.get("InstanceType", ""),
                    public_ip=inst.get("PublicIpAddress", "") or "",
                    private_ip=inst.get("PrivateIpAddress", "") or "",
                )
            )
    return out


def get_instance(ec2_client, instance_id: str) -> InstanceInfo:
    resp = ec2_client.describe_instances(InstanceIds=[instance_id])
    reservations = resp.get("Reservations", [])
    if not reservations or not reservations[0].get("Instances"):
        raise ValueError(f"Instance not found: {instance_id}")

    inst = reservations[0]["Instances"][0]
    return InstanceInfo(
        instance_id=inst.get("InstanceId", ""),
        name=_tag_value(inst.get("Tags"), "Name"),
        state=(inst.get("State") or {}).get("Name", ""),
        instance_type=inst.get("InstanceType", ""),
        public_ip=inst.get("PublicIpAddress", "") or "",
        private_ip=inst.get("PrivateIpAddress", "") or "",
    )


def start_instance(ec2_client, instance_id: str, dry_run: bool = False) -> dict[str, Any]:
    return ec2_client.start_instances(InstanceIds=[instance_id], DryRun=dry_run)


def stop_instance(ec2_client, instance_id: str, dry_run: bool = False) -> dict[str, Any]:
    return ec2_client.stop_instances(InstanceIds=[instance_id], DryRun=dry_run)


def reboot_instance(ec2_client, instance_id: str, dry_run: bool = False) -> dict[str, Any]:
    return ec2_client.reboot_instances(InstanceIds=[instance_id], DryRun=dry_run)


def set_name_tag(ec2_client, instance_id: str, name: str, dry_run: bool = False) -> dict[str, Any]:
    return ec2_client.create_tags(
        Resources=[instance_id],
        Tags=[{"Key": "Name", "Value": name}],
        DryRun=dry_run,
    )
