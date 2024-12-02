import os
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_correctness,
    answer_similarity,
    context_precision,
    answer_relevancy,
    context_recall,
    context_entity_recall,
)
import streamlit as st

# Streamlit App Title
st.title("Metrics Evaluation for LLM Responses")

# File Uploader
uploaded_file = st.file_uploader(
    "Upload the Excel file containing questions, answers, contexts, and ground truth data",
    type=["xlsx"],
)

if uploaded_file:
    # Read uploaded Excel file
    df = pd.read_excel(uploaded_file)
    st.write("Preview of Uploaded Data:")
    st.dataframe(df)

    # Ensure required columns are present
    required_columns = ["questions", "ground_truth"]
    if all(col in df.columns for col in required_columns):
        # Collect data from the file
        data_samples = {
            "question": df["questions"].tolist(),
            "answer": df.get("answer", ["Not Available"] * len(df)).tolist(),
            "contexts": df.get("contexts", [["Not Available"]] * len(df)).tolist(),
            "ground_truth": df["ground_truth"].tolist(),
        }

        # Prepare the Dataset for evaluation
        dataset = Dataset.from_dict(data_samples)

        # Metrics evaluation
        if st.button("Evaluate Metrics"):
            st.info("Calculating metrics, please wait...")
            score = evaluate(
                dataset,
                metrics=[
                    context_precision,
                    context_recall,
                    context_entity_recall,
                    faithfulness,
                    answer_relevancy,
                    answer_correctness,
                    answer_similarity,
                ],
            )
            # Convert scores to Pandas DataFrame
            metrics_df = score.to_pandas()

            # Show results
            st.write("Evaluation Metrics:")
            st.dataframe(metrics_df)

            # Save to Excel and provide download link
            output_file = "evaluation_metrics.xlsx"
            metrics_df.to_excel(output_file, index=False)

            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download Metrics Results as Excel",
                    data=file,
                    file_name="evaluation_metrics.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
    else:
        st.error(f"The uploaded file must contain these columns: {required_columns}.")
else:
    st.warning("Please upload an Excel file to proceed.")
