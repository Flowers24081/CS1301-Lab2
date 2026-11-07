import os
import pandas as pd
import streamlit as st
import json
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Academic Confidence Visualizations",
    page_icon="📈",
)

# PAGE TITLE
st.title("Academic Confidence Visualizations 📈")
st.write(
    "Explore academic confidence ratings using data from "
    "the provided JSON and CSV files."
)


# ==========================================
# PART 1: GRAPHS FROM data.json
# ==========================================

json_path = os.path.join(
    os.path.dirname(__file__), "..", "data.json"
)

with open(json_path, "r") as file:
    data = json.load(file)

labels = [point["label"] for point in data["data_points"]]
values = [point["value"] for point in data["data_points"]]

st.subheader("Static JSON Visualization")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(labels, values)

ax.set_title(data["chart_title"])
ax.set_xlabel("Courses")
ax.set_ylabel("Course Rating (1–100)")
ax.set_ylim(0, 100)

st.pyplot(fig)
plt.close(fig)


st.subheader("Dynamic JSON Visualization")

if "selected_item" not in st.session_state:
    st.session_state.selected_item = labels[0]

selected_item = st.selectbox(
    "Choose an item:",
    labels,
    key="selected_item"
)

selected_index = labels.index(selected_item)
selected_value = values[selected_index]

st.write(f"Value for {selected_item}: {selected_value}")

dynamic_json_fig, dynamic_json_ax = plt.subplots(figsize=(8, 5))

dynamic_json_ax.pie(
    [selected_value, sum(values) - selected_value],
    labels=[selected_item, "Other items"],
    autopct="%1.1f%%",
    startangle=90
)

dynamic_json_ax.set_title(
    f"{selected_item} Compared with Other Items"
)

st.pyplot(dynamic_json_fig)
plt.close(dynamic_json_fig)


# ==========================================
# PART 2: GRAPHS FROM data.csv
# ==========================================

st.divider()
st.header("Part 2: Academic Confidence Results")

csv_path = os.path.join(
    os.path.dirname(__file__), "..", "data.csv"
)

if not os.path.exists(csv_path):
    st.error("data.csv was not found in the main Lab02 folder.")

else:
    csv_data = pd.read_csv(csv_path)

    # Prepare the CSV data.
    csv_data["Category"] = (
        csv_data["Category"].astype(str).str.strip().str.lower()
    )

    csv_data["Value"] = pd.to_numeric(
        csv_data["Value"], errors="coerce"
    )

    csv_data = csv_data.dropna(subset=["Value"])

    # Keep only valid confidence ratings from 1 to 10.
    csv_data = csv_data[
        (csv_data["Value"] >= 1) &
        (csv_data["Value"] <= 10) &
        (csv_data["Category"] != "")
    ]

    if csv_data.empty:
        st.info("No valid academic confidence ratings are available.")

    else:

        # ======================================
        # STATIC VISUALIZATION: LOLLIPOP CHART
        # ======================================

        st.subheader("Academic Confidence by Subject")

        static_fig, static_ax = plt.subplots(figsize=(10, 5))

        positions = range(len(csv_data))

        static_ax.hlines(
            y=positions,
            xmin=0,
            xmax=csv_data["Value"],
            color="skyblue",
            linewidth=4
        )

        static_ax.scatter(
            csv_data["Value"],
            positions,
            s=150,
            color="royalblue",
            edgecolors="white",
            linewidths=1.5,
            zorder=3
        )

        static_ax.set_yticks(list(positions))
        static_ax.set_yticklabels(csv_data["Category"])

        static_ax.set_title("Student Confidence Ratings by Subject")
        static_ax.set_xlabel("Confidence Rating (1–10)")
        static_ax.set_ylabel("Academic Subject")
        static_ax.set_xlim(0, 10)

        static_ax.grid(
            axis="x",
            linestyle="--",
            alpha=0.4
        )

        static_fig.tight_layout()
        st.pyplot(static_fig)
        plt.close(static_fig)

        # ======================================
        # DYNAMIC VISUALIZATION: LINE CHART
        # ======================================

        st.subheader("Explore Confidence Ratings")

        categories = sorted(csv_data["Category"].unique().tolist())

        if "selected_categories" not in st.session_state:
            st.session_state.selected_categories = categories.copy()

        # Remove selections that no longer exist in the CSV.
        st.session_state.selected_categories = [
            category
            for category in st.session_state.selected_categories
            if category in categories
        ]

        selected_categories = st.multiselect(
            "Choose subjects to display:",
            categories,
            key="selected_categories"
        )

        filtered_data = csv_data[
            csv_data["Category"].isin(selected_categories)
        ]

        if filtered_data.empty:
            st.warning("Select at least one subject to display.")

        else:
            dynamic_fig, dynamic_ax = plt.subplots(figsize=(10, 5))

            dynamic_ax.plot(
                filtered_data["Category"],
                filtered_data["Value"],
                marker="o",
                linestyle="-",
                color="darkorange",
                linewidth=2,
                markersize=8
            )

            dynamic_ax.set_title(
                "Confidence Ratings for Selected Subjects"
            )
            dynamic_ax.set_xlabel("Academic Subjects")
            dynamic_ax.set_ylabel("Confidence Rating (1–10)")
            dynamic_ax.set_ylim(0, 10)
            dynamic_ax.tick_params(axis="x", labelrotation=30)

            dynamic_ax.grid(
                axis="y",
                linestyle="--",
                alpha=0.4
            )

            dynamic_fig.tight_layout()
            st.pyplot(dynamic_fig)
            plt.close(dynamic_fig)

            # ======================================
            # EXTRA CREDIT: SUMMARY STATISTICS
            # ======================================

            st.subheader("Academic Confidence Statistics")

            mean_value = filtered_data["Value"].mean()
            median_value = filtered_data["Value"].median()

            if "previous_mean" not in st.session_state:
                st.session_state.previous_mean = None

            if "previous_median" not in st.session_state:
                st.session_state.previous_median = None

            previous_mean = st.session_state.previous_mean
            previous_median = st.session_state.previous_median

            mean_delta = None
            median_delta = None

            if previous_mean is not None:
                mean_delta = mean_value - previous_mean

            if previous_median is not None:
                median_delta = median_value - previous_median

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Mean Confidence",
                    f"{mean_value:.2f}",
                    delta=(
                        f"{mean_delta:+.2f}"
                        if mean_delta is not None else None
                    )
                )

            with col2:
                st.metric(
                    "Median Confidence",
                    f"{median_value:.2f}",
                    delta=(
                        f"{median_delta:+.2f}"
                        if median_delta is not None else None
                    )
                )

            st.caption(
                f"Displaying {len(filtered_data)} responses "
                f"from {len(selected_categories)} selected subjects."
            )

            # Save current statistics for the next interaction.
            st.session_state.previous_mean = mean_value
            st.session_state.previous_median = median_value
