from ec2mgr.cli import build_parser


def test_parser_list():
    p = build_parser()
    args = p.parse_args(["list"])
    assert args.cmd == "list"
    assert args.region == "us-east-1"
    assert args.dry_run is False


def test_parser_tag():
    p = build_parser()
    args = p.parse_args(["--region", "eu-west-1", "--dry-run", "tag", "i-123", "Name=test"])
    assert args.cmd == "tag"
    assert args.region == "eu-west-1"
    assert args.dry_run is True
    assert args.instance_id == "i-123"
    assert args.tag == "Name=test"
