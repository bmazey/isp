def handler(event, context):
    userMessage = event['message']
    botReply = "Sorry - I don't understand that."

    if userMessage is None or len(userMessage) < 1:
        return {
            'statusCode': 200,
            'body': json.dumps(botReply)
        }

    response = client.post_text(botName='higgins_bot',
                                botAlias='$LATEST',
                                userId='USER1',
                                inputText=userMessage)

    if response['message'] is not None or len(response['message']) > 0:
        userMessage = response['message']

    return {
        'statusCode': 200,
        'body': json.dumps(userMessage)
    }