def bytes_to_mb(size):

    if not size:
        return "Unknown"

    return round(size / (1024 * 1024), 2)