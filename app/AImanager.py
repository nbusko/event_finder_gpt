import os
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from db_utils import MongoDB
from openai import OpenAI


class AImanager:
    def __init__(self, path) -> None:
        self.api_key=os.getenv("API_KEY")
        self.client_gpt = OpenAI(
            api_key=self.api_key,
        )
        self.database = MongoDB(path)
            
    async def get_events_by_date_type(self, event_date, event_theme):
        result = self.database.get_events_by_date_type(event_date, event_theme)
        return result
        
    async def get_info(self, text):
        lines = text.lower().split(';')
        date = lines[0].replace('дата: ', '')
        theme = lines[1].replace('тематика: ', '')
        event_lst = await self.get_events_by_date_type(date, theme)
        return event_lst
    

    async def process(self, text: str):
        self.client_gpt = OpenAI(
            api_key=self.api_key,
        )

        input_task = f"ты русскоязычный ассистент. классифицируй этот запрос, сделанный к русскоязычному ассистенту: \"{text}\". Напиши, касается он посещения какого-то мероприятия, в ответ напиши только да или нет"

        chat_completion = self.client_gpt.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_task,
                }
            ],
            model="gpt-3.5-turbo",
        )
        output = chat_completion.choices[0].message.content

        if output == "нет":
            return "Ваш запрос не касается помощи в подборе мероприятий. Такие запросы не обрабатываются"
        input_task = f"\
            проанализируй этот запрос, сделанный к русскоязычному ассистенту: \"{text}\".\
            найди в этом запросе дату,\
            среди тематик: развлечение концерт музыка саундтрек детям концерт выставка история культура искусство кинематограф современная музыка школа экономика классическая музыка орган выставка культура панк панк-выставка спектакль мюзикл концерт кино рок хип-хоп рэп соревнование конкурс итмо конференция конгресс ниоктр фестиваль драма\
            определи, к какой из них относится запрос, предоставь ответ в таком виде:\
            дата: ДД/ММ/ГГГГ;тематика: максимально близкая тематика"
        
        self.client_gpt = OpenAI(
            api_key=self.api_key,
        )
        
        chat_completion = self.client_gpt.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_task,
                }
            ],
            model="gpt-3.5-turbo",
        )
        output = chat_completion.choices[0].message.content
        event_lst = await self.get_info(output)
        event_text = "есть список мероприятий:\n"
        for event in event_lst:
            row = f"Название: {event['name']} Тип мероприятия: {event['type']} Тема мероприятия: {event['theme']} Описание: {event['description']} Дата: {event['date']} Время: {event['time']} Адрес: {event['address']} Ссылка на мероприятие: {event['href']} \n"
            event_text+=row
        event_text+="Только среди этих мероприятий выбери максимально подходящие запросу по теме мероприятия и дате и выведи в виде списка указывая Название, Тип, Описание, Дату, Время, Адрес и Ссылку, как это указано в списке, выведи только список, больше ничего не пиши"
        self.client_gpt = OpenAI(
            api_key=self.api_key,
        )
        chat_completion = self.client_gpt.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": event_text,
                }
            ],
            model="gpt-3.5-turbo",
        )
        output = chat_completion.choices[0].message.content
        res = output+"\nВот, что мне удалось найти по вашему запросу!\nРад, если в этом списке вы найдете то, что вам понравится.\nОбязательно оставьте отзыв после посещения мероприятия!"
        return res