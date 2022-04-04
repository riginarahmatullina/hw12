import logging

from flask import Blueprint, request, render_template

from functions import load_posts, uploads_posts

loader_blueprint = Blueprint('loader', __name__, url_prefix='/post', static_folder='static', template_folder='templates')

@loader_blueprint.route('/form/')
def forma():
    return render_template('post_form.html')


@loader_blueprint.route('/upload/', methods=["POST"])
def upload():
    try:
        file = request.files['picture']
        filename = file.filename
        content = request.values['content']
        posts = load_posts()
        posts.append({
            'pic': f'/uploads/images/{filename}',
            'content': content
        })
        uploads_posts(posts)
        file.save(f'uploads/images/{filename}')
        if filename.split('.')[-1] not in ['png', 'jpeg', 'jpg']:
            logging.info('Загружаемый файл не изображние')
            return "<h1> Загружаемый файл не изображние </h1>"
    except FileNotFoundError:
        logging.error('Ошибка при загрузке файла')
        return "<h1> Файл не найден </h1>"
    else:
        return render_template('post_uploaded.html', pic=f'/uploads/images/{filename}', content=content)
