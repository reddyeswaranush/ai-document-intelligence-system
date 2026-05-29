import easyocr


# -----------------------------------------------------
# Initialize OCR model
# -----------------------------------------------------
reader = easyocr.Reader(
    ['en'],
    gpu=False
)


# -----------------------------------------------------
# Extract text from image
# -----------------------------------------------------
def extract_text(image_path):

    results = reader.readtext(

        image_path,

        detail=1,

        paragraph=True
    )


    extracted_text = ""

    total_confidence = 0

    valid_confidence_count = 0


    # -------------------------------------------------
    # Process OCR results safely
    # -------------------------------------------------
    for result in results:


        # ---------------------------------------------
        # Extract text safely
        # ---------------------------------------------
        if len(result) > 1:

            detected_text = result[1]

            extracted_text += detected_text + "\n"


        # ---------------------------------------------
        # Extract confidence safely
        # ---------------------------------------------
        if len(result) > 2:

            confidence = result[2]

            total_confidence += confidence

            valid_confidence_count += 1


    # -------------------------------------------------
    # Calculate average confidence
    # -------------------------------------------------
    if valid_confidence_count > 0:

        average_confidence = (

            total_confidence
            / valid_confidence_count

        ) * 100

    else:

        average_confidence = 0


    print(
        f"\nOCR Confidence: {average_confidence:.2f}%\n"
    )


    return extracted_text