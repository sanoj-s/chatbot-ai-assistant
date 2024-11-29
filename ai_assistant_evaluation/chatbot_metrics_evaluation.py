import pandas as pd
import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_correctness, answer_similarity, context_precision, answer_relevancy, \
    context_recall, context_entity_recall
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# OPENAI_API_KEY should be the same as the key in the OpenAI account and used in the Bot.

excel_file = 'questions_ground_truth_data.xlsx'
df = pd.read_excel(excel_file)

# questions and ground_truth can be fetched from the Test data Excel.
# answer is the actual Bot response can be get from the API response.
# contexts can be fetched from the DB using the API.

data_samples = {
    'question': df['questions'].tolist(),
    'answer': ['Rise of Germany and decline of the Ottoman Empire which disturbed the long-standing balance of power '
               'in Europe', 'Bi-est Estradiol (E2) Estradiol'
                                                                               'Valerate (E2V) Estriol (E3) Estrone ('
                                                                               'E1) Methyltestosterone'
                                                                               'Progesterone Testosterone (T1) Tri-est'],
    'contexts': [
        [
            'The causes of World War I included the rise of Germany and decline of the Ottoman Empire, '
            'which disturbed the long-standing balance of power in Europe, as well as economic competition between '
            'nations triggered by industrialisation and imperialism. Growing tensions between the great powers and in '
            'the Balkans reached a breaking point on 28 June 1914, when a Bosnian Serb named Gavrilo Princip '
            'assassinated Archduke Franz Ferdinand, heir to the Austro-Hungarian throne.'
        ],
        [
            'Not Applicable'
        ]
    ],
    'ground_truth': df['ground_truth'].tolist()
}

dataset = Dataset.from_dict(data_samples)
score = evaluate(dataset,
                 metrics=[context_precision, context_recall, context_entity_recall, faithfulness, answer_relevancy,
                          answer_correctness, answer_similarity])
df = score.to_pandas()
df.to_excel(os.path.join(os.path.dirname(__file__), 'test_llm_apps_score.xlsx'), index=False)
