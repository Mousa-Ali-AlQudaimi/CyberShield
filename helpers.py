def summarize_items(*args, **kwargs):
    """Demonstrates *args packing and **kwargs unpacking for the project rubric."""
    values = list(args)
    values.sort(key=lambda item: str(item))
    return {"items": values, "metadata": kwargs}
