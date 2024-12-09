import pytest

from ai_assistant_metrics_evaluation.chatbot_evaluation_metrics import *

user_inputs = [
    "What if these shoes don't fit?",
    "Can I return a product after 30 days?",
    "How do I track my order?"
]

bot_responses = [
    "We offer a 30-day full refund at no extra cost.",
    "Returns are accepted up to 30 days only if unused.",
    "You can track your order via the tracking link in your email."
]

retrieval_contexts = [
    ["All customers are eligible for a 30-day full refund at no extra cost."],
    ["Returns are accepted up to 30 days only if unused."],
    ["Tracking links are sent via email once your order ships."]
]

expected_outputs = [
    "You are eligible for a 30 day full refund at no extra cost.",
    "Returns are valid within 30 days only.",
    "Track your order using the link sent via email."
]


# @pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_all_metrics():
    metric_name_value = "Correctness"
    g_eval_criteria_details = "Determine whether the actual output is factually correct based on the expected output."
    evaluate_all_metrics_deepeval(user_inputs, retrieval_contexts, bot_responses,
                                  expected_outputs, metric_name_value, g_eval_criteria_details)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_answer_relevancy():
    evaluate_answer_relevancy_deepeval(user_inputs, bot_responses)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_faithfulness():
    evaluate_faithfulness_deepeval(user_inputs, retrieval_contexts, bot_responses)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_hallucination():
    evaluate_hallucination_deepeval(user_inputs, retrieval_contexts, bot_responses)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_contextual_relevancy():
    evaluate_contextual_relevancy_deepeval(user_inputs, retrieval_contexts, bot_responses)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_contextual_recall():
    evaluate_contextual_recall_deepeval(user_inputs, retrieval_contexts, bot_responses, expected_outputs)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_contextual_precision():
    evaluate_contextual_precision_deepeval(user_inputs, retrieval_contexts, bot_responses, expected_outputs)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_bias():
    evaluate_bias_deepeval(user_inputs, bot_responses)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_toxicity():
    evaluate_toxicity_deepeval(user_inputs, bot_responses)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_ragas_contextual_precision_metrics():
    evaluate_ragas_contextual_precision_metrics_deepeval(user_inputs, retrieval_contexts, bot_responses,
                                                         expected_outputs)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_ragas_contextual_recall_metrics():
    evaluate_ragas_contextual_recall_metrics_deepeval(user_inputs, retrieval_contexts, bot_responses, expected_outputs)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_ragas_faithfulness_metrics():
    evaluate_ragas_faithfulness_metrics_deepeval(user_inputs, retrieval_contexts, bot_responses, expected_outputs)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_ragas_answer_relevancy_metrics():
    evaluate_ragas_answer_relevancy_metrics_deepeval(user_inputs, retrieval_contexts, bot_responses, expected_outputs)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_metrics_using_g_eval():
    metric_name_value = "Correctness"
    g_eval_criteria_details = "Determine whether the actual output is factually correct based on the expected output."

    evaluate_metrics_using_g_eval_deepeval(metric_name_value, g_eval_criteria_details, user_inputs, bot_responses,
                                           expected_outputs)


@pytest.mark.skip(reason="This test is skipped.")
def test_evaluate_summarization():
    assessment_questions = [
        "What if these shoes don't fit?",
        "What is the return policy?",
        "Do you offer free shipping?"
    ]
    evaluate_summarization_deepeval(user_inputs, assessment_questions, bot_responses)
