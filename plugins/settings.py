from pyrogram import emoji
from database import database
from pystark import Stark, Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Stark.cmd('settings', description='Configure personal bot settings.', private_only=True)
async def settings(_, msg: Message):
    text, markup = await user_settings(msg.from_user.id)
    await msg.react(text, reply_markup=markup)


async def user_settings(user_id):
    data = await database.get('users', user_id)
    if not data:
        return False, False
    tick = ' ✔'
    cross = ' ✖️ '
    ask_emojis = "Emoji isteyin"
    ask_emojis_msg = f"Botun pakete eklerken video etiketine ayarlanacak emojiler istemesini istiyorsanız True olarak ayarlayın. False olarak ayarlanırsa, tüm çıkartmalar varsayılan emojiyi kullanır - {emoji.RED_HEART}"
    get_webm = "Get WEBM"
    get_webm_msg = f"Mevcut herhangi bir video çıkartmasını gönderdiğinizde webm dosyalarını almak istiyorsanız True olarak ayarlayın. Bu şekilde, @Stickers kullanarak diğer kişilerin paketlerinden çıkartmalar ekleyebilirsiniz. False ise bot çıkartmayı yok sayar."
    kang_mode = "Kang Mode"
    kang_mode_msg = "Var olan bazı paketlerden bir video çıkartması göndererek paketinize çıkartmalar eklemek istiyorsanız True olarak ayarlayın. Bu şekilde, diğer kişilerin paketlerinden çıkartmaları paketinize ekleyebilirsiniz. False ise bot çıkartmayı yok sayar."
    default_emojis = "Varsayılan Emojiler"
    default_emojis_msg = f"Çıkartmalarınızda kullanılacak varsayılan emojileri ayarlayın. hiçbir şey ayarlanmamışsa, {emoji.RED_HEART} kullanılacak."
    text = f'**Settings** \n\n'
    ask_emojis_db = data['ask_emojis']
    get_webm_db = data['get_webm']
    kang_mode_db = data['kang_mode']
    default_emojis_db = data['default_emojis']
    general_text = "**{}** : {} \n{} \n\n"
    if ask_emojis_db:
        text += general_text.format(ask_emojis, 'True', ask_emojis_msg)
        ask_emojis += tick
    else:
        text += general_text.format(ask_emojis, 'False', ask_emojis_msg)
        ask_emojis += cross
    if get_webm_db:
        text += general_text.format(get_webm, 'True', get_webm_msg)
        get_webm += tick
    else:
        text += general_text.format(get_webm, 'False', get_webm_msg)
        get_webm += cross
    if kang_mode_db:
        text += general_text.format(kang_mode, 'True', kang_mode_msg)
        kang_mode += tick
    else:
        text += general_text.format(kang_mode, 'False', kang_mode_msg)
        kang_mode += cross
    if default_emojis_db:
        text += general_text.format(default_emojis, default_emojis_db, default_emojis_msg)
        default_emojis += ' - SET'
    else:
        text += general_text.format(default_emojis, 'Not Set', default_emojis_msg)
        default_emojis += ' - NOT SET'
    text += 'Use below buttons to change values. A tick means True and cross means False'
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(ask_emojis, callback_data="emojis")],
        [InlineKeyboardButton(default_emojis, callback_data="default_emojis")],
        [InlineKeyboardButton(kang_mode, callback_data="kang_mode")],
        [InlineKeyboardButton(get_webm, callback_data="webm")],
    ])
    return text, markup


async def default_emojis_settings(user_id):
    data = await database.get('users', user_id)
    if not data:
        return False, False
    data = data['default_emojis']
    if data:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Emojileri Değiştir', callback_data="change_default_emojis")],
            [InlineKeyboardButton('Varsayılan Emojileri Kaldır', callback_data="remove_default_emojis")],
            [InlineKeyboardButton('<-- Geri ', callback_data="back")],
        ])
        text = f'Geçerli Varsayılan Emojiler `{data}` \n\nBunları değiştirmek veya kaldırmak için aşağıdaki düğmeleri kullanın'
    else:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Emoji Ekle', callback_data="change_default_emojis")],
            [InlineKeyboardButton('<-- Geri', callback_data="back")],
        ])
        text = 'Şu anda hiçbir Emoji ayarlanmamış. Bunları eklemek için aşağıdaki düğmeyi kullanın.'
    return text, markup
