from app import app
from app.models.question_paper import ObjectiveQuestion, Question, QuestionPaper
from app.models.question_paper_repository import QuestionPaperRepo


def collect_question_without_answer():
    question_text = input("Enter the question text for the question: ")
    return Question(question_text)


def collect_objective_question():
    question_text = input("Enter the question text for the objective question: ")
    multiple_choice = input("Is this a multiple-choice question (yes/no)? ").strip().lower() == 'yes'
    options = input("Enter the options separated by commas: ")
    return ObjectiveQuestion(question_text, options, multiple_choice)

def main():
    collected_questions = []
    questions = []

    while True:
        question_type = input("Enter question type (sub/obj) or 'quit' to exit: ").strip().lower()
        if question_type == 'quit':
            break
        elif question_type == 'subj':
            question = collect_question_without_answer()
            collected_questions.append(question)
        elif question_type == 'obj':
            question = collect_objective_question()
            collected_questions.append(question)
        else:
            print("Invalid input. Please enter 'sub' for subjective' or 'obj' for objective.")

    # Display all collected questions
    print("\nCollected Questions:")
    for i, question in enumerate(collected_questions, 1):
        ques_to_store = QuestionPaper()
        ques_to_store.question = question.question_text
        print(f"\nQuestion {i}: {question.question_text}")
        if isinstance(question, ObjectiveQuestion):
            ques_to_store.options = question.options
            ques_to_store.is_multi_choice = question.multi_choice
            print(question.options)
        questions.append(ques_to_store)

    if questions:
        with app.app_context():
            QuestionPaperRepo.bulk_create_questions(questions)


if __name__ == "__main__":
    main()

# export PYTHONPATH=$(pwd)