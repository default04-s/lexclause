# ===== CHANGED =====
# Renamed to support different document types in the future.
def extract_text(file_path):

    # ===== CHANGED =====
    # Read text directly from a .txt file.
    with open(file_path, "r", encoding="utf-8") as file:
        full_text = file.read()

    return full_text