# -*- coding: utf-8 -*- 
import requests
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from time import sleep
import json
from selenium.webdriver.chrome.options import Options
import random
import pyautogui
import datetime

api = "7bcfdc5184c0af85db1182ca132fc0fe"
sleep_ = 3

# Читаем файл и узнаем количество строк
common2 = []
count_lines = 0
with open('text.txt', 'r',encoding="utf-8") as f:
    common = f.readlines()
for l in common:
	common2.append(l)


common = common2
print('Скрипт запущен!')
#options = Options()
#options.headless = True

names = ['Myhailo', "Sergiy","Anton","Jek","Bogdan","Dima","Alexey"]
surnames = ['Smirnov','Ivanov','Kuznecov','Socolov','Popov','Lebedev','Morozov']


for i in range(len(common)):
	if True:
		print(80*'*')
		print(f'Локация номер {i+1}')
		print(f'Локация {common[i]}')
		from_ = common[i].split('-')[0].replace(' ', '')
		where = common[i].split('-')[1].replace('\n', '').replace(' ', '')

		opts = Options()
		opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
		dr = webdriver.Chrome(chrome_options=opts) #options=options
		dr.maximize_window()
		sleep(2)
		dr.delete_all_cookies()

		
		dr.get('https://taxi.yandex.ru/')
		sleep(sleep_)
		sleep(sleep_)

        # Ввод данных для заказа(ул.)
		try:
			all = dr.find_elements_by_class_name("amber-input__control")
			all[0].send_keys(from_)
			sleep(sleep_)
			dr.find_element_by_class_name('amber-list-item__col.amber-list-item__col_grow').click()
			sleep(sleep_)
			all[1].send_keys(where)
			sleep(sleep_)
			dr.find_element_by_class_name('amber-list-item__col.amber-list-item__col_grow').click()
			sleep(sleep_)
		except:
			print(f'Ошибка. Пропускаем данную локацию: {common[i]}')
			dr.close()
			sleep(5)
			continue

        ###########

        
		but = dr.find_elements_by_class_name('amber-button__text')
		try:
			#dr.delete_all_cookies()
			sleep(3)
			#dr.delete_all_cookies()
			but[1].click()
		except:
			print(f'Нету свободных машин. Пропускаем данную локацию {common[i]}!')
			dr.close()
			sleep(5)
			continue

		sleep(sleep_)
		sleep(sleep_)
		sleep(sleep_)

