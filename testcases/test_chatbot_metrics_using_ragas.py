import pytest

from ai_assistant_metrics_evaluation.chatbot_evaluation_metrics import *

data_samples = {
    'question': [
        "What if these shoes don't fit?",
        "Can I return a product after 30 days?",
        "How do I track my order?"
    ],
    'answer': [
        "We offer a 30-day full refund at no extra cost.",
        "Returns are accepted up to 30 days only if unused.",
        "You can track your order via the tracking link in your email."
    ],
    'contexts': [
        ["All customers are eligible for a 30-day full refund at no extra cost."],
        ["Returns are accepted up to 30 days only if unused."],
        ["Tracking links are sent via email once your order ships."]
    ],
    'ground_truth': [
        "You are eligible for a 30 day full refund at no extra cost.",
        "Returns are valid within 30 days only.",
        "Track your order using the link sent via email."
    ]
}


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_all_metrics():
    evaluate_all_metrics_ragas(data_samples)


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_context_precision_metrics():
    evaluate_context_precision_ragas(data_samples)


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_context_recall_metrics():
    evaluate_context_recall_ragas(data_samples)


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_context_entity_recall_metrics():
    evaluate_context_entity_recall_ragas(data_samples)


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_faithfulness_metrics():
    evaluate_faithfulness_ragas(data_samples)


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_answer_relevancy_metrics():
    evaluate_answer_relevancy_ragas(data_samples)


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_answer_correctness_metrics():
    evaluate_answer_correctness_ragas(data_samples)


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_answer_similarity_metrics():
    evaluate_answer_similarity_ragas(data_samples)
