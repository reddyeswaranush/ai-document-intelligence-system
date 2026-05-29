import cv2


# -----------------------------------------------------
# Improve image quality before OCR
# -----------------------------------------------------
def preprocess_image(image_path):

    # Read image
    image = cv2.imread(image_path)


    # Resize image for better OCR accuracy
    image = cv2.resize(
        image,
        None,
        fx=2,
        fy=2
    )


    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # Reduce noise
    denoised = cv2.fastNlMeansDenoising(
        gray
    )


    # Sharpen image
    sharpen_kernel = cv2.GaussianBlur(
        denoised,
        (0, 0),
        3
    )

    sharpened = cv2.addWeighted(
        denoised,
        1.5,
        sharpen_kernel,
        -0.5,
        0
    )


    # Thresholding
    threshold_image = cv2.threshold(
        sharpened,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]


    # Save processed image
    processed_path = image_path.replace(
        "uploads",
        "processed"
    )

    cv2.imwrite(
        processed_path,
        threshold_image
    )


    return processed_path