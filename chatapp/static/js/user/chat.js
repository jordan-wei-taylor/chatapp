import { authenticate, classify, fetchPreamble, fetchCue, getOption, amtWarmUp, submitRecord, updateUserModule } from "/static/js/events.js"
import { getCookies } from "/static/js/utils.js"

const cookies  = getCookies()
const cookie   = cookies.cookie
const module   = document.location.href.match('(?<=-)[0-9]+')[0]
const Message  = document.getElementById('userInput')
const chatMessages = document.getElementById('chatMessages')
const option   = await getOption(cookie)
var   maxCount = 1
var   mode     = 'classify'
var   record   = {cookie: cookie, module: module, count: 1}
var   cue      = {}
var   preamble = await fetchPreamble(module, cookie)
var   flag     = true

if (option === 'feedback') { maxCount = 3 }


console.log(maxCount)

document.getElementsByClassName('chat-header')[0].innerHTML = cookies.module

function showTypingIndicator() {
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typing-indicator';
    typingIndicator.classList.add('message', 'bot');

    const ellipsis = document.createElement('div');
    ellipsis.classList.add('ellipsis');  // Apply the ellipsis class for animation

    typingIndicator.appendChild(ellipsis);
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        chatMessages.removeChild(typingIndicator);
    }
}

async function addMessage(content, role) {
    const messageElement = document.createElement('div')
    const messageContent = document.createElement('div')
    if (role === 'bot') {
        showTypingIndicator()
        return new Promise (function (resolve, reject) {
            setTimeout(resolve, 2000)
        })
        .then(() =>{
            removeTypingIndicator()
            messageElement.classList.add('message', role)
            messageContent.classList.add('message-content');
            messageContent.textContent = content;
            messageElement.appendChild(messageContent);
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
    } else {
        messageElement.classList.add('message', role)
        messageContent.classList.add('message-content');
        messageContent.textContent = content;
        messageElement.appendChild(messageContent);
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}


async function estherClassify(message) {
    const response = await classify({message: message, count: record.count, maxCount: maxCount})
    for (const [key, value] of Object.entries(response)) {
        if (key === 'mode') { mode = value }
        else { record[key] = value }
    }
    await addMessage(response.esther, 'bot')
}

async function estherValency(message) {
    if (( /^[12345]$/ ).test(message)) {
        record.user_valence = message
        record.cue_word = cue.cueWord
        record.cue_text = cue.cue
        submitRecord(record)
        await addMessage(record.esther_response, 'bot')
        mode = 'classify'
        await newCue()
    } else { await addMessage('Please can you enter an integer between 1 and 5.', 'bot') }
}

async function esther(message) {
    if (mode === 'classify') { await estherClassify(message) }
    else if (mode === 'valency') { await estherValency(message) }
}

async function newCue() {
    cue = await fetchCue(module, cookie)
    console.log(cue)
    if (cue.cue == 'N/A') {
        await addMessage('You have completed this module! Please go back to your dashboard area and proceed to the next module.')
        updateUserModule(cookie, module)
    } else {
        if (flag) {
            for (const element of preamble) { await addMessage(element, 'bot') }
            flag = false
        }
        await addMessage(cue.cue, 'bot')
    }
}

document.getElementById('send-button').addEventListener('click', async () => {
    if (Message.value.trim() !== "") {
        record.user = Message.value
        Message.value = ''
        addMessage(record.user, 'user')
        await esther(record.user)
        
    }
})

newCue()
amtWarmUp() 



