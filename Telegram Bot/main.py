import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Bot Name : Insta Downloader
# Developed by : Jagadish

header = {
            "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }

def start_command(update, context):
    context.bot.send_message(chat_id = update.message.chat_id,text = f"Hello {update.effective_user.first_name}! \nI'm here to download instagram image apart from private accounts")
    context.bot.send_message(chat_id = update.message.chat_id, text = "Send me only instagram image link")


def imageDownload(update, context):
    url = update.message.text

    if 'https://www.instagram.com/' not in url:
        context.bot.send_message(chat_id = update.message.chat_id, text = "It may not be instagram link !\nCheck once again and send me")
        return

    response = requests.get(url, headers = header)

    if not response.ok:
        context.bot.send_message(chat_id = update.message.chat_id, text = "Server error! Please try again !")
        return

    soup = BeautifulSoup(response.text,'html.parser')

    img_url = None
    for tag in soup.find_all("meta"):
        if tag.get("property", None) == 'og:image':
            img_url = tag.get('content', None)

    if img_url is None:
        context.bot.send_message(chat_id = update.message.chat_id,
                                    text = "Image is not obtained! Please try again!")
        return

    context.bot.send_photo(chat_id = update.message.chat_id, photo = img_url)



## handling unexpected input from user
def no_text_handling(update, context):
    update.effective_message.reply_text("Only texts allowed !")
    start_command(update, context)


def main():
    
    ## Replace this api_token with yours
    api_token = API_TOKEN
    updater = Updater(api_token, use_context = True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start",start_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,imageDownload))
    dispatcher.add_handler(MessageHandler(Filters.all,no_text_handling))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()