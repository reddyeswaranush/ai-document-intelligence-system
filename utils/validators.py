# -----------------------------------------------------
# Validate uploaded files
# -----------------------------------------------------
def validate_uploaded_file(uploaded_file):

    allowed_extensions = [
        "png",
        "jpg",
        "jpeg",
        "pdf"
    ]


    extension = uploaded_file.name.split(".")[-1].lower()


    # File type validation
    if extension not in allowed_extensions:

        return "Unsupported file format"


    # File size validation
    # 5 MB limit
    if uploaded_file.size > 5 * 1024 * 1024:

        return "File size exceeds 5 MB"


    return None