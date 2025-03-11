
import re

def sanitize_model_output(response):
    response = re.sub(r"<think>.*</think>", r'', response, flags=re.DOTALL)
    response = re.sub(r"<\|begin_of_thought\|>.*<\|end_of_thought\|>", r'', response, flags=re.DOTALL)
    response = re.sub(r"<\|.*\|>", r'', response)
    return response.strip()

def is_answer_correct(checker, question, expected_answer, provided_answer):
    # checker_prompt = f'''
    # Evaluate if the model provided the expected answer for the question.
    # If the final answer is as expected, do not provide any explanation, reply with just one word: 'Yes'.
    # If the final answer is not as expected, reply with 'No' and explanation (what was the expected answer, what was the model's answer, how these answers differ).
    # Ignore response length, text formatting and any additional information, focus only on final answer.
    #
    # # The question:
    # {question}
    #
    # # Expected answer:
    # {expected_answer}
    #
    # # Model output:
    # {provided_answer}
    # '''.strip()

    checker_prompt = f'''
# Document:
{question}

Correct answer:
{provided_answer}

# Claim: 
Correct answer is {expected_answer}
'''.strip()

    evaluation = checker.chat(checker_prompt)

    res = 'Yes' == evaluation.strip()
    if not res:
        print(f'[FAIL]\n  # {question}\n  # Expected answer: {expected_answer}\n  # Provided answer: {provided_answer}\n  # Evaluation: {evaluation}\n\n')

    return res

