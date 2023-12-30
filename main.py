import json
from difflib import get_close_matches
import streamlit as st
import pandas as pd


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(usr_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(usr_question,
                                      questions,
                                      n=1,
                                      cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    if q in knowledge_base['questions']:
        if q['questions'] == question:
            return q['answers']


def chat_bot():
    st.title("Curious Chat Bot")

    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    # Initialize conversation history as a DataFrame
    conversation_df = pd.DataFrame(columns=['User', 'Bot'])

    while True:
        user_input: str = st.text_input("You:")

        if user_input.lower() == 'quit':
            break

        if st.button("Ask"):

            conversation_df = pd.concat([conversation_df, pd.DataFrame({'User': [user_input], 'Bot': ['']})])

            best_match: str = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])

            if best_match:
                answer: str = get_answer_for_question(best_match, knowledge_base)
                st.text(f"Bot: {answer}")

                conversation_df = pd.concat([conversation_df, pd.DataFrame({'User': [''], 'Bot': [answer]})])

            else:
                st.text("Bot: I don't know the answer, please can you teach me?")
                new_answer: str = st.text_input('Type the answer or "skip" to skip:')

                if new_answer.lower() != 'skip':
                    knowledge_base['questions'].append({'question': user_input, 'answer': new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    st.text("Bot: Thank you! I learnt something new.")

                    conversation_df = pd.concat(
                        [conversation_df, pd.DataFrame({'User': [''], 'Bot': ["Thank you! I learnt something new."]})])

    # Display the full conversation history
    st.text("Full Conversation History:")
    st.table(conversation_df.reset_index(drop=True))


if __name__ == '__main__':
    chat_bot()
