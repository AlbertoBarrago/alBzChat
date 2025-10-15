import json
from datetime import datetime
from adapters.messages_adapter import get_new_messages


async def prepare(resp):
    formatted_messages = []
    for el in resp:
        message_data = {
            'message': el[0],
            'ddateTime': el[1].strftime('%H:%M:%S'),
            'sender': el[2],
        }
        formatted_messages.append(message_data)
    list_items = "".join(
        f"<li class='bg-white rounded-lg p-4 m-4 shadow-sm transition duration-300 ease-in-out hover:shadow-md'>"
        f"{msg['ddateTime']} - {msg['sender']}: <b>{msg['message']}</b></li>" for msg in formatted_messages)
    response_html = f"<ul>{list_items}</ul>"
    return response_html


async def prepare_dict(resp):
    formatted_messages = []
    for el in resp:
        message_data = {
            'message': el['content'],
            'ddateTime': el['timestamp'].strftime('%H:%M:%S'),
            'sender': el['username'],
        }
        formatted_messages.append(message_data)

    return json.dumps(formatted_messages)


async def prepare_message(func):
    """
    Call adapter service and format messages
    :param func: service method to call
    :return: formatted HTML
    """
    messages = func()
    formatted_messages = []

    for el in messages:
        message_data = {
            'id': el[0],
            'message': el[1],
            'dateTime': el[2].strftime('%H:%M:%S'),
            'username': el[3],
            'user_id': el[4]
        }
        formatted_messages.append(message_data)

    html_parts = []
    for msg in formatted_messages:
        html_part = f"""
        <div class="message-item p-2 mb-2 bg-gray-50 rounded-lg" data-message-id="{msg['id']}" data-user-id="{msg['user_id']}">
            <div class="flex justify-between items-start">
                <div class="flex-1">
                    <strong>{msg['username']}</strong> <span class="text-gray-500 text-sm">{msg['dateTime']}</span>
                    <div class="mt-1">{msg['message']}</div>
                </div>
                <button class="delete-btn ml-2 text-red-500 hover:text-red-700 text-sm" 
                        data-message-id="{msg['id']}" data-user-id="{msg['user_id']}"
                        style="display: none;">
                    🗑️
                </button>
            </div>
        </div>
        """
        html_parts.append(html_part)

    response_html = "".join(html_parts)
    return response_html


async def fetch_all_messages(last_timestamp):
    """
    Fetch messages for all users in the instance.
    :param last_timestamp: The last timestamp of messages received (can be Unix timestamp or datetime).
    :return: A JSON response with new messages since last_timestamp.
    """

    messages = get_new_messages(last_timestamp)
    print(len(messages))

    if isinstance(last_timestamp, (int, float)):
        last_timestamp = datetime.fromtimestamp(last_timestamp)

    new_messages = [
        msg for msg in messages if isinstance(msg['timestamp'], datetime) and msg['timestamp'] > last_timestamp
    ]
    print(len(new_messages))

    return await prepare_dict(new_messages)


async def fetch_histories(chat_service):
    """
    Fetch messages by user_id
    :param chat_service:
    :return:
    """
    messages = chat_service.load_history()
    formatted_messages = []
    for el in messages:
        message_data = {
            'ddateTime': el[1].strftime('%H:%M:%S'),
            'message': el[0]
        }
        formatted_messages.append(message_data)
    list_items = "".join(f"<li>{msg['ddateTime']}: <b>{msg['message']}</b></li>" for msg in formatted_messages)
    response_html = f"<ul>{list_items}</ul>"
    return response_html
