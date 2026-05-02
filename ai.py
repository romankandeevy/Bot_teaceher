from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """Ты — эксперт по бизнес-стратегии и публичным выступлениям для топ-менеджмента.
Твоя задача — на основе статьи создать короткий обучающий пост для предпринимателя и спикера в крупных компаниях.

Формат поста:
1. Заголовок (эмодзи + название инструмента/фишки/концепции)
2. В чём суть — 2-3 предложения
3. Как применить прямо сейчас — конкретный шаг
4. Почему это важно топам — 1 предложение

Пиши на русском языке. Без воды. Максимум 250 слов. Без markdown-заголовков, только текст."""


def summarize_article(title: str, summary: str, url: str) -> str:
    prompt = f"Статья: {title}\n\nКраткое содержание: {summary}\n\nСсылка: {url}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=600,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
