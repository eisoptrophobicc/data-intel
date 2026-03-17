def detect_chart(data):

    if not data:
        return {"type": "table"}

    row = data[0]

    numeric = []
    categorical = []

    for col, val in row.items():

        if isinstance(val, (int, float)):
            numeric.append(col)
        else:
            categorical.append(col)

    # KPI
    if len(data) == 1 and len(numeric) == 1:
        return {
            "type": "kpi",
            "value": numeric[0]
        }

    # Time series → Line
    if "timestamp" in row or "date" in row:
        return {
            "type": "line",
            "x": "timestamp" if "timestamp" in row else "date",
            "y": numeric[0] if numeric else None
        }

    # Pie chart (percentage column)
    for col in numeric:
        if "percent" in col or "%" in col:
            return {
                "type": "pie",
                "labels": categorical[0] if categorical else None,
                "values": col
            }

    # Radar (multiple metrics)
    if len(categorical) >= 1 and len(numeric) >= 3:
        return {
            "type": "radar",
            "category": categorical[0],
            "metrics": numeric
        }

    # Grouped bar
    if len(categorical) == 1 and len(numeric) > 1:
        return {
            "type": "grouped_bar",
            "x": categorical[0],
            "y": numeric
        }

    # Bar
    if len(categorical) == 1 and len(numeric) == 1:
        return {
            "type": "bar",
            "x": categorical[0],
            "y": numeric[0]
        }

    # Scatter
    if len(numeric) >= 2:
        return {
            "type": "scatter",
            "x": numeric[0],
            "y": numeric[1]
        }

    return {"type": "table"}