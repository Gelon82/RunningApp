from turtledemo.penrose import start
from urllib.request import parse_http_list

from charset_normalizer.cli import query_yes_no
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будем писать наш код :)
async def start (update, context):
    await show_main_menu(update, context,{
        "start": "главное меню бота",
        "profile": "генерация Tinder-профля 😎",
        "opener":"сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠"
    })
    dialog.mode="main"
    text=load_message("main")
    await send_text(update, context, text)
    await send_photo(update, context, "main")

async def gpt (update, context):
    dialog.mode = "gpt"
    text=load_message("gpt")
    await send_text(update, context, text)
    await send_photo(update, context, "gpt")

async def gpt_dialog(update, context):
    text=update.message.text
    pr=load_prompt("gpt")
    ans=await chatGpt.send_question(pr,text)
    await send_text(update, context, "Welcome to GPT Chat "+ans)

async def hi(update,context):
    if dialog.mode=="gpt":
        await gpt_dialog(update,context)
    if dialog.mode=="date":
        await date_dialog(update, context)
    if dialog.mode=="message":
        await message_dialog(update, context)

    else:
        await send_text(update,context,"*Привет!*")
        await send_text(update, context, "_Как дела?_")
        await send_text(update, context, "Вы написали: "+update.message.text)
        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Запустить процесс?",buttons={
            "start":"запустить",
            "stop":"остановить"
        })

async def date (update, context):
    dialog.mode = "date"
    text=load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {"date_grande": "Ариана Гранде",
                                                    "date_robbie": "Марго Робби",
                                                    "date_zendaya": "Зендея",
                                                    "date_gosling": "Райан Гослинг",
                                                    "date_hardy": "Том Харди"
                                                    })

async def date_dialog(update, context):
    text=update.message.text
    mym=await send_text(update, context,"дедушка набирает текст.. ")
    answer=await  chatGpt.add_message(text)
    await mym.edit_text(answer)
    await send_text(update, context,answer)

async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context,query)
    await send_html(update, context, "key press " + query)
    prompt = load_prompt(query)
    chatGpt.set_prompt(prompt)

async def message (update, context):
    dialog.mode = "message"
    text=load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons(update, context, text,{"message_next":"отпр сообщ","message_date":"пригласить на свидание "})
    dialog.list.clear()
async def message_dialog(update, context):
    text=update.message.text
    dialog.list.append(text)

    #mym=await send_text(update, context,"дедушка набирает текст.. ")
    #answer=await  chatGpt.add_message(text)
    #await mym.edit_text(answer)
    #await send_text(update, context,answer)

async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    prompt = load_prompt(query)
    user_chat_hist="\n\n".join(dialog.list)
    mym = await send_text(update, context, "дедушка думает набирает текст.. ")
    answer=await chatGpt.send_question(prompt,user_chat_hist)
    await mym.edit_text(answer)
    #await send_text(update,context,answer)

    #await send_photo(update, context,query)
    #await send_html(update, context, "key press " + query)



async def hi_button(update, context):
    query=update.callback_query.data
    if query=="start":
        await send_text(update, context, "_srted_")
    else:
        await send_text(update, context, "_stoped_")
dialog=Dialog()
dialog.mode=None
dialog.list=[]
chatGpt=ChatGptService(token="gpt:A03NYofv3ubgIx6f1SXnPAKmBZ0E9dS9Qcn2T2Zi1nOgo_QvJ0z8W5cWFvJFkblB3TavDiNT25x1--mRNrTISss9Vj3Q6lCoImv5cXw51H8RE70DG7rsRaf4bEE4")
app = ApplicationBuilder().token("7729544877:AAF1QzOvLfBL2MYRBEKvtlZIt-RZbi2p8gI").build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("gpt",gpt))
app.add_handler(CommandHandler("date",date))
app.add_handler(CommandHandler("message",message))
app.add_handler(CallbackQueryHandler(date_button,pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button,pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hi_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,hi))
app.run_polling()
