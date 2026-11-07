# This creates the page for users to submit their academic confidence ratings.
# The collected data is appended to the provided data.csv file.

import os
import math
import pandas as pd
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Academic Confidence Survey",
    page_icon="📝",
)

# CSV FILE LOCATION
CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "data.csv")

# PAGE TITLE AND USER DIRECTIONS
st.title("Academic Confidence Survey 📝")
st.write(
    "How confident are you in each academic subject? "
    "Rate your confidence from 1 (not confident) to 10 (very confident)."
)

# DATA INPUT FORM
with st.form("survey_form"):

    category_input = st.text_input("Which academic subject?")

    value_input = st.text_input(
        "How confident are you in this subject? (1–10)"
    )

    submitted = st.form_submit_button("Submit Response")

    if submitted:

        if category_input.strip() == "" or value_input.strip() == "":
            st.error("Please fill out both fields.")

        else:
            try:
                numeric_value = float(value_input)

                if not math.isfinite(numeric_value):
                    st.error("Please enter a valid numerical rating.")

                elif numeric_value < 1 or numeric_value > 10:
                    st.error("Your confidence rating must be between 1 and 10.")

                else:
                    subject = category_input.strip().lower()

                    file_exists = (
                        os.path.exists(CSV_FILE)
                        and os.path.getsize(CSV_FILE) > 0
                    )

                    # Check whether the subject already has a response.
                    if file_exists:
                        existing_data = pd.read_csv(CSV_FILE)

                        existing_subjects = (
                            existing_data["Category"]
                            .astype(str)
                            .str.strip()
                            .str.casefold()
                        )

                    else:
                        existing_subjects = pd.Series(dtype=str)

                    if subject.casefold() in existing_subjects.values:
                        st.error(
                            "You have already submitted a rating "
                            "for this subject."
                        )

                    else:
                        new_row = pd.DataFrame({
                            "Category": [subject],
                            "Value": [numeric_value]
                        })

                        new_row.to_csv(
                            CSV_FILE,
                            mode="a",
                            header=not file_exists,
                            index=False
                        )

                        st.success("Your response has been submitted!")

                        st.write(f"Subject: {subject}")
                        st.write(f"Confidence rating: {numeric_value}")

            except ValueError:
                st.error("Please enter a valid numerical rating.")

# DISPLAY CURRENT CSV DATA
st.divider()
st.header("Current Survey Responses")

if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
    current_data = pd.read_csv(CSV_FILE)

    display_data = current_data.rename(columns={
        "Category": "Subject",
        "Value": "Confidence Rating (1–10)"
    })

    display_data["Subject"] = (
        display_data["Subject"].astype(str).str.strip().str.lower()
    )

    st.dataframe(display_data, use_container_width=True)

else:
    st.info("No survey responses have been collected yet.")