#######################################
		
		#переходим на вторую страницу
		tabs = dr.window_handles
		#print(tabs)
		dr.switch_to.window(tabs[-1])

		# Взять номер и увести
        
        #print('Берем номер телефона')
        # 900 565
		pyautogui.click(900,565)
		pyautogui.keyDown('backspace')
		pyautogui.keyDown('backspace')
		pyautogui.keyUp('backspace')
		pyautogui.keyUp('backspace')

		try:
			responce = requests.get('https://onlinesim.ru/api/getNum.php?apikey=7bcfdc5184c0af85db1182ca132fc0fe&service=yandex&number=True')
			soup = bs4(responce.content, 'html.parser').get_text(strip=True)
			js = json.loads(soup)
			try:
				id_ = js["tzid"]
			except:
				print('Недостаточно средств на балансе! Стоп скрипт')
				break
			number = js["number"]
			#print(number)
			#print(f'id: {id_}')
		except Exception as ex:
			print('Ошибка: '+str(ex))
			print(f'Пропускаем данную локацию: {common[i]}')
			dr.close()
			sleep(5)
			continue

		# пишем номер
		#try:
			#tabs = dr.window_handles
			#print(tabs)
		#except:
			#print('EEEEEEEEEEEEE')
		#dr.switch_to.window(tabs[-1])

		ph = dr.find_element_by_class_name('Textinput-Control')
		ph.send_keys(number)
		dr.find_element_by_class_name('Button2.Button2_size_l.Button2_view_action.Button2_width_max.Button2_type_submit').click()
		sleep(sleep_)



		# Уводим код из смс
        #print('Уводим код из смс')
		try:
			responce = requests.get(f'https://onlinesim.ru/api/getState.php?apikey=7bcfdc5184c0af85db1182ca132fc0fe&tzid={id_}&message_to_code=1')
			soup = bs4(responce.content, 'html.parser').get_text(strip=True)
			i = 0
			while 'msg' not in str(soup):
				responce = requests.get(f'https://onlinesim.ru/api/getState.php?apikey=7bcfdc5184c0af85db1182ca132fc0fe&tzid={id_}&message_to_code=1')
				soup = bs4(responce.content, 'html.parser').get_text(strip=True)
				i +=1
				sleep(3)
				if i == 30:
					print(f'Скрипт ждет смс более {i} сек. Скорее всего сервис временно заблокировал скрипт. (Перезапустите програму, если тоже самое, то смените proxy). Пропускаем локацию!')
					dr.close()
					sleep(5)
					continue
			js = json.loads(soup)
			dr.find_element_by_class_name('Textinput-Control').send_keys(js[0]["msg"])     ####
			#dr.find_element_by_class_name('Button2.Button2_size_l.Button2_view_action.Button2_width_max').click()	####

		except Exception as ex:
			print('Ошибка: '+str(ex))
			print(f'Пропускаем данную локацию: {common[i]}')
			dr.close()
			sleep(5)
			continue
		
		# Уводим имя и фамилию
		
		sleep(10)
		
		pyautogui.click(878,545)
		pyautogui.write(f'{random.choice(names)}', interval=0.1)

		pyautogui.click(889,615)
		pyautogui.write(f'{random.choice(surnames)}', interval=0.1)

		pyautogui.click(967,695)
		sleep(2)

		



		#Підтверджуем условия
		dr.find_element_by_class_name('Checkbox-Control').click()
		dr.find_element_by_class_name('Button2.Button2_size_l.Button2_view_action.Button2_width_max').click()

		#переходим на первую страницу
		#

		sleep(5)
		sleep(5)
		#dr.delete_all_cookies()
		dr.switch_to.window(tabs[0])
		#dr.delete_all_cookies()
		acc = dr.find_elements_by_class_name('amber-button__text')
		acc[0].click()
		requests.get(f'https://onlinesim.ru/api/setOperationOk.php?apikey=7bcfdc5184c0af85db1182ca132fc0fe&tzid={id_}')
		sleep(sleep_)
		sleep(sleep_)
		#dr.delete_all_cookies()

        # Если цена изменилась
		# try:
		# 	if dr.find_element_by_class_name('amber-alert__content'):
		# 		acc = dr.find_elements_by_class_name('amber-button__text')
		# 		acc[1].click()
		# except:
		# 	print(f'Нету свободных машин. Пропускаем данную локацию {common[i]}!')
		# 	dr.close()
		# 	sleep(5)
		# 	continue

		try:
			acc = dr.find_elements_by_class_name('amber-button__text')
			acc[0].click()
		except:
			print(f'Нету свободных машин. Пропускаем данную локацию {common[i]}!')
			dr.close()
			sleep(5)
			continue

		pyautogui.click(218, 522)

		sleep(sleep_)

        # Ждем когда найдем таксиста
        #print('Поиск водителя')
		try:
			while 'Поиск' in dr.find_element_by_class_name('CardTitle__status').text:
				sleep(3)
		except:
			sleep(120)

		print('Результат')
		print('Статус: '+ dr.find_element_by_class_name('CardTitle__status').text)
		NumAndCar = dr.find_element_by_class_name('CardTitle__car').text
		print('Машина: '+ NumAndCar.split('\n')[0])
		print('Hомер: '+NumAndCar.split('\n')[1])

		sleep(60)

        # Действия "Уже иду!"
		while dr.find_element_by_class_name('CardTitle__status').text != "Водитель ждёт":
			print('###Статус: '+dr.find_element_by_class_name('CardTitle__status').text)
			sleep(60)
		print("Статус: "+ dr.find_element_by_class_name('CardTitle__status').text)
        
        #action = '1'
        #action = input('Что делать с заказом: (Варианты: "Уже иду") ')
		sleep(3)
		all_but = dr.find_elements_by_class_name('amber-button.amber-button_theme_circle.amber-button_size_circle-m')
        #if action == 'Отмена':
        #    all_but[2].click()
        #    alls = dr.find_elements_by_class_name('amber-button__text')
        #    alls[4].click()
        #if action in 'Уже иду':
		all_but[1].click()
        #dr.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/section[3]/div/button').click()

        #print('Выполнено!')

		car = NumAndCar.split('\n')[0]
		num = {NumAndCar.split('\n')[1]}

		with open('data.csv', 'a') as f:
			f.write(f"{common[i]}; {dr.find_element_by_class_name('CardTitle__status').text}; {car}; {num};")


		print('======Водитель ждет, запускаем вторую локацию.========')
		dr.close()
		sleep(5)
		print(80*'*')
	else:
    #except Exception as ex:
		print(f'Ошибка с локацией' + str(ex))
		dr.close()

