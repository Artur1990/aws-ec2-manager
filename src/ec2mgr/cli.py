from __future__ import annotations

import argparse
import sys
from dotenv import load_dotenv

load_dotenv()

from .aws import (
    get_instance,
    list_instances,
    make_ec2_client,
    reboot_instance,
    set_name_tag,
    start_instance,
    stop_instance,
)
from .formatting import format_instances_table


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ec2mgr", description="Manage AWS EC2 instances safely.")
    p.add_argument("--region", default="us-east-1", help="AWS region, default: us-east-1")
    p.add_argument("--profile", default=None, help="AWS profile name (optional)")
    p.add_argument("--dry-run", action="store_true", help="Do not execute AWS call (DryRun)")

    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List instances")

    s = sub.add_parser("status", help="Show single instance status")
    s.add_argument("instance_id")

    s = sub.add_parser("start", help="Start instance")
    s.add_argument("instance_id")

    s = sub.add_parser("stop", help="Stop instance")
    s.add_argument("instance_id")

    s = sub.add_parser("reboot", help="Reboot instance")
    s.add_argument("instance_id")

    t = sub.add_parser("tag", help="Set Name tag (Name=...)")
    t.add_argument("instance_id")
    t.add_argument("tag", help="Example: Name=my-server")

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ec2 = make_ec2_client(region=args.region, profile=args.profile)

    try:
        if args.cmd == "list":
            items = list_instances(ec2)
            print(format_instances_table(items))
            return 0

        if args.cmd == "status":
            inst = get_instance(ec2, args.instance_id)
            print(format_instances_table([inst]))
            return 0

        if args.cmd == "start":
            start_instance(ec2, args.instance_id, dry_run=args.dry_run)
            print("OK")
            return 0

        if args.cmd == "stop":
            stop_instance(ec2, args.instance_id, dry_run=args.dry_run)
            print("OK")
            return 0

        if args.cmd == "reboot":
            reboot_instance(ec2, args.instance_id, dry_run=args.dry_run)
            print("OK")
            return 0

        if args.cmd == "tag":
            if not args.tag.startswith("Name="):
                raise ValueError("Only Name tag is supported in MVP. Use: Name=my-server")
            name = args.tag.split("=", 1)[1].strip()
            if not name:
                raise ValueError("Name cannot be empty.")
            set_name_tag(ec2, args.instance_id, name=name, dry_run=args.dry_run)
            print("OK")
            return 0

        raise ValueError("Unknown command")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
