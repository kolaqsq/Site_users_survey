let count = 0

function addSection() {
    let section = document.createElement("div");
    section.className = "edit-section";
    section.innerHTML = '<div class="edit-section__top-bar">\n' +
        '                        <span class="edit-section__header">Новая секция</span>\n' +
        '                        <svg class="edit-section__icon" width="24" height="24" viewBox="0 0 24 24" fill="none"\n' +
        '                             xmlns="http://www.w3.org/2000/svg">\n' +
        '                            <path fill-rule="evenodd" clip-rule="evenodd"\n' +
        '                                  d="M12 0C5.37273 0 0 5.37273 0 12C0 18.6273 5.37273 24 12 24C18.6273 24 24 18.6273 24 12C24 5.37273 18.6273 0 12 0ZM7.63636 10.9091C7.34704 10.9091 7.06956 11.024 6.86497 11.2286C6.66039 11.4332 6.54545 11.7107 6.54545 12C6.54545 12.2893 6.66039 12.5668 6.86497 12.7714C7.06956 12.976 7.34704 13.0909 7.63636 13.0909H16.3636C16.653 13.0909 16.9304 12.976 17.135 12.7714C17.3396 12.5668 17.4545 12.2893 17.4545 12C17.4545 11.7107 17.3396 11.4332 17.135 11.2286C16.9304 11.024 16.653 10.9091 16.3636 10.9091H7.63636Z"\n' +
        '                                  fill="#F8D4D4"></path>\n' +
        '                        </svg>\n' +
        '                    </div>\n' +
        '                    <div class="edit-section__line">\n' +
        '                        <label class="edit-section__label" for="section-title-' + count + '">Название:</label>\n' +
        '                        <input class="edit-section__input" type="text" name="section-title-' + count + '" id="section-title-' + count + '"\n' +
        '                               maxlength="200"\n' +
        '                               required>\n' +
        '                    </div>\n' +
        '                    <div class="edit-section__line edit-section__line_vertical">\n' +
        '                        <label class="edit-section__label" for="section-desc-' + count + '">Описание:</label>\n' +
        '                        <textarea class="edit-section__textarea" id="section-desc-' + count + '" name="section-desc-' + count + '"\n' +
        '                                  maxlength="1000"></textarea>\n' +
        '                    </div>\n' +
        '                    <div class="edit-section__line edit-section__line_vertical" id="questions-container-' + count + '">\n' +
        '                        <span class="edit-section__label">Вопросы:</span>\n' +
        '                        <button class="edit-section__button" onclick="addQuestion(\'questions-container-' + count + '\')" id="section-button-' + count + '" type="button">Добавить вопрос</button>\n' +
        '                    </div>\n';
    const container = document.getElementById('sections-container')
    container.insertBefore(section, container.lastElementChild)
    count++
}

function addQuestion(container_id) {
    var question = document.createElement("div");
    question.className = "edit-question";
    question.innerHTML = '<div class="edit-question__top-bar">\n' +
        '                        <span class="edit-question__header">Новый вопрос</span>\n' +
        '                        <svg class="edit-question__icon" width="24" height="24" viewBox="0 0 24 24" fill="none"\n' +
        '                             xmlns="http://www.w3.org/2000/svg">\n' +
        '                            <path fill-rule="evenodd" clip-rule="evenodd"\n' +
        '                                  d="M12 0C5.37273 0 0 5.37273 0 12C0 18.6273 5.37273 24 12 24C18.6273 24 24 18.6273 24 12C24 5.37273 18.6273 0 12 0ZM7.63636 10.9091C7.34704 10.9091 7.06956 11.024 6.86497 11.2286C6.66039 11.4332 6.54545 11.7107 6.54545 12C6.54545 12.2893 6.66039 12.5668 6.86497 12.7714C7.06956 12.976 7.34704 13.0909 7.63636 13.0909H16.3636C16.653 13.0909 16.9304 12.976 17.135 12.7714C17.3396 12.5668 17.4545 12.2893 17.4545 12C17.4545 11.7107 17.3396 11.4332 17.135 11.2286C16.9304 11.024 16.653 10.9091 16.3636 10.9091H7.63636Z"\n' +
        '                                  fill="#F8D4D4"></path>\n' +
        '                        </svg>\n' +
        '                    </div>\n' +
        '                    <div class="edit-question__line">\n' +
        '                        <label class="edit-question__label" for="question-title-' + count + '">Название:</label>\n' +
        '                        <input class="edit-question__input" type="text" name="question-title-' + count + '" id="question-title-' + count + '"\n' +
        '                               maxlength="200"\n' +
        '                               required>\n' +
        '                    </div>\n' +
        '                    <div class="edit-question__line">\n' +
        '                        <label class="edit-question__label" for="question-type-' + count + '">Тип вопроса:</label>\n' +
        '                        <select name="question-type-' + count + '" id="question-type-' + count + '" class="edit-question__select" required>\n' +
        '                            {% for type in types %}\n' +
        '                                <option value="{{ type.id }}" class="edit-question__option">{{ type.name }}</option>\n' +
        '                            {% endfor %}\n' +
        '                        </select>\n' +
        '                    </div>\n' +
        '                    <div class="edit-question__line edit-question__line_vertical">\n' +
        '                        <label class="edit-question__label" for="question-question-' + count + '">Вопрос:</label>\n' +
        '                        <textarea class="edit-question__textarea" id="question-question-' + count + '" name="question-question-' + count + '"\n' +
        '                                  maxlength="1000" required></textarea>\n' +
        '                    </div>\n' +
        '                    <div class="edit-question__line edit-question__line_vertical">\n' +
        '                        <label class="edit-question__label" for="question-choices-' + count + '">Варианты ответа:</label>\n' +
        '                        <textarea class="edit-question__textarea" id="question-choices-' + count + '" name="question-choices-' + count + '"\n' +
        '                                  maxlength="1000"></textarea>\n' +
        '                        <span class="edit-question__hint">Каждый вариант ответа вводить с новой строки<br>\n' +
        '                            Оставить поле пустым, если выбран тип ответа в свободной форме</span>\n' +
        '                    </div>';
    const container = document.getElementById(container_id)
    container.insertBefore(question, container.lastElementChild)
    count++
}