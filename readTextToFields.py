import datetime
import re


def readTextToFields(fields, str_line):
    """ Парсим строку, достаем данные по полям"""

    def getfloat(str):
        # print(str)
        new_str = str.replace(',‚', ',')
        # print(new_str)
        new_str = new_str.replace('‚', '.')
        # print(new_str)
        new_str = new_str.replace(',', '.')
        # print(new_str)
        new_str = new_str.replace('Р', '')
        # print(new_str)
        new_str = new_str.replace('>', '')
        # print(new_str)
        new_str = new_str.replace('<', '')
        # print(new_str)
        new_str = new_str.replace('»', '')
        # print(new_str)
        new_str = new_str.replace('«', '')


        if new_str.isdigit():
            result = float(new_str)
            # print(f'Result 1 - {result}')
        else:
            new_str_num = re.findall(r'\d*\.\d\d', new_str)
            try:
                result = float(new_str_num[0])
                # print(f'Result 2 - {result}')

            except IndexError:
                print(f'Ошибка функции getFloat old >>> {new_str} - {fields.name}')
                result = 0.0
        return result

    # print(str_line)

    position = 0

    bed_words = ['История', 'Отмена', 'Обновлен', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
                 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь', 'Поездка', 'попали', 'этот', 'Оцените',
                 'качества', 'следующем', 'Доступно', 'комплименты', 'приоритет', 'транзакции']

    while position < len(str_line):
        """ Неверный скрин """
        atention = ''
        for i in bed_words:
            if str_line[position] == i:
                atention = 'atention'
                # print(f'atention {i}')
                break
        if atention == 'atention':
            break
        if str_line[position] == 'За' and str_line[position + 1] == 'неделю':
            break
        if str_line[position] == 'На' and str_line[position + 1] == 'основе':
            break
        if str_line[position] == 'следующем' and str_line[position + 1] == 'месяце':
            break
        if str_line[position] == 'эту' and str_line[position + 1] == 'неделю':
            break

        if str_line[position] == 'Сегодня':
            if str_line[position + 1] == '0,00':
                break
            if str_line[position + 1] == '0,00Р':
                break
            if str_line[position + 1] == '0,00?':
                break
            if str_line[position + 1] == '0,00?Р':
                break

        """ Активность, Рейтинг, Уровень """
        if str_line[position] == 'Самозанятый':
            try:
                fields.activ = int(str_line[position + 1])
                fields.rait = float(str_line[position + 2])
                if str_line[position + 3] == 'Бронза':
                    fields.grate = 3
                if str_line[position + 3] == 'Золото':
                    fields.grate = 2
                if str_line[position + 3] == 'Платина':
                    fields.grate = 1
            except:
                print(
                    f'Error active old {fields.name} \n {str_line} \n- {str_line[position + 1]}/{str_line[position + 2]}')
            position += 1
            continue

        if str_line[position] == 'Сегодня':
            """ Всего выручка """
            all_profit_str = str_line[position + 1] + str_line[position + 2] + str_line[position + 3]
            # print(all_profit_str)

            try:
                fields.all_profit = getfloat(all_profit_str)
            except:
                print(f'Error all_profit old >{all_profit_str}<')
                # print(getfloat(all_profit_str))

            position += 1
            continue

        if str_line[position] == 'карта':  # Выручка карта
            cart_profit_str = str_line[position - 2] + str_line[position - 1]

            try:
                fields.cart_profit = getfloat(cart_profit_str)
            except:
                print(f'Error card old {fields.name} - {cart_profit_str}')

        """ Выручка наличные """
        if str_line[position] == 'карта':
            if str_line[position + 1] != 'водителя':
                if len(str_line[position + 2]) == 1:
                    cash_profit_str = str_line[position + 2] + str_line[position + 3]
                else:
                    cash_profit_str = str_line[position + 2]
                try:
                    fields.cash_profit = getfloat(cash_profit_str)
                except:
                    print(f"Ошибка cash Old {fields.name} - {cash_profit_str} - {str_line}")
            position += 1
            continue

        """ Заказов """
        if str_line[position] == 'заказов' or str_line[position] == 'заказа':
            if str_line[position + 1] == 'Комиссия':
                if str_line[position - 1] != 'стоимости':
                    # print(str_line[position - 1])
                    orders_str = str_line[position - 1]
                    try:
                        orders_num = re.findall(r'\d*', orders_str)
                        fields.orders = int(orders_num[0])
                    except:
                        print(f'Error order old {fields.name} - {str_line[position - 1]} - {str_line}')
            position += 1
            continue

        """ Комиссия """
        if str_line[position] == 'Комиссия' and str_line[position + 1] == 'парка':
            if str_line[position - 1] == 'Яндекса':
                position += 1
                continue
            commission_str = str_line[position - 2] + str_line[position - 1]

            try:
                fields.commission = getfloat(commission_str)
            except:
                print(f'Error commission old {fields.name} - {commission_str}')
            position += 1
            continue

        """ Пробег """
        if str_line[position] == 'Пробег':
            mileage_str = str_line[position + 1]
            if str_line[position + 1] == 'О':
                fields.mileage = 0
                position += 1
                continue
            if str_line[position + 1] == 'З':
                fields.mileage = 3
                position += 1
                continue
            try:
                mileage_str = str_line[position + 1] + str_line[position + 2]
                mileage_num = re.findall(r'\d*', mileage_str)
                fields.mileage = int(mileage_num[0])
            except:
                print(f'Error mileage old {fields.name} - {str_line[position + 1]}/{str_line[position + 2]} - {str_line}')
            position += 1
            continue

        if str_line[position] == 'Баланс':
            if position < len(str_line) - 4:
                if len(str_line[position + 1]) == 1:
                    balance_str = str_line[position + 1] + str_line[position + 2]
                else:
                    balance_str = str_line[position + 1]

                try:
                    fields.balance = getfloat(balance_str)
                except:
                    print(f'Error balanse old {fields.name} \n {str_line} \n- {balance_str}')

        position += 1

    ''' Получение даты из имени файла'''

    str_line = fields.name.split('_')
    datetimeplus = str_line[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    fields.date = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')