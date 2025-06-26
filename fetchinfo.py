from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize LLM
llm = ChatOpenAI(model="gpt-4.1", temperature=0.2)
output_parser = StrOutputParser()

# Prompt to ask for name creatively
question_template = """
You are a smart detective who is trying to know the person's name.
Until you find the name, keep asking friendly and creative questions like:
"How's your day going?", "What's up?", etc.
But smartly guide the conversation to get their name.
Do not use quizzes or riddles.
"""
prompt_template = ChatPromptTemplate.from_template(template=question_template)

username = None
email = None
password = None


    
def check_username_in_message(user_msg):
    checkusername_template = """Check for a user name in the following message: "{input}". If there is a name, just say 'True', otherwise say 'False'."""
    checkusername_prompt = ChatPromptTemplate.from_template(checkusername_template)
    username_chain = checkusername_prompt | llm | output_parser
    username_check_response = username_chain.invoke({"input": user_msg})
    print(username_check_response)
    return username_check_response.strip().lower() == 'true'


def ask_question(user_msg):
    global username  # Access the global username variable

    if check_username_in_message(user_msg):
        # Extract the username from the user message (you may want a better extraction logic)
        extract_username = """ This message fromuser contains the user's name: "{input}". What is the user name? Just give me the user name as response nothing else """
        extract_username_prompt = ChatPromptTemplate.from_template(extract_username)
        extract_username_chain = extract_username_prompt | llm | output_parser
        extract_username_response = extract_username_chain.invoke({"input": user_msg})
        username = extract_username_response
        return f"Username received: {username}. Greetings, {username}!"
    
    # If username is not found, generate a new creative question
    formatted_prompt = prompt_template.format()  # No need to pass a string
    response_chain = prompt_template | llm | output_parser
    response = response_chain.invoke({})
    return response


def check_email(email_msg):
    template = """Check for an email in the following message: "{input}". If there is an email, just say 'True', otherwise say 'False'."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": email_msg})
    return response.strip().lower() == 'true'

def extract_email(email_msg):
    template = """This message from user contains the user's email: "{input}". What is the user email? Just give me the user email as response, nothing else."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | output_parser
    return chain.invoke({"input": email_msg}).strip()

def ask_for_email(email_msg):
    global email
    if check_email(email_msg):
        email = extract_email(email_msg)
        return f"Email received: {email}. Thank you!"
    else:
        return "No email found. Please share your email."

def check_password(password_msg):
    template = """Check for a password in the following message: "{input}". If there is a password, just say 'True', otherwise say 'False'."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": password_msg})
    return response.strip().lower() == 'true'


def extract_password(password_msg):
    template = """This message from user contains the user's password: "{input}". What is the password? Just give me the password as response, nothing else."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | output_parser
    return chain.invoke({"input": password_msg}).strip()


def ask_for_password(password_msg):
    global password
    if check_password(password_msg):
        password = extract_password(password_msg)
        return f"Password received: {password}. Thank you!"
    else:
        return "No password found. Please provide your password."


while username is None:
    user_msg = input("Enter a name: ")
    print(check_username_in_message(user_msg))

while email is None:
    email_msg = input("Enter your email: ")
    print(ask_for_email(email_msg))

while password is None:
    password_msg = input("Enter your password: ")
    print(ask_for_password(password_msg))

print(f" Name: {username}")
print(f"Email: {email}")
print(f" Password: {password}")
