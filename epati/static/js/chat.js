let loc = window.location
let wsStart = 'ws://'

if (location.protocol == 'https') {
    wsStart = 'wss://'
}

let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e) {
    console.log('open', e)
    $('.msg_send_btn').on('click', function(e) {
        e.preventDefault()
        let message = document.getElementById('write_msg').value
        let sent_by = $('#logged-user-id').val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': sent_by,
            'send_to': send_to,
            'thread_id': thread_id,
        }
        data = JSON.stringify(data)
        socket.send(data)
    })
    $('#write_msg').on('keypress', function(e) {
        if (e.key === "Enter" ) {
            $('.msg_send_btn').click()
        }
    })
}

socket.onmessage = async function(e) {
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e) {
    console.log('error', e)
}

socket.onclose = async function(e) {
    console.log('close', e)
}

function newMessage(message, sent_by_id, thread_id) {
    if ($.trim(message) == '' ) {
        return false;
    }

    let chat_id = 'chat_' + thread_id
    var newDate = new Date();

    let message_element
    if (sent_by_id == $('#logged-user-id').val()) {
        message_element = `
            <div class="outgoing_msg">
                <div class="sent_msg">
                    <p> ${message} </p>
                <span class="time_date">${newDate.toLocaleString('en-gb',{day:'2-digit', month:'short'})}     |    ${newDate.toLocaleString('en-gb', {hour:'2-digit', minute:'2-digit'})}</span> </div>
            </div>
        `
    }
    else {
        message_element = `
        <div class="incoming_msg">
            <div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
            <div class="received_msg">
              <div class="received_withd_msg">
                <p> ${message} </p>
                <span class="time_date">${newDate.toLocaleString('en-gb',{day:'2-digit', month:'short'})}     |    ${newDate.toLocaleString('en-gb', {hour:'2-digit', minute:'2-digit'})}</span></div>
            </div>
          </div>
    `
    }

    let message_body = $('.mydiv[chat-id="' + chat_id +'"] .msg_history')
    message_body.append($(message_element))
    $('.mydiv[chat-id="' + chat_id +'"] .msg_history').scrollTop(function() { return this.scrollHeight; });
    document.getElementById('write_msg').value = null

    $('.last-message').load(' .last_message', function(){$(this).children().unwrap()})
}


function changeThread(element) {
    $('.chat_list.active_chat').removeClass('active_chat')
    element.classList.add('active_chat')

    // message wrappers
    let chat_id = element.getAttribute('chat-id')
    $('.mydiv.is_active').removeClass('is_active')
    $('.mydiv[chat-id="' + chat_id +'"]').addClass('is_active')
    $('.mydiv[chat-id="' + chat_id +'"] .msg_history').scrollTop(function() { return this.scrollHeight; });
}

function get_active_other_user_id() {
    let other_user_id = $('.mydiv.is_active').attr("other-user-id")
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id() {
    let chat_id = $('.mydiv.is_active').attr("chat-id")
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}

$( document ).ready(function() {
    $('.mydiv .msg_history').scrollTop(function() { return this.scrollHeight; });
});