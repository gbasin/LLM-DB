import openai

class BadMessagesFormat(Exception):
    pass

def generate_chat_completion(messages, 
                             system_message = "You are a helpful assistant.",
                             examples = [], 
                             model = "gpt-3.5-turbo", 
                             temperature = 0,
                             max_tokens = 256):
    
    
    chat_messages = [
        {"role": "system", "content": system_message}
    ]    
        
    for example in examples:
        chat_messages.append({"role": "system", "name": example['name'], "content": example['content']})
     
    
    #user_message = {"role": "user", "content": user_msgs[i]}
    #messages.append(user_message)
     
    if (isinstance(messages, str)):
        chat_messages.extend([{"role": "user", "content": messages}])
    elif (isinstance(messages, list)):
        chat_messages.extend(messages)
    else:
        raise BadMessagesFormat('`messages` object must be a list of object literals like `"{`"role`": `"user`", `"content`": message`" or a string');

    response = openai.ChatCompletion.create(
        model=model,
        messages=chat_messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    #response_txt = response['choices'][0]['message']['content'];
        
    #if response.get('gptcache'):
    #    print('cached: true')
    
    return response