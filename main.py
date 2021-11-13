import os
import json
import boto3
import random

from dadata import Dadata
from utils import load_users, dump_users, load_complements, send_message
from utils import markdown_escape, admin_id

from dotenv import load_dotenv
load_dotenv()

s3 = boto3.session.Session().client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)
trigger_invokes = list(range(10, 19, 2))
chance = 1 / (len(trigger_invokes) + 1)

dadata = Dadata(token=os.getenv('DADATA_TOKEN'),
                secret=os.getenv('DADATA_SECRET'))


def handler(event, context):
    if 'messages' in event:
        # сработал триггер
        # с вероятностью chance отправляем сообщения
        if random.random() < chance:
            print('Рассылаю сообщения...')
            for user in users:
                param = {'chat_id': user['id'],
                         'text': generate_awesome_message(user).translate(markdown_escape)}
                send_message(params=param)
        else:
            print('Игнорирую рассылку')

    else:
        # пришло сообщение от телеграмма
        tg_input = json.loads(event['body'])
        print(tg_input)
        tg_text = tg_input['message']['text'].strip()
        user = tg_input['message']['from']

        if tg_text.startswith('/start'):
            res = start_message

        elif tg_text.startswith('/help'):
            res = help_message

        elif tg_text.startswith('/subscribe'):
            if user['id'] in {x['id'] for x in users}:
                res = fail_subscribe_message
            else:
                users.append(user)
                dump_users(users, s3=s3, dadata=dadata)
                res = subscribe_message

        elif tg_text.startswith('/unsubscribe'):
            user = [x for x in users if x['id'] == user['id']]
            if len(user) > 0:
                users.remove(user[0])
                dump_users(users, s3=s3, dadata=dadata)
                res = unsubscribe_message
            else:
                res = fail_unsubscribe_message

        elif tg_text.startswith('/'):
            res = 'Неизвестная комманда'

        else:
            # если это ответ от меня, пересылаем отправителю
            if user['id'] == admin_id and \
                    'reply_to_message' in tg_input['message'] and \
                    'forward_from' in tg_input['message']['reply_to_message']:
                answer = {
                    "method": "sendMessage",
                    "chat_id": tg_input['message']['reply_to_message']['forward_from']['id'],
                    "text": tg_text
                }
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(answer)
                }
            # иначе пересылаем мне сообщение
            else:
                answer = {
                    "method": "forwardMessage",
                    "chat_id": admin_id,
                    "from_chat_id": tg_input['message']['chat']['id'],
                    "message_id": tg_input['message']['message_id']
                }
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(answer)
                }

        answer = {
            "method": "sendMessage",
            "chat_id": tg_input['message']['chat']['id'],
            "parse_mode": 'MarkdownV2',
            "text": res.translate(markdown_escape)
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'isBase64Encoded': False,
            'body': json.dumps(answer)
        }


# формирует обращение случайным образом с обработкой Рыжа
def get_greeting(user):
    greetings = ['', user['first_name']]
    if user['id'] == 281407619:
        greetings.append('Рыж')
    choice = random.choice(greetings)
    if choice == '':
        return 'Ты'
    else:
        return f'{choice}, ты'


# формирует сообщение целиком по шаблону случайным образом
def generate_awesome_message(user):
    if random.random() < 0.3:
        # формируем сообщение старым образом
        nouns = ['топчик', 'пушка', 'космос', 'бомба']
        epithets = ['', 'просто', 'сегодня']
        message = "{greeting} {epithet} {noun}".format(
            greeting=get_greeting(user),
            epithet=random.choice(epithets),
            noun=random.choice(nouns)
        )
        return message.replace('  ', ' ')
    else:
        # выбираем один из комплементов
        message = random.choice(complement_list)
        return message


start_message = 'Этот бот может примерно раз в день в случайное время отправлять вам приятное сообщение. ' \
                'Если вы согласны, нужно подписаться. Отписаться можно в любой момент. Нажмите /help'
help_message = 'Чтобы подписаться, нажмите /subscribe' + '\n' \
               'Чтобы отписаться, нажмите /unsubscribe'
info_message = ''
subscribe_message = 'Вы подписались! Отныне начнут приходить сообщения.' + '\n' \
                    'Не волнуйся, сообщения будут. Чтобы они были приятными, о них нужно забыть'
unsubscribe_message = 'Вы отписались, сообщения больше не будут приходить'
fail_subscribe_message = 'Вы уже подписаны'
fail_unsubscribe_message = 'Вы ещё не подписаны'

users = load_users(s3=s3)
complement_list = load_complements(s3=s3)
