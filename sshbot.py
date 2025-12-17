# Author: Nathan
# Thanks to : x9
# Date: 15 Feb 2024
# Decrypt : SSH ( HTTP CUSTOM )
##############################################

import telepot
import telepot.loop
from telepot.loop import MessageLoop
import time

# =====================================================
# 🔥 PARCHE DEFINITIVO PARA TELEPOT (NO CRASHEA)
# =====================================================
_original_extract = telepot.loop._extract_message

def _patched_extract_message(update):
    # Ignorar updates que rompen Telepot
    if 'my_chat_member' in update:
        return None, None
    return _original_extract(update)

telepot.loop._extract_message = _patched_extract_message
# =====================================================


# =====================================================
# 🔐 FUNCIÓN DE DECRYPT ORIGINAL (NO TOCADA)
# =====================================================
def dec_ssh(ld):
    userlv = [i for i in ld.split('.')][::2]
    userld = [i for i in ld.split('.')][1::2]
    newld = ""
    for x in range(len(userld)):
        v = int(userlv[x]) - len(userlv)
        w = int(userld[x]) - len(userlv)
        m = (v // (2 ** w)) % 256
        newld += chr(m)
    return newld
# =====================================================


def handle(msg):
    # Ignorar basura / updates vacíos
    if not msg or 'text' not in msg:
        return

    chat_id = msg['chat']['id']
    command = msg['text']

    if command.startswith('/start'):
        bot.sendMessage(
            chat_id,
            "Welcome to SSH Decryptor Bot!\n\n"
            "Use:\n"
            "/ssh server:port@user:password\n\n"
            "Example:\n"
            "/ssh ghoib.yassvpn.my.id:80@1816222515.26..."
        )

    elif command.startswith('/ssh'):
        try:
            encrypted_data = command.split(' ', 1)[1]

            server = encrypted_data.split('@')[0].split(':')[0]
            port = encrypted_data.split('@')[0].split(':')[1]

            user_enc = encrypted_data.split('@')[1].split(':')[0]
            pass_enc = encrypted_data.split('@')[1].split(':')[1]

            user = dec_ssh(user_enc)
            passwd = dec_ssh(pass_enc)

            response = (
                "╭──────────────────────\n"
                "│ SSH Decryptor\n"
                "├──────────────────────\n"
                f"├ Server   : {server}\n"
                f"├ Port     : {port}\n"
                f"├ Username : {user}\n"
                f"├ Password : {passwd}\n"
                "╰──────────────────────"
            )

            bot.sendMessage(chat_id, response)

        except Exception:
            bot.sendMessage(chat_id, "❌ Invalid SSH format")


# =====================================================
# 🔑 PON AQUÍ TU TOKEN
# =====================================================
bot = telepot.Bot("8439536914:AAEvaCXGJZwckZoWijejfO0o1zxaNkOePW8")

MessageLoop(bot, handle).run_as_thread()

print("Bot Activate by Nathan")

while True:
    time.sleep(10)
