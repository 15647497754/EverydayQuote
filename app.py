from flask import Flask, render_template, request, redirect, url_for, make_response
import random

app = Flask(__name__)

# Пример базы данных цитат
quotes_db = [
    {"text": "Два вида человеческой слабости: вера в судьбу после успеха и виноватость перед судьбой после неудачи.", "author": "Жорж Клемансо", "category": "Вдохновляющие"},
    {"text": "Если вы хотите, чтобы что-то было сделано, поручите это заняться занятому человеку.", "author": "Лесли Таунесенд", "category": "Мотивационные"},
    {"text": "Слабый человек никогда не прощает. Прощение присуще сильным.", "author": "Махатма Ганди", "category": "Философские"},
    {"text": "Любовь — это великая сила. Когда мы любим, мы всегда стремимся стать лучше, чем мы есть.", "author": "Далай Лама", "category": "Вдохновляющие"},
    {"text": "Неудача — это просто возможность начать снова, но уже более мудро.", "author": "Генри Форд", "category": "Мотивационные"},
    {"text": "Искусство быть собой — это самое трудное искусство всех на свете.", "author": "Оскар Уайльд", "category": "Философские"},
    {"text": "Единственный способ делать отличную работу — любить то, что ты делаешь.", "author": "Стив Джобс", "category": "Мотивационные"},
    {"text": "Не бойтесь больших изменений. Бойтесь оставаться на месте.", "author": "Макс Фрай", "category": "Мотивационные"},
    {"text": "Только тот, кто рискнет ошибиться, может достичь великого.", "author": "Джон С. Максвелл", "category": "Мотивационные"},
    {"text": "Будьте изменением, которое вы хотели бы видеть в мире.", "author": "Махатма Ганди", "category": "Вдохновляющие"},
    {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", "author": "Стив Джобс", "category": "Мотивационные"},
    {"text": "Большая часть успеха приходит тем, кто находит удовольствие в том, что делает.", "author": "Элберт Хаббард", "category": "Мотивационные"},
    {"text": "Без силы воли нет характера.", "author": "Наполеон Хилл", "category": "Мотивационные"},
    {"text": "Лучший способ предсказать будущее — его изобрести.", "author": "Алан Кей", "category": "Мотивационные"},
    {"text": "Только те, кто рискуют пойти слишком далеко, могут узнать, насколько далеко можно зайти.", "author": "Т. С. Элиот", "category": "Мотивационные"},
    {"text": "Неважно, сколько раз ты упал — важно, сколько раз ты встал.", "author": "Кит Лук", "category": "Мотивационные"},
    {"text": "Секрет успеха — это знание того, как использовать время.", "author": "Артур Шопенгауэр", "category": "Мотивационные"},
    {"text": "Самый лучший способ предсказать будущее — это его создать.", "author": "Питер Друкер", "category": "Мотивационные"},
    {"text": "Сложнее всего начать действовать, все остальное зависит только от упорства.", "author": "Амелия Эрхарт", "category": "Мотивационные"},
    {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "category": "Мотивационные"},
    {"text": "Твоя работа — это та часть жизни, которая не является твоим отдыхом.", "author": "Джей Кей", "category": "Мотивационные"},
    {"text": "Будущее зависит от того, что вы делаете сегодня.", "author": "Махатма Ганди", "category": "Мотивационные"},
    {"text": "По ту сторону терпения — награда.", "author": "Дж. Б. Пристли", "category": "Вдохновляющие"},
    {"text": "Будь сегодня лучше, чем вчера.", "author": "Уоррен Баффет", "category": "Мотивационные"},
    {"text": "Самая трудная часть — это решение начать.", "author": "Амелия Эрхарт", "category": "Мотивационные"},
    {"text": "Если вы делаете то, что вам нравится, вам не придется работать ни одного дня в своей жизни.", "author": "Конфуций", "category": "Мотивационные"},
    {"text": "Секрет в том, чтобы начать.", "author": "Марк Твен", "category": "Мотивационные"},
    {"text": "Делай сегодня то, что другие не хотят, завтра будешь жить так, как другие не могут.", "author": "Джерри Райс", "category": "Мотивационные"},
    {"text": "Нельзя сделать ничего полезного, не попробовав.", "author": "Фрэнклин Рузвельт", "category": "Мотивационные"},
    {"text": "Делай то, что ты можешь, с тем, что у тебя есть, там, где ты находишься.", "author": "Теодор Рузвельт", "category": "Мотивационные"},
    {"text": "Не обращайте внимания на тех, кто говорит, что что-то невозможно сделать. Это просто ограничения их собственного мышления.", "author": "Эйнштейн", "category": "Мотивационные"},
    {"text": "Лучший способ предсказать будущее — это его изобрести.", "author": "Алан Кей", "category": "Мотивационные"},
    {"text": "Только те, кто рискуют пойти слишком далеко, могут узнать, насколько далеко можно зайти.", "author": "Т. С. Элиот", "category": "Мотивационные"},
    {"text": "Неважно, сколько раз ты упал — важно, сколько раз ты встал.", "author": "Кит Лук", "category": "Мотивационные"},
    {"text": "Секрет успеха — это знание того, как использовать время.", "author": "Артур Шопенгауэр", "category": "Мотивационные"},
    {"text": "Самый лучший способ предсказать будущее — это его создать.", "author": "Питер Друкер", "category": "Мотивационные"},
    {"text": "Сложнее всего начать действовать, все остальное зависит только от упорства.", "author": "Амелия Эрхарт", "category": "Мотивационные"},
    {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "category": "Мотивационные"},
    {"text": "Твоя работа — это та часть жизни, которая не является твоим отдыхом.", "author": "Джей Кей", "category": "Мотивационные"}
    # Добавьте еще цитаты и категории
]

# Список сохраненных цитат пользователя
favorite_quotes = []

@app.route('/')
def index():
    # Получение случайной цитаты
    random_quote = random.choice(quotes_db)
    return render_template('index.html', quote=random_quote, quotes_db=quotes_db, favorite_quotes=favorite_quotes)

@app.route('/get_new_quote')
def get_new_quote():
    # Получение новой случайной цитаты при клике на кнопку
    random_quote = random.choice(quotes_db)
    return render_template('index.html', quote=random_quote, quotes_db=quotes_db, favorite_quotes=favorite_quotes)

@app.route('/save_quote/<int:quote_index>')
def save_quote(quote_index):
    # Сохранение цитаты в персональный список (используя Cookie)
    quote_to_save = quotes_db[quote_index]
    favorite_quotes.append(quote_to_save)
    
    # Создание и установка Cookie с сохраненными цитатами
    response = make_response(redirect(url_for('index')))
    response.set_cookie('favorite_quotes', str(favorite_quotes))
    
    return response

# Внесите изменения в функцию search() в файле app.py
@app.route('/search')
def search():
    # Функция поиска цитат по ключевым словам, авторам или категориям
    query = request.args.get('query') or ""
    category = request.args.get('category')

    if category:
        results = [quote for quote in quotes_db if query.lower() in quote['text'].lower() and category.lower() == quote['category'].lower()]
        category_msg = f" категория: {category}"
    else:
        results = [quote for quote in quotes_db if query.lower() in quote['text'].lower() or query.lower() in quote['author'].lower()]
        category_msg = ""

    categories = list(set(quote['category'] for quote in quotes_db))  # Получение уникальных категорий

    return render_template('search.html', query=query, results=results, categories=categories, category_msg=category_msg)

# Добавьте новый маршрут и функцию для удаления цитаты из списка сохраненных
@app.route('/remove_favorite/<int:quote_index>')
def remove_favorite(quote_index):
    # Удаление цитаты из списка сохраненных
    if 0 <= quote_index < len(favorite_quotes):
        del favorite_quotes[quote_index]

        # Обновление Cookie с сохраненными цитатами
        response = make_response(redirect(url_for('index')))
        response.set_cookie('favorite_quotes', str(favorite_quotes))
        return response

    return "Invalid Quote Index"


if __name__ == '__main__':
    app.run(debug=True)