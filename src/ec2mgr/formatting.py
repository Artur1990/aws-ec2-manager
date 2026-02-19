from __future__ import annotations

from typing import Iterable

from .aws import InstanceInfo


def format_instances_table(items: Iterable[InstanceInfo]) -> str:
    rows = list(items)
    headers = ["InstanceId", "Name", "State", "Type", "PublicIP", "PrivateIP"]
    data = [
        [r.instance_id, r.name, r.state, r.instance_type, r.public_ip, r.private_ip] for r in rows
    ]

    # простой табличный вывод без внешних библиотек
    cols = list(zip(headers, *data)) if data else [(h,) for h in headers]
    widths = [max(len(str(x)) for x in col) for col in cols]

    def fmt_row(row):
        return "  ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))

    out = [fmt_row(headers)]
    out.append("  ".join("-" * w for w in widths))
    for row in data:
        out.append(fmt_row(row))
    return "\n".join(out)
