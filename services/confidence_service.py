# -----------------------------------------------------
# Generate confidence score
# -----------------------------------------------------
def generate_confidence(data):

    confidence = {}


    for key, value in data.items():

        # High confidence if value exists
        if value and value != "Not Found":

            confidence[key] = 90


        # Low confidence if missing
        else:

            confidence[key] = 40


    return confidence