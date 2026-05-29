import streamlit as st
import os
from datetime import datetime
from services.pdf_service import convert_pdf_to_images
from services.preprocessing import preprocess_image
from services.text_extractor import extract_text
from services.gemini_service import extract_structured_data
from services.confidence_service import generate_confidence
from services.database_service import (
    save_document,
    get_all_documents
)

from utils.validators import validate_uploaded_file


# -----------------------------------------------------
# Streamlit page configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------------------------
# Create required folders automatically
# -----------------------------------------------------
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("database", exist_ok=True)


# -----------------------------------------------------
# Sidebar navigation
# -----------------------------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["Upload Document", "History"]
)


# =====================================================
# PAGE 1 → DOCUMENT UPLOAD
# =====================================================
if page == "Upload Document":

    st.title("📄 AI Document Intelligence System")

    st.caption(
        "Upload documents and extract structured information using OCR + AI"
    )


    # -------------------------------------------------
    # File uploader
    # -------------------------------------------------
    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["png", "jpg", "jpeg", "pdf"]
    )


    if uploaded_file:

        # ---------------------------------------------
        # Validate uploaded file
        # ---------------------------------------------
        validation_message = validate_uploaded_file(uploaded_file)

        if validation_message:

            st.error(validation_message)
            st.stop()


        # ---------------------------------------------
        # Save uploaded file locally
        # ---------------------------------------------
        upload_path = f"uploads/{uploaded_file.name}"

        with open(upload_path, "wb") as file:

            file.write(uploaded_file.getbuffer())


        st.success("File uploaded successfully")


        # ---------------------------------------------
        # Progress bar
        # ---------------------------------------------
        progress_bar = st.progress(0)


        # ---------------------------------------------
        # Main processing pipeline
        # ---------------------------------------------
        with st.spinner("Processing document..."):


            # -------------------------------------------------
            # Detect uploaded file type
            # -------------------------------------------------
            file_extension = uploaded_file.name.split(".")[-1].lower()

            raw_text = ""


            # -------------------------------------------------
            # Handle PDF files
            # -------------------------------------------------
            if file_extension == "pdf":

                st.info("Converting PDF into images")

                progress_bar.progress(15)

                image_paths = convert_pdf_to_images(upload_path)


                st.info("Running OCR on PDF pages")

                progress_bar.progress(40)

                for image_path in image_paths:

                    processed_path = preprocess_image(image_path)

                    page_text = extract_text(processed_path)

                    raw_text += page_text + "\n"


            # -------------------------------------------------
            # Handle image files
            # -------------------------------------------------
            else:

                st.info("Enhancing image quality")

                progress_bar.progress(25)

                processed_path = preprocess_image(upload_path)


                st.info("Extracting text from image")

                progress_bar.progress(50)

                raw_text = extract_text(processed_path)


            # -------------------------------------------------
            # Reduce token size
            # -------------------------------------------------
            raw_text = raw_text[:4000]


            # -------------------------------------------------
            # AI structured extraction
            # -------------------------------------------------
            st.info("Generating structured information")

            progress_bar.progress(75)

            try:

                structured_data = extract_structured_data(
                    raw_text
                )

            except Exception as error:

                st.error(
                    f"Extraction Failed: {str(error)}"
                )

                st.stop()

            structured_data["processed_at"] = (
                datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
                )
            )

            # -------------------------------------------------
            # Confidence scoring
            # -------------------------------------------------
            confidence_scores = generate_confidence(structured_data)
   
            # -------------------------------------------------
            # Save result into database
            # -------------------------------------------------
            save_document(
                uploaded_file.name,
                structured_data
            )

            progress_bar.progress(100)


        # ---------------------------------------------
        # Document type badge
        # ---------------------------------------------
        if "document_type" in structured_data:

            st.success(
                f"Detected Document Type: {structured_data['document_type'].upper()}"
            )


        # ---------------------------------------------
        # Display results
        # ---------------------------------------------
        st.subheader("📌 Extracted Information")

        col1, col2 = st.columns(2)


        # ---------------------------------------------
        # Left side → structured fields
        # ---------------------------------------------
        with col1:

            for key, value in structured_data.items():

                if key == "processed_at":
                    continue

                st.markdown(
                    f"### {key.replace('_', ' ').title()}"
                )

                st.write(value)

                score = confidence_scores.get(key, 0)

                st.progress(score / 100)

                st.caption(
                    f"Confidence Score: {score}%"
                )


            if "processed_at" in structured_data:

                st.info(
                    f"Processed At: {structured_data['processed_at']}"
                )


        # ---------------------------------------------
        # Right side → raw OCR text
        # ---------------------------------------------
        with col2:

            st.subheader("📝 Raw OCR Text")

            st.text_area(
                "OCR Output",
                raw_text,
                height=500
            )


        # ---------------------------------------------
        # JSON Preview
        # ---------------------------------------------
        st.subheader("📦 Structured JSON")

        if "raw_response" in structured_data:

            st.error("JSON Parsing Failed")

            st.text(
                structured_data["raw_response"]
            )

        else:

            st.json(structured_data)


# =====================================================
# PAGE 2 → HISTORY
# =====================================================
elif page == "History":

    st.title("📜 Previously Processed Documents")

    documents = get_all_documents()


    if not documents:

        st.warning("No processed documents found")


    else:

        for document in documents:

            with st.expander(
                f"📄 {document['filename']}"
            ):

                st.json(document["data"])