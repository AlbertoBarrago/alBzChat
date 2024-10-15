async def make_call_and_handle_result(method_to_get_data):
    """
    Fetch messages for all users in the instance
    :param method_to_get_data:
    :return:
    """
    resp = method_to_get_data()
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



async def make_call_and_handle_result_history(chat_service):
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