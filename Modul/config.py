import vk_api
import random
from datetime import date, datetime, time

whiteWordPart = [
	'лайк',
	'репост',
	'поделится',
	'поделиться',
	]

blackWordPart = (
	'порно',
	'знакомств',
	'sex',
	'казино',
	'вечеринк',
	'кастинг',
	)

noInterecting = (
	'дрипк',
	'vape',
	'испаритель',
	'предтрен',
	'тотализатор',
	'маникюр',
	'наращивание',
	'увеличение',
	'ламинирование',
	'шугаринг',
	'кружева',
	'лосины',
	'фотос',
	)

dopActions = (
	'закреп',
	'написать',
	'оставить',
	'напишите',
	'оставьте',
	'добавить фото',
	'зарегистрироваться',
	'за счет победителя',
	'на стене не ниже',
	)


vinePosts = (
	'поздравляем',
	'у нас победител',
	'ура! победител',
	'наш победитель!',
	'итоги подвели',
	'победители определены',
	'подводим итог',
	'победителя выбрали',
	'победителя определелили',
	'заканчиваются розыгрыши',
	'завершаются три',
	'завершаются два',
	'часов до завершения конкурс',
	)


# results = pool.method('newsfeed', {'q':u'Конкурс репост подарки Сочи'})
# results = pool.method('newsfeed', {'q':u'Конкурс репост подарки Россия'})
# results = groups.search('репост')
# results = groups.search('бесплатный')


# Репост записи
# results.wall.repost

# Вступить в группу
# results.groups.join

#time.sleep(120.0+random.random()*200.0)
