import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import psycopg2

conn = psycopg2.connect(dbname=f"novosti", user="postgres", password="postgres", host="localhost", port="5432")


#access_token = '436f7621b86b28171790471a9103459f890ec533adb66fe1a5c324a203a129ead6d5d9db007376f87c629'
access_token = 'vk1.a.MFFJ03OM-J26X1D5owObrD1hi3Hc8KmYX73dw-K2fmuT1HRfp139Tacju7xVRxJ_7EVVETjljea0wRSeoPDSMq_vMLeS4NWCXb9v_CD9x13TyJQWpkjzrNPSM7g7KEC6Scub4m55C9--8riiyUTl_-nOA7uaTBTjXaPklGoGBzr6-dvF_kGw2uw7k8RT24Zl'
session = vk_api.VkApi(token=access_token)
api = session.get_api()


def send_message(user_id, message, **kwargs):
    try:
        api.messages.send(
            user_id=user_id,
            message=message,
            random_id=0,
            **kwargs
        )
    except:
        send_message(user_id, message, **kwargs)


for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id
        print(user_id, text)
        cur = conn.cursor()
        if text == "start" or text=='начать':
            keyboard = VkKeyboard()
            #keyboard.add_location_button()
            #keyboard.add_line()

            btn = "выкл"
            cur.execute('update status_bool set status=True')
            conn.commit()
            #button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.NEGATIVE,
             #                   VkKeyboardColor.SECONDARY, VkKeyboardColor.POSITIVE]
#            print(zip(buttons, button_colors))

            keyboard.add_button(btn)

            send_message(user_id=user_id, message="Если вы хотите начать роботу, нажмите кнопку вкл, если же хотите остановить работу нажмите кнопку выкл", keyboard=keyboard.get_keyboard())
        elif text == "вкл":
            keyboard = VkKeyboard()
            cur.execute('update status_bool set status=True')
            conn.commit()
            keyboard.add_button('выкл')
            send_message(user_id=user_id, message="вкл", keyboard=keyboard.get_keyboard())

        elif text == "выкл":
            keyboard = VkKeyboard()
            cur.execute('update status_bool set status=False')
            conn.commit()
            keyboard.add_button('вкл')
            send_message(user_id=user_id, message="выкл", keyboard=keyboard.get_keyboard())
        cur.close()
conn.close()
