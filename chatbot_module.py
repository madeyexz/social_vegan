import sqlite_module # to interact with database
import openai
import os # to access environment variables

# initialize connection to OpenAI (get API key at https://beta.openai.com/)

def chatbot_completion(prompt, model="gpt-3.5-turbo-1106", max_tokens=400, temperature=0.4, top_p=1, frequency_penalty=0, presence_penalty=0):
    """
    Perform a completion task using OpenAI's language models.
    :param prompt: The input text to complete.
    :param model: The model to use (e.g., "text-davinci-003").
    :param max_tokens: The maximum number of tokens to generate.
    :param temperature: Controls randomness. Higher is more random.
    :param top_p: Nucleus sampling. Lower means more focused; 1 is no limit.
    :param frequency_penalty: Discourages repetition.
    :param presence_penalty: Encourages new concepts.
    :return: The completed text.
    """
    try:   
        openai.api_key = os.environ["OPENAI_API_KEY"]
        response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful translation assistant."},
            {"role": "user", "content": "Translate 'hi' in to French"},
            {"role": "assistant", "content": "Bonjour"},
            {"role": "user", "content": f"{prompt}."},
        ],
        temperature=0,
    )
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Set your API key here

# Example usage
prompt = "Translate the following English text to French: 'Hello, how are you?'"
result = chatbot_completion(prompt)
print(result)