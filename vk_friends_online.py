import vk
import getpass
import argparse


APP_ID = 5653246


def get_user_login():
    return input('Логин пользователя: ')


def get_user_password():
    return getpass.getpass('Пароль: ')


def get_credentials(namespace):
    if not namespace.token and (not namespace.login or not namespace.password):
        login = get_user_login()
        password = get_user_password()
    else:
        login = namespace.login
        password = namespace.password
    return login, password, namespace.token


def get_online_friends(login, password, token):
    if token:
        session = vk.Session(access_token=token)
    else:
        session = vk.AuthSession(
            app_id=APP_ID,
            user_login=login,
            user_password=password,
            scope='friends'
        )
    api = vk.API(session)
    friends_online = api.friends.getOnline()
    return api.users.get(user_ids=friends_online)


def output_friends_to_console(friends_online):
    if friends_online:
        print('Список друзей онлайн:')
        for num, friend in enumerate(friends_online, start=1):
            print('%s. %s %s' % (num, friend['first_name'],
                  friend['last_name']))
    else:
        print('Нет друзей онлайн.')


def create_parser():
    parser = argparse.ArgumentParser(description='Скрипт выводит список \
                                     онлайн друзей пользователя VK.')
    parser.add_argument('-t', '--token', metavar='ТОКЕН',
                        help='Ключ доступа пользователя VK.')
    parser.add_argument('-l', '--login', metavar='ЛОГИН',
                        help='Логин пользователя VK.')
    parser.add_argument('-p', '--password', metavar='ПАРОЛЬ',
                        help='Пароль пользователя VK.')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    login, password, token = get_credentials(namespace)
    friends_online = get_online_friends(login, password, token)
    output_friends_to_console(friends_online)
