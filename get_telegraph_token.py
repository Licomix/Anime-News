from telegraph import Telegraph
from telegraph import TelegraphException

# Инициализация Telegraph
telegraph = Telegraph()

# Регистрация нового аккаунта (это нужно сделать только один раз)
try:
    # Создаем новый аккаунт и получаем токен
    response = telegraph.create_account(short_name='MyBot', author_name='Bot Author')
    access_token = response['access_token']
    print('Account created. Access token:', access_token)
except TelegraphException as e:
    print('Error creating account:', e)
