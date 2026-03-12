# ⚡ Energy Bot - Умный помощник для выбора энергетика

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![PyTelegramBotAPI](https://img.shields.io/badge/PyTelegramBotAPI-4.x-blue)](https://pytba.readthedocs.io/ru/latest/index.html)
[![Transformers](https://img.shields.io/badge/Transformers-4.36+-green)](https://huggingface.co/docs/transformers/index)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-red)](https://pytorch.org/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-purple)](https://openrouter.ai/)
[![YooMoney](https://img.shields.io/badge/YooMoney-API-yellow)](https://yoomoney.ru/)
[![Git](https://img.shields.io/badge/Git-version--control-red)](https://git-scm.com/)
[![GitHub](https://img.shields.io/badge/GitHub-repository-black)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 📸 Демонстрация работы

### Главное меню бота
![Главное меню бота](https://sun9-43.userapi.com/s/v1/ig2/ZhPCPoxOGTfCbhPXnQbYn-ZaLBYwMEt6G7DUB8u_gJhZXSfRhbINoTiGh8_6dwooKraeqcM-lrZ4OkCHO1l24y1N.jpg?quality=95&as=32x7,48x10,72x16,108x23,160x35,240x52,360x78,480x104,540x117,640x139,720x156,1080x234,1222x265&from=bu&cs=1222x0)
*Главное меню с кнопками: Энергос, Корзина, Консультант*

### Пример анализа комментария
![Анализ комментария](assets/sentiment_analysis.png)
*Определение токсичности комментария с помощью модели трансформера*

### Пример рекомендации энергетика
![Рекомендация](assets/recommendation.png)
*Консультация по энергетикам через OpenRouter AI*

**Energy Bot** — это командный проект, представляющий собой многофункционального Telegram-бота для заказа энергетических напитков. Бот умеет анализировать комментарии на токсичность с помощью модели трансформера, давать консультации через нейросеть и принимать оплату через ЮMoney.

## 🚀 Функциональность

*   **🧠 Анализ токсичности (NLP):** Модель трансформера определяет наличие оскорблений, угроз и нецензурной брани в комментариях к заказу.
*   **🤖 AI-консультант:** Интеграция с OpenRouter API для получения бесплатных консультаций по энергетическим напиткам.
*   **🛒 Корзина и заказы:** Удобная система добавления товаров, корзина с возможностью удаления позиций.
*   **💳 Оплата через ЮMoney:** Интеграция с платежной системой YooMoney для приема оплаты.
*   **📦 Оформление заказов:** Сбор адреса доставки и комментария с автоматической проверкой токсичности.

## 🛠 Стек технологий

*   **Язык:** Python 3.13+
*   **Фреймворк для бота:** PyTelegramBotAPI (telebot)
*   **ML/NLP:** Transformers + PyTorch (модель классификации токсичности)
*   **AI-консультант:** OpenRouter API (бесплатные модели)
*   **Платежи:** YooMoney API
*   **Система контроля версий:** Git + GitHub

## 🤖 Использованные API и модели

### 1. API нейросети для консультаций

**Название API:** [OpenRouter API](https://openrouter.ai/)

**Описание:** OpenRouter — это унифицированный API, предоставляющий доступ к множеству языковых моделей (включая бесплатные). Позволяет использовать различные нейросети через единый интерфейс.

**Использование в проекте:**
```python
def ask_ai(prompt):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'openrouter/free',  # Бесплатная модель
        'messages': [
            {'role': 'user', 'content': f"Ты консультант по энергетикам. Коротко ответь на вопрос: {prompt}"}
        ],
        'max_tokens': 100,
        'temperature': 0.7
    }
    
    response = requests.post('https://openrouter.ai/api/v1/chat/completions', 
                            headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']
