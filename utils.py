def parse_response(text):
    sections = {"plan": "", "quiz": "", "explanation": ""}

    if "### Learning Plan" in text:
        sections["plan"] = text.split("### Learning Plan")[1].split("### Quiz")[0]

    if "### Quiz" in text:
        sections["quiz"] = text.split("### Quiz")[1].split("### Explanation")[0]

    if "### Explanation" in text:
        sections["explanation"] = text.split("### Explanation")[1]

    return sections