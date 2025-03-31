import openai
import requests
import string
import math
import json
import time
import random
import os

# parameters for GPT API
GPT_MODEL      = "gpt-3.5-turbo"
THRESHOLD      = 0.6

# credentials for APIs
SECRETS = {
    "amt": {
        "url": "https://api-inference.huggingface.co/models/exp-psych-lab/AMT-pipeline",
        "headers": {
            "Authorization": os.environ['amt_api_key']
        }
    },
    "gpt": {
        "api_key": os.environ['gpt_api_key']
    }
}

# predefined responses
with open('responses.json') as file:
    RESPONSES = json.load(file)

def gpt(query):
    # query -> probability(valid memory within query), memory estimate
    client   = openai.OpenAI(**SECRETS['gpt'])

    def gen_messages(system, assistant, user = query):
        return [{"role" : role, "content" : locals()[role]} for role in ['system', 'assistant', 'user']]
    
    kwargs       = dict(model = GPT_MODEL, temperature = 0.)

    messages_yn  = gen_messages("answer with yes / no",
                                "does the user talk about a memory in the following text?")

    yn           = client.chat.completions.create(messages = messages_yn,
                                                  logprobs = True,
                                                  **kwargs).choices[0].logprobs.content[0]
    
    if 'n' in yn.token.lower():
        prob = 1 - math.exp(yn.logprob)
    else:
        prob = math.exp(yn.logprob)

    messages_mem = gen_messages("answer with up to two words",
                                "what is the main user memory from the following text?")

    mem          = client.chat.completions.create(messages = messages_mem,
                                                  **kwargs).choices[0].message.content
    return prob, mem.lower().translate(str.maketrans('', '', string.punctuation))

def amt(query):
    # query -> { label : p(label | query) } (probability decreasing order)
    for _ in range(5):
        ret = {}
        try:
            response = requests.post(**SECRETS['amt'], json = query)
            response.raise_for_status()
            for item in response.json()[0]:
                ret[item['label']] = item['score']
            return ret
        except Exception as e:
            print(f'Error : {e}')
            time.sleep(2)
    return {}

def sample(label):
    # sample a predefined response based on label
    return random.choice(RESPONSES[label])