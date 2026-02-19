from ec2mgr.aws import list_instances, start_instance, stop_instance


class FakeEC2:
    def __init__(self):
        self.calls = []

    def describe_instances(self):
        return {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-1",
                            "InstanceType": "t3.micro",
                            "State": {"Name": "running"},
                            "PublicIpAddress": "1.2.3.4",
                            "PrivateIpAddress": "10.0.0.1",
                            "Tags": [{"Key": "Name", "Value": "demo"}],
                        }
                    ]
                }
            ]
        }

    def start_instances(self, InstanceIds, DryRun=False):
        self.calls.append(("start", InstanceIds, DryRun))
        return {"ok": True}

    def stop_instances(self, InstanceIds, DryRun=False):
        self.calls.append(("stop", InstanceIds, DryRun))
        return {"ok": True}


def test_list_instances_parses():
    ec2 = FakeEC2()
    items = list_instances(ec2)
    assert len(items) == 1
    assert items[0].instance_id == "i-1"
    assert items[0].name == "demo"
    assert items[0].state == "running"


def test_start_stop_calls():
    ec2 = FakeEC2()
    start_instance(ec2, "i-1", dry_run=True)
    stop_instance(ec2, "i-1", dry_run=False)

    assert ec2.calls[0] == ("start", ["i-1"], True)
    assert ec2.calls[1] == ("stop", ["i-1"], False)
