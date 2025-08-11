

from typing import List, Dict, Any

def parse_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parse raw data from APIs into a standardized format.

    :param raw_data: List of dictionaries containing raw data from APIs.
    :return: List of dictionaries with the following fields:
        - 'service' (str): Name of the service/source of the breach.
        - 'breach_date' (str): Date of the breach (if known).
        - 'data_types' (List[str]): Types of data that were breached.
        - 'description' (str): Optional description of the breach.
    """
    seen = set()
    parsed_results = []

    for item in raw_data:
        if "service_name" in item and "breach_date" in item:
            # Format from LeakCheck API
            service = item.get("service_name") or "Unknown"
            breach_date = item.get("breach_date") or ""
            description = item.get("description") or ""
            data_classes = item.get("data_types", [])
        elif "Name" in item or "name" in item:
            # Format from another API
            service = item.get("Name") or item.get("name") or "Unknown"
            breach_date = item.get("BreachDate") or item.get("date") or ""
            description = item.get("Description") or item.get("description") or ""
            data_classes = (
                item.get("DataClasses") or
                item.get("dataClasses") or
                item.get("data_classes") or
                []
            )
        else:
            # Unknown format, skip
            continue

        if isinstance(data_classes, str):
            data_classes = [data_classes]
        elif not isinstance(data_classes, list):
            data_classes = []

        key = (service.lower(), breach_date, tuple(sorted(dt.lower() for dt in data_classes)))

        if key in seen:
            continue
        seen.add(key)

        parsed_results.append({
            "service": service,
            "breach_date": breach_date,
            "data_types": data_classes,
            "description": description
        })

    return parsed_results
