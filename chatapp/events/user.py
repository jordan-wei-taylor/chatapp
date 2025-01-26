from chatapp.objects import socket

from chatapp import api, sql

@socket.on('client-signup')
def signup(data):
    email = data['email']
    dob   = data['dob']
    sex   = data['sex']
    response = sql.signup(email, dob, sex)
    socket.emit('server-signup', response)

@socket.on('client-update-user-module')
def update_user_module(data):
    cookie = data['cookie']
    module = data['module']
    print('client-update-user-module', cookie, module)
    sql.update_user_module(cookie, module)

@socket.on('client-fetch-modules-completed')
def fetch_modules_completed(cookie):
    number = sql.fetch_modules_completed(cookie)
    socket.emit('server-fetch-modules-completed', number)

@socket.on('client-fetch-cues')
def fetch_cues(data):
    module = data['module']
    cookie = data['cookie']
    cues   = sql.fetch_cues(cookie, module)
    socket.emit('server-fetch-cues', cues)

@socket.on('client-fetch-cue')
def fetch_cue(data):
    module = data['module']
    cookie = data['cookie']
    cue_word, cue = sql.fetch_cue(cookie, module)
    socket.emit('server-fetch-cue', dict(cueWord = cue_word, cue = cue))

@socket.on('client-fetch-preamble')
def fetch_preamble(data):
    module = data['module']
    cookie = data['cookie']
    preamble = sql.fetch_preamble(cookie, module)
    socket.emit('server-fetch-preamble', preamble)

@socket.on('client-classify')
def classify(data):
    message   = data['message']
    count     = int(data['count'])
    max_count = int(data['maxCount'])
    prob, memory = api.gpt(message)
    if any([memory is None, memory == "memory", prob < 0.3]):
        print('could not identify memory via gpt!')
        memory = 'N/A'

    classification = api.amt(message)

    while len(classification) == 0:
        classification = api.amt(message)
        
    most_prob      = max(classification.values())
    label          = list(classification)[0]
    conditions     = any([most_prob < 0.5, prob < 0.3]) and (count < max_count)

    if conditions:
        count  += 1
        payload = dict(esther = api.sample('generic-na') if memory == 'N/A' else api.sample('generic').format(memory),
                       count  = count) 
    else:
        label   = list(classification)[0]
        payload = dict(mode            = 'valency',
                       user_text       = message,
                       esther_response = api.sample(label).format(memory),
                       gpt_prob        = prob,
                       gpt_memory      = memory,
                       amt_label       = label,
                       esther          = 'On a scale of 1 (very negative) to 5 (very positive), what sort of emotions does talking about this make you feel?',
                       count           = 1,
                       user_flag       = 'N/A' if ((count == 1) and (label == 'specific')) else 'Target' if ((count <= max_count) and (label == 'specific')) else 'Non-Target'
        )
        for label, prob in classification.items():
            payload[f'amt_{label}'] = prob

    socket.emit('server-classify', payload)

@socket.on('client-add-record')
def add_record(data):
    sql.add_record(data)

@socket.on('client-amt-warm-up')
def amt_warm_up():
    api.amt('Hello World!')

@socket.on('client-submit-record')
def submit_record(data):
    args = [data[key] for key in ['cookie', 'module', 'cue_word', 'cue_text', 'user_text', 'user_valence', 'gpt_prob', 'gpt_memory', 'amt_label', 'amt_associate',
                                  'amt_categoric', 'amt_extended', 'amt_omission', 'amt_specific', 'esther_response', 'user_flag']]
    sql.submit_record(*args)

@socket.on('client-get-option')
def get_option(cookie):
    socket.emit('server-get-option', sql.get_option(cookie))