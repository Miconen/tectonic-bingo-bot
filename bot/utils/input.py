def sanitize_string(s: str):
    special_chars = [" ", "-", "_", ".", ",", "!", "?", ":", ";", "'", '"', "`", "’"]

    for i in range(len(special_chars)):
        s = s.replace(special_chars[i], "")

    return s.strip().lower()
