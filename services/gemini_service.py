from groq import Groq
from dotenv import load_dotenv
import os
import json
import re


# -----------------------------------------------------
# Load environment variables
# -----------------------------------------------------
load_dotenv()


# -----------------------------------------------------
# Initialize Groq client
# -----------------------------------------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------------------------------
# Clean and normalize OCR text
# before sending to LLM
# -----------------------------------------------------
def clean_ocr_text(raw_text):

    # Remove extra spaces
    cleaned = re.sub(
        r"\s+",
        " ",
        raw_text
    )

    # Remove unwanted symbols
    cleaned = re.sub(
        r"[^\w\s:/.-]",
        "",
        cleaned
    )

    return cleaned.strip()


# -----------------------------------------------------
# Mask Aadhaar number
# for privacy/security
# -----------------------------------------------------
def mask_aadhaar(aadhaar_number):

    if not aadhaar_number:

        return None


    # Remove spaces
    cleaned = aadhaar_number.replace(
        " ",
        ""
    )


    # Ensure valid length
    if len(cleaned) >= 12:

        return (
            "XXXX XXXX "
            + cleaned[-4:]
        )


    return aadhaar_number


# -----------------------------------------------------
# Extract structured information
# using Groq LLM
# -----------------------------------------------------
def extract_structured_data(raw_text):


    # ---------------------------------------------
    # Clean OCR text
    # ---------------------------------------------
    cleaned_text = clean_ocr_text(raw_text)


    # ---------------------------------------------
    # Reduce token size
    # Improves speed and avoids huge prompts
    # ---------------------------------------------
    cleaned_text = cleaned_text[:4000]


    # ---------------------------------------------
    # Prompt for AI extraction
    # ---------------------------------------------
    prompt = f"""
    You are an intelligent OCR document extraction AI.

    Analyze the OCR text carefully.

    Extract all useful structured information.

    Return ONLY valid JSON.

    Rules:
    - Detect document type automatically
    - If field missing → return null
    - Extract Aadhaar details if present
    - Keep response compact

    Possible fields:
    - document_type
    - name
    - father_name
    - dob
    - aadhaar_number
    - email
    - phone
    - degree
    - institution
    - year
    - cgpa
    - company
    - role
    - stipend
    - skills

    Example:

    {{
        "document_type": "aadhaar",
        "name": "John Doe",
        "dob": "01/01/2000",
        "aadhaar_number": "1234 5678 9012"
    }}

    OCR TEXT:
    {cleaned_text}
    """


    # ---------------------------------------------
    # Generate AI response
    # ---------------------------------------------
    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    # ---------------------------------------------
    # Extract generated content
    # ---------------------------------------------
    content = response.choices[0].message.content


    # ---------------------------------------------
    # Remove markdown wrappers
    # ---------------------------------------------
    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )


    # ---------------------------------------------
    # Print response for debugging
    # ---------------------------------------------
    print("\n========== AI RESPONSE ==========\n")

    print("\n=================================\n")


    # ---------------------------------------------
    # Convert response into JSON
    # ---------------------------------------------
    try:

        parsed_json = json.loads(content)


        # -----------------------------------------
        # Mask Aadhaar number
        # -----------------------------------------
        if parsed_json.get("aadhaar_number"):

            parsed_json["aadhaar_number"] = (
                mask_aadhaar(
                    parsed_json["aadhaar_number"]
                )
            )


        return parsed_json


    # ---------------------------------------------
    # JSON parsing failure fallback
    # ---------------------------------------------
    except Exception as error:

        return {

            "raw_response": content,

            "error": str(error)
        }