from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field


class UserInfo(BaseModel):
    """
    A Pydantic model that holds user information such as username, email, and password.
    Used for data validation and serialization in API requests or internal data handling.
    """
    
    username: str = Field(description="The unique name chosen by the user to identify themselves in the system.")
    email: str = Field(description="The user's email address used for communication and login purposes.")
    password: str = Field(description="The user's secret key used for authentication and account security.")
    
llm = ChatOpenAI(model="gpt-4.1",temperature=0.5)
llm = llm.with_structured_output(UserInfo)

username_input = input("Enter your username: ")
email_input = input("Enter your email: ")
password_input = input("Enter your password: ")


prompt = ChatPromptTemplate.from_messages([
    ('system',"You are an assistant that extracts user credentials."),
    ('user',"{input}")
]
)


user_input = f"My username is {username_input}, my email is {email_input}, and my password is {password_input}."
    

formatted_prompt = prompt.format_messages(input=user_input)
result = llm.invoke(formatted_prompt)


if not result.username:
    result.username = input("Username is missing. Please enter your username: ")

if not result.email:
    result.email = input("Email is missing. Please enter your email: ")

if not result.password:
    result.password = input("Password is missing. Please enter your password: ")


print("\nAll UserInfo:=")
print("Username:", result.username)
print("Email:", result.email)
print("Password:", result.password)

