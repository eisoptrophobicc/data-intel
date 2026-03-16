def format_value(value):
    """
    Safely format SQL values.
    Numbers stay raw, strings get quotes.
    """

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, str):
        return f"'{value}'"

    return str(value)

def build_filter(filter_obj):
    """
    Convert a filter object into SQL.
    """

    col = filter_obj.get("column")
    op = filter_obj.get("op")
    value = filter_obj.get("value")

    if col is None or op is None:
        return None

    if op == "=":
        return f"{col} = {format_value(value)}"

    if op in [">", "<", ">=", "<="]:
        return f"{col} {op} {format_value(value)}"

    if op == "LIKE":
        return f"{col} LIKE '%{value}%'"

    if op == "IN":
        if not isinstance(value, list):
            return None
        values = ", ".join(format_value(v) for v in value)
        return f"{col} IN ({values})"

    if op == "BETWEEN":
        if not isinstance(value, list) or len(value) != 2:
            return None
        start, end = value
        return f"{col} BETWEEN {format_value(start)} AND {format_value(end)}"

    return None

def generate_select(metrics, aggregation, group_by):
    """
    Build SELECT clause.
    """

    select_parts = []

    # group columns first
    for g in group_by:
        select_parts.append(g)

    # aggregated metrics
    if aggregation and metrics:
        for m in metrics:
            alias = f"{aggregation.lower()}_{m}"
            select_parts.append(f"{aggregation}({m}) AS {alias}")

    # COUNT(*) case
    elif aggregation == "COUNT" and not metrics:
        select_parts.append("COUNT(*) AS count")

    # raw metrics
    elif metrics:
        select_parts.extend(metrics)

    # fallback
    else:
        select_parts.append("*")

    return "SELECT " + ", ".join(select_parts)

def generate_where(filters):
    """
    Build WHERE clause.
    """

    if not filters:
        return ""

    clauses = []

    for f in filters:

        clause = build_filter(f)

        if clause:
            clauses.append(clause)

    if not clauses:
        return ""

    return "WHERE " + " AND ".join(clauses)

def generate_group_by(group_by):
    """
    Build GROUP BY clause.
    """

    if not group_by:
        return ""

    return "GROUP BY " + ", ".join(group_by)

def generate_order_by(order_by, order, aggregation, metrics):
    """
    Build ORDER BY clause.
    """

    if not order_by:
        return ""

    order = order or "DESC"

    if aggregation and order_by in metrics:
        return f"ORDER BY {aggregation}({order_by}) {order}"

    return f"ORDER BY {order_by} {order}"

def generate_limit(limit):
    """
    Build LIMIT clause.
    """

    if limit is None:
        return ""

    return f"LIMIT {limit}"

def generate_sql(plan, table_name="youtube_videos_staging"):
    """
    Convert query plan → SQL query.
    """

    metrics = plan.get("metrics", [])
    aggregation = plan.get("aggregation")
    group_by = plan.get("group_by", [])
    filters = plan.get("filters", [])
    order_by = plan.get("order_by")
    order = plan.get("order")
    limit = plan.get("limit")

    select_clause = generate_select(metrics, aggregation, group_by)

    where_clause = generate_where(filters)

    group_clause = generate_group_by(group_by)

    order_clause = generate_order_by(order_by, order, aggregation, metrics)

    limit_clause = generate_limit(limit)

    parts = [
        select_clause,
        f"FROM {table_name}",
        where_clause,
        group_clause,
        order_clause,
        limit_clause
    ]

    sql = " ".join(part for part in parts if part)

    return sql