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
![Анализ комментария](https://sun9-61.userapi.com/s/v1/ig2/gjiFezfdILRmQW6W59vT5dqscO5xbKkOSQH_n3x9HHlo0kWjvoo3gXDhrCGcM9d_dxat81lbzkgdQsLFk3hGo2C2.jpg?quality=95&as=32x27,48x41,72x61,108x92,160x136,240x205,360x307,480x409,540x460,611x521&from=bu&u=tpvDhN3VTJxz68tQle_9WLsy--zlTJ1a0XUzKF_pZ14&cs=611x0)
*Определение токсичности комментария с помощью модели трансформера*

### Пример рекомендации энергетика
![Рекомендация](https://sun9-67.userapi.com/s/v1/ig2/F3CE9WBAUg4w3KWPytZaO31e13y5_e2_9SVUV4WgCcN0Q5uZdWnE1IX-XVj3TxTpVpNX6bTLxmpYc5CQ7SG2nazZ.jpg?quality=95&as=32x14,48x20,72x31,108x46,160x68,240x103,360x154,480x205,540x231,640x273,720x308,1080x461,1222x522&from=bu&cs=1222x0)
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

### 1. API для AI-консультанта
**Название:** OpenRouter API  
**Описание:** API для доступа к языковым моделям. В проекте используется для создания консультанта по энергетикам.

### 2. Базовая модель ИИ
**Название:** deepseek

### 3. Модель трансформера
**Название:** Кастомная модель на базе RuBERT (`russian_text_classifier.pth`)  
**Задача:** Классификация текста - определение токсичности комментариев (оскорбления, угрозы, нецензурная брань)

## 🔄 Система контроля версий
- **Git** + **GitHub**
- Репозиторий: [https://github.com/kamilaA123/EmilKamila](https://github.com/kamilaA123/EmilKamila)
- Ветки: `main` (стабильная), `Kamila` (разработка), `Emil` (разработка)
