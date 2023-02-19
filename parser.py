import pandas as pd
import csv
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def try_except(func):               # Декоратор для перехвата ошибок
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
        except:
            data = None
        return data
    return wrapper


@try_except
def check_404(driver):
    try:
        driver.find_element(By.CLASS_NAME, "content404__title")
    except NoSuchElementException:
        return False
    return True


@try_except
def open_spec_and_desc(driver):
    driver.find_element(By.CLASS_NAME, "j-parameters-btn").click()  # открываем характеристики
    driver.find_element(By.CLASS_NAME, "j-description-btn").click()  # открываем описание


@try_except
def get_sku():
    articul = browser.find_element(By.CSS_SELECTOR, '#productNmId')
    return articul.text


@try_except
def get_name():
    nazv = browser.find_element(By.XPATH, "//h1[@data-link='text{:selectedNomenclature^goodsName || product^goodsName}']")
    return nazv.text


@try_except
def get_stars():
    rating = browser.find_element(By.XPATH, "//span[contains(@data-link, 'text{: product^star}')]")
    return rating.text


@try_except
def get_sostav():
    sost = browser.find_element(By.XPATH, "//span[contains(@data-link, 'text{:selectedNomenclature^consist}')]")
    return sost.text


@try_except
def get_color():
    col = browser.find_element(By.CLASS_NAME, 'color')
    return col.text


@try_except
def get_pictures():
    pict = browser.find_element(By.CSS_SELECTOR, '.photo-zoom__preview.j-zoom-image')
    return pict.get_attribute('src')


@try_except
def get_description():
    desc = browser.find_element(By.CLASS_NAME, "collapsable__text")
    return desc.text


@try_except
# Собираем таблицу характеристик
def get_raw_specifications():
    spec = browser.find_element(By.CLASS_NAME, "j-add-info-section")
    return spec.text


@try_except
# Добавляем найденные характеристики в словарь
def get_specifications():
    raw_spec = get_raw_specifications()
    s = raw_spec[26::].split('\n')
    new_dict = {'Фактура материала': '', 'Вырез горловины': '', 'Тип рукава': '', 'Модель трусов': '', 'Вид застежки': '',
     'Декоративные элементы': '', 'Особенности модели': '', 'Рисунок': '', 'Покрой': '', 'Назначение': '', 'Тип ростовки': '',
     'Высота упаковки': '', 'Длина упаковки': '', 'Ширина упаковки': '', 'Уход за вещами': '', 'Любимые герои': '',
     'Параметры модели на фото (ОГ-ОТ-ОБ)': '', 'Размер на модели': '', 'Рост модели на фото': '', 'Страна производства': '',
     'Коллекция': '', 'Комплектация': '', 'Пол': '', 'Сезон': '', 'ТНВЭД': ''}
    for i in s:
        for j in new_dict:
            if j in i:
                n = s.index(i)
                s[n] = s[n].replace(j, '').strip()
                new_dict[j] = s[n]
                break
    return new_dict


@try_except
def parse_data():
    new_dict = {'Артикул': get_sku(), 'Наименование': get_name(), 'Рейтинг': get_stars(), 'Состав': get_sostav(),
                'Цвет': get_color(), 'Фото': get_pictures(), 'Описание': get_description(), 'Фактура материала': '',
                'Вырез горловины': '', 'Тип рукава': '', 'Модель трусов': '', 'Вид застежки': '',
                'Декоративные элементы': '', 'Особенности модели': '', 'Рисунок': '', 'Покрой': '', 'Назначение': '',
                'Тип ростовки': '', 'Высота упаковки': '', 'Длина упаковки': '', 'Ширина упаковки': '',
                'Уход за вещами': '', 'Любимые герои': '', 'Параметры модели на фото (ОГ-ОТ-ОБ)': '',
                'Размер на модели': '', 'Рост модели на фото': '', 'Страна производства': '', 'Коллекция': '',
                'Комплектация': '', 'Пол': '', 'Сезон': '', 'ТНВЭД': ''}
    spec_dict = get_specifications()
    for key, value in spec_dict.items():
        if key in new_dict:
            new_dict[key] = value
    return new_dict


@try_except
def complete_dictionary():
    card_dict = parse_data()
    for key, value in card_dict.items():
        if key in parsing_cards:
            parsing_cards[key].append(value)
    return parsing_cards


if __name__ == "__main__":
    try:
        parsing_cards = {'Артикул': [], 'Наименование': [], 'Рейтинг': [], 'Состав': [], 'Цвет': [], 'Фото': [], 'Описание': [], 'Фактура материала': [],
                         'Вырез горловины': [], 'Тип рукава': [], 'Модель трусов': [], 'Вид застежки': [], 'Декоративные элементы': [], 'Особенности модели': [],
                         'Рисунок': [], 'Покрой': [], 'Назначение': [], 'Тип ростовки': [], 'Высота упаковки': [], 'Длина упаковки': [], 'Ширина упаковки': [],
                         'Уход за вещами': [], 'Любимые герои': [], 'Параметры модели на фото (ОГ-ОТ-ОБ)': [], 'Размер на модели': [],
                         'Рост модели на фото': [], 'Страна производства': [], 'Коллекция': [], 'Комплектация': [], 'Пол': [], 'Сезон': [], 'ТНВЭД': []}
        browser = Chrome()
        browser.implicitly_wait(5)
        with open('urls_for_tests.csv', 'r', encoding='utf-8') as file:
            for line in csv.DictReader(file):
                url = line['urls']
                browser.get(url)  # открываем ссылку
                if check_404(browser) == False:
                    open_spec_and_desc(browser)
                    parsing_cards = complete_dictionary()
                else:
                    continue
        parsing = pd.DataFrame.from_dict(parsing_cards, orient='index')
        path = r'C:\Users\Irina_Fomina\PycharmProjects\parser_wb'
        parsing.to_csv('parsing_2.csv')


    finally:
        browser.quit()
