from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4.1", temperature=0.2)

output_parser = StrOutputParser()

question_tempate = """ 
You are a smart detective who is trying to know the person name and until you find the person name you keep asking the person in different creative way to figure out the person's details.
Just be have normal human converstaion like "hi how was your day","how is everything", something similar in that ask the person name smartly. Dont play quiz. 
"""


username = None
email = None
password=None

checkusername_template = """
Does the following message from the user contain their name? Reply with "true" or "false".
Message: "{input}"
"""
checkemail_template = """
Dose the following message from the user contain their email? Reply with "true" or "false".
Message : "{input}"
"""
checkpassword_template = """
Dose the following message from the user contain their password? Reply with "true" or "false".
Message : "{input}"
"""
checkusername_prompt = ChatPromptTemplate.from_template(checkusername_template)
checkemail_prompt = ChatPromptTemplate.from_template(checkemail_template)
checkpassword_prompt = ChatPromptTemplate.from_template(checkpassword_template)

def check_username(user_msg):
    prompt_messages = checkusername_prompt.format_messages(input=user_msg)
    message = llm.invoke(prompt_messages)
    result = output_parser.invoke(message)
    return result.strip() == "true"  

def ask_question(user_msg):
    global username
    
    if check_username(user_msg):
        extract_username = """ This message fromuser contains the user's name: "{input}". What is the user name? Just give me the user name as response nothing else """
        extract_username_prompt = ChatPromptTemplate.from_template(extract_username)
        message = extract_username_prompt.invoke({"input": user_msg})
        result = llm.invoke(message)
        username = output_parser.invoke(result)
        return f"Username received: {username}. Greetings, {username}!"
    else:
        return "Username not found. Please tell me your name."
    
def check_email(email_msg):
    checkemail_template = """Check if the following is a valid email address: "{input}". If yes, say 'True'. Otherwise, say 'False'."""
    checkemail_prompt = ChatPromptTemplate.from_template(checkemail_template)
    prompt_email_message = checkemail_prompt.invoke({"input": email_msg})
    response = llm.invoke(prompt_email_message)
    result = output_parser.invoke(response)
    return result.strip().lower() == 'true'

def ask_email(email_msg):
    
    global email

    if check_email(email_msg):
        extract_email = """This message contains the user's email: "{email_input}". What is the email? Just return the email address, nothing else."""
        extract_email_prompt = ChatPromptTemplate.from_template(extract_email)
        message = extract_email_prompt.invoke({"email_input": email_msg})
        result = llm.invoke(message)
        email = output_parser.invoke(result)
        return f"Email received: {email}. Thank you!"
    else:
        return "Email not found. Please provide your email."

def check_password(pass_msg):
    checkpassword_template = """Check if the following is valid password : "{input}".If yes,say 'True'. Otherwise ,say 'false'"""
    checkpassword_prompt=ChatPromptTemplate.from_template(checkpassword_template)
    check_password_prompt =checkpassword_prompt.invoke({"input":pass_msg})
    response = llm.invoke(check_password_prompt)
    result = output_parser.invoke(response)
    return result.strip().lower() == 'true'

def ask_password(pass_msg):
    global password
    
    if check_password(pass_msg):
        extract_password="""This message is contain the user's password :"{input}". What is the password? Just return the password,nothing else."""
        extract_password_prompt = ChatPromptTemplate.from_template(extract_password)
        message= extract_password_prompt.invoke({"pass_input":pass_msg})
        response = llm.invoke(message)
        result=output_parser.invoke(response)
        password = result.strip()
        return f"Password received: {password}."
    else:
        return f"Password is not found. Give me correct passwords"
    
while username is None:
    user_msg = input("Enter a username : ")
    ai_msg=ask_question(user_msg)
    print(f"AI : ",ai_msg)
    
while email is None:
    email_msg = input("Enter an Email : ")
    aiemail_msg=ask_email(email_msg)
    print(f"AI : ",aiemail_msg)

while password is None:
    pass_msg = input("Enter the password : ")
    aipass_msg = ask_password(pass_msg)
    print(f"AI : ",aipass_msg)
    
print(f"Name: {username}")
print(f"Email: {email}")
print(f"Password:{password}")