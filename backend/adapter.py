def adapt_result(result, question):

    chart = result.get("chart", {})
    data = result.get("data", [])

    if not data:
        
        return {
            "title": title,
            "summary": "No data available for this query.",
            "sql": sql,
            "kpis": [],
            "charts": []
        }

    chart_type = chart.get("type")

    title = question
    summary = result.get("insight")
    sql = result.get("sql")

    if chart_type == "kpi" and data:

        key = chart.get("value")
        value = data[0].get(key, 0)

        return {
            "title": title,
            "summary": summary,
            "sql": sql,
            "kpis": [
                {
                    "label": key.replace("_", " ").title(),
                    "value": round(value, 2) if isinstance(value, float) else value,
                    "delta": "",
                    "trend": "neutral",
                    "sub": ""
                }
            ],
            "charts": []
        }

    if chart_type == "pie":

        labels = chart.get("labels")
        values = chart.get("values")

        pie_data = [
            {"name": row.get(labels), "value": row.get(values)}
            for row in data
        ]

        return {
            "title": title,
            "summary": summary,
            "sql": sql,
            "kpis": [],
            "charts": [
                {
                    "id": "c1",
                    "type": "pie",
                    "title": title,
                    "data": pie_data
                }
            ]
        }

    if chart_type == "radar":

        metrics = chart.get("metrics", [])

        radar_data = [
            {"metric": m, "value": data[0].get(m)}
            for m in metrics
        ]

        return {
            "title": title,
            "summary": summary,
            "sql": sql,
            "kpis": [],
            "charts": [
                {
                    "id": "c1",
                    "type": "radar",
                    "title": title,
                    "data": radar_data
                }
            ]
        }

    if chart_type == "grouped_bar":

        x = chart.get("x")
        ys = chart.get("y", [])

        colors = ["#D4A854", "#4F46E5", "#10B981", "#F59E0B"]

        return {
            "title": title,
            "summary": summary,
            "sql": sql,
            "kpis": [],
            "charts": [
                {
                    "id": "c1",
                    "type": "bar",
                    "title": title,
                    "data": data,
                    "xKey": x,
                    "yKeys": [
                        {
                            "key": y,
                            "label": y.replace("_", " ").title(),
                            "color": colors[i % len(colors)]
                        }
                        for i, y in enumerate(ys)
                    ]
                }
            ]
        }

    if chart_type == "scatter":

        return {
            "title": title,
            "summary": summary,
            "sql": sql,
            "kpis": [],
            "charts": [
                {
                    "id": "c1",
                    "type": "scatter",
                    "title": title,
                    "data": data,
                    "xKey": chart.get("x"),
                    "yKey": chart.get("y")
                }
            ]
        }

    if chart_type == "line":

        x = chart.get("x")
        y = chart.get("y")

        return {
            "title": title,
            "summary": summary,
            "sql": sql,
            "kpis": [],
            "charts": [
                {
                    "id": "c1",
                    "type": "line",
                    "title": title,
                    "data": data,
                    "xKey": x,
                    "yKeys": [
                        {
                            "key": y,
                            "label": y,
                            "color": "#D4A854"
                        }
                    ]
                }
            ]
        }

    if chart_type == "bar":

        x = chart.get("x")
        y = chart.get("y")

        return {
            "title": title,
            "summary": summary,
            "sql": sql,
            "kpis": [],
            "charts": [
                {
                    "id": "c1",
                    "type": "bar",
                    "title": title,
                    "data": data,
                    "xKey": x,
                    "yKeys": [
                        {
                            "key": y,
                            "label": y,
                            "color": "#D4A854"
                        }
                    ]
                }
            ]
        }

    return {
        "title": title,
        "summary": summary,
        "sql": sql,
        "kpis": [],
        "charts": []
    }

    