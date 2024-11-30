

# Промпты оформлять ввиде функции возвращающих жти же промпты.


def prompt_main_structure_project(structure):
    return f'''Структура проекта:
```
{structure}
```
Стандарты архитектуры:
- Используется монорепозиторий.
- В корне проекта находятся файлы: .gitignore, .editorconfig, .gitattributes.
- В каталоге `deployment` расположены файлы для CI/CD (структура обсуждается с командой DevOps).
- В каталоге `docs` хранится техническая документация, включая схемы, созданные с использованием PlantUML:
  - Схема прецедентов.
  - Схема базы данных.
  - Схема развертывания.
  - Схема компонентов.
  - Дока Swagger генерируется на бэкенде при вызове соответствующего эндпоинта.
  - Документацию по бизнес-процессам можно хранить здесь или в отдельной Wiki.
- Внутри проекта находится каталог `components`, предназначенный для разделения фронтенда и бэкенда (структура фронтенда обсуждается с соответствующей командой).
- В каталоге `components` расположен каталог `demo_project_backend`, который является корнем для бэкенд-модулей проекта. Этот каталог также служит источником импорта для Python-модулей проекта.
- Каталог бэкенда оформлен как стандартный Python-пакет:
  - В файле `setup.py` описаны метаданные пакета и зависимости.
  - Допускается использование файла `setup.cfg`.
  - В файле `pyproject.toml` содержатся настройки сборщиков, автоформатеров и других инструментов.
  - В файле `README.md` содержится краткое описание проекта, инструкции по развертыванию на локальной машине/контейнере, запуску тестов, схеме прав/групп и другие важные сведения.
- Каталог с исходным кодом является корнем импорта внутри проекта, рекомендуется использовать лаконичное имя.
```
**Задание:**  
Представь, что ты архитектор it проектов. Тебе дали задание найти и исправить ошибки в структуре проекта. Все стандарты я написал выше.
Если есть ошибки в архитектуре проекта - то пиши их так, как будто ты пишешь отчет, но по стилю как Markdown. Если их нет, то ничего не пиши.
Тебе необходимо проитись по каждому пункту отедльно и если есть ошибка - сообщить о ней.
Тебе не нужны ни цель проекта, ни язык программирвоания который используется в проекте. Тебе Просто нужно провести анализ стуркутры проекта по отмеченным компниям пунктам.
Также нужно представить строгий отчет после анализа, без введения и своего личного мнения, без заключения.
Для того чтобы выделить структуру или код используй такие кавычки, Вот пример ``` print("Hello") ```.
Если хочешь выделить жирным используй звездочки. Например, *custom_file.txt* или *Отчет по анализу*
Все ошибки должны быть записаны под заголовком Архитектурное наружение и выделены жирным. Например, # **Архитектурное нарушение**, а подзаголовки ## **<Подзаголовок>**. 
Ты не должен писать в конце писать вывод, делать отчеты по всему анализу, подводить итоги анализа, давать рекомендации. Это категорически запрещено.
Твоя задача - найти все ошибки связанные со стандартами которые я тебе передал.
Также в конце выведи исправленную версию структуры проекта исходя из ошибок пользователя.
Вот пример того как должен быть офрмлен вывод отчета по Архитектурным нарушениям:
# Архитектурный анализ проекта

## Отсутствие файла .editorconfig
Файл .editorconfig отсутствует в корне проекта, что может привести к несоответствиям в стиле кода и форматировании между различными редакторами и окружениями.

## Отсутствие файла .gitattributes
Файл .gitattributes отсутствует в корне проекта, что может повлиять на правильное отображение и обработку спецсимволов в репозитории.

## Отсутствие каталога deployment
Каталог deployment отсутствует в проекте, что может затруднить процесс CI/CD.

## Отсутствие схемы компонентов в каталоге docs
В каталоге docs отсутствует схема компонентов, что может усложнить понимание структуры проекта и взаимодействия между его частями.

## Неправильная структура каталога components
Каталог components содержит только каталог demo_project_backend, что не соответствует стандарту разделения фронтенда и бэкенда. Необходимо добавить каталог для фронтенда и обсудить его структуру с соответствующей командой.

## Отсутствие файла setup.cfg в каталоге demoprojectbackend
Файл setup.cfg отсутствует в каталоге demo_project_backend, что может усложнить настройку и управление пакетом.

## Неправильное расположение файла README.md в каталоге demoprojectbackend
Файл README.md расположен в каталоге demo_project_backend, а не в корне проекта, как это рекомендуется в стандартах.

## Исправленная версия структуры проекта

Ты можешь только дополнять этот шаблон ошибками которые ты обнаружил.
'''
