# Описание:
# 1. Спрашивать у пользователя первоначальный запрос.
# 2. Переходить по первоначальному запросу в Википедии.
# 3. Предлагать пользователю три варианта действий:
# листать параграфы текущей статьи;
# перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
# выйти из программы.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Инициализация драйвера
# service = Service(executable_path="path/to/chromedriver")  # Замените на путь к вашему chromedriver
# browser = webdriver.Chrome(service=service)
browser = webdriver.Chrome()

browser.get(
    'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0')


# Функция для поиска статьи на Википедии
def search_wikipedia(query):
    browser.get('https://www.wikipedia.org/')
    search_box = browser.find_element(By.NAME, 'search')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждем загрузки страницы


# Функция для пролистывания параграфов статьи
def scroll_paragraphs():
    paragraphs = browser.find_elements(By.TAG_NAME, 'p')
    for indx, paragraph in enumerate(paragraphs):
        print(f"Параграф {indx + 1}:")
        print(paragraph.text)
        next_action = input("Введите 'n' для следующего параграфа, 'q' для выхода: ")
        if next_action == 'q':
            break


# Функция для перехода на связанную статью
def navigate_internal_links():
    links = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/wiki/"]')
    for indx, link in enumerate(links[:10]):  # Показать первые 10 связанных ссылок
        print(f"{indx + 1}. {link.text}")

    choice = int(input("Введите номер статьи для перехода или 0 для выхода: "))
    if choice == 0:
        return False
    else:
        links[choice - 1].click()
        time.sleep(2)  # Ждем загрузки страницы
        return True


# Основная программа
def main():
    query = input("Введите ваш запрос для Википедии: ")
    search_wikipedia(query)

    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        choice = input("Введите номер действия (1, 2, 3): ")

        if choice == '1':
            scroll_paragraphs()
        elif choice == '2':
            if not navigate_internal_links():
                break
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

    browser.quit()


if __name__ == "__main__":
    main()
