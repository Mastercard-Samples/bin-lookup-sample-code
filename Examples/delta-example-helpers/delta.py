"""Apply BIN delta insert/update/delete operations to a local snapshot (B + D = B')."""

NON_DATA = {"operation", "changedFields"}  # delta metadata, not BIN range data


def row_key(row):
    """Identity key used to match a row across B, D, B' and R."""
    return str(row.get("lowAccountRange", "")), str(row.get("highAccountRange", ""))


def apply_delta(rows, delta_items, field_mapping):
    """
    Apply `delta_items` to `rows` in place, turning B into B'.

    Args:
        rows: base snapshot (B) rows, mutated in place.
        delta_items: delta items, each with an "operation" of I, U or D.
        field_mapping: B field name -> R field name (see fields.build_field_mapping).

    Returns:
        Counts of applied inserts/updates/deletes and skipped items (key not found).
    """
    from .fields import normalize_row  # local import avoids a circular import with fields.py

    index = {row_key(row): i for i, row in enumerate(rows)}
    stats = {"I": 0, "U": 0, "D": 0, "skip": 0}

    for item in delta_items:
        operation = item.get("operation")
        key = (str(item.get("lowAccountRange", "")), str(item.get("highAccountRange", "")))

        if operation == "D":
            index_row = index.get(key)
            if index_row is None:
                stats["skip"] += 1
                continue
            rows.pop(index_row)
            index = {row_key(row): i for i, row in enumerate(rows)}  # positions shifted
            stats["D"] += 1

        elif operation == "I":
            new_row = normalize_row(
                {field_name: field_value for field_name, field_value in item.items() if field_name not in NON_DATA},
                field_mapping,
            )
            rows.append(new_row)
            index = {row_key(row): i for i, row in enumerate(rows)}
            stats["I"] += 1

        elif operation == "U":
            index_row = index.get(key)
            if index_row is None:
                stats["skip"] += 1
                continue
            # Only touch listed fields; fall back to all data fields if the list is missing.
            changed_fields = item.get("changedFields") or [
                field_name for field_name in item if field_name not in NON_DATA
            ]
            for field in changed_fields:
                target_field = field_mapping.get(field)
                if target_field and target_field in rows[index_row]:
                    rows[index_row][target_field] = str(item.get(field, "") or "")
            stats["U"] += 1

        else:
            stats["skip"] += 1

    return stats
