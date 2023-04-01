import telebot
import psycopg2
from psycopg2.extras import DictCursor
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import logging

telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot('6176147461:AAHlfAvtHsoPW_1GWRT6bKVZXm0CMD5Trfo')

conn = psycopg2.connect(
    host="127.0.0.1",
    database="movies",
    user="postgres",
    password="Aegis1885"
)

CHECK_MARK = u'\U00002705'  # ✅
CROSS_MARK = u'\U0000274C'  # ❌

cur = conn.cursor(cursor_factory=DictCursor)


def keyboard(key_type="main"):
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    if key_type == "main":
        markup.add("Add new", "Show movies")
    elif key_type == "all":
        markup.add("👀 All", "✅ Watched", "❌ Unwatched")
        markup.add("🍥 Anime", "👶🏻 Cartoons", "🧝‍ Fantasy")
        markup.add("👻 Horrors", "☠️Thrillers/Drama", "🎭 Tragicomedy")
        markup.add("⚔️ Historical", "🦵 Art House", "👨‍👨‍👧 Family friendly")
        markup.add("🦸‍ Fiction", "🤡 Comedies/trash", "🎮 Games")
        markup.add("🔙 Back")
    elif key_type == 'boolean':
        markup.add("true", "false")
    elif key_type == 'genres':
        markup.add("🍥 Anime", "👶🏻 Cartoons", "🧝‍ Fantasy")
        markup.add("👻 Horrors", "☠️Thrillers/Drama", "🎭 Tragicomedy")
        markup.add("⚔️ Historical", "🦵 Art House", "👨‍👨‍👧 Family friendly")
        markup.add("🦸‍ Fiction", "🤡 Comedies/trash", "🎮 Games")
    return markup


def keyboard_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Mark as watched", callback_data="cb_watched"))
    return markup


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "SHTO TI HOCHESH???", reply_markup=keyboard('main'))


@bot.message_handler(func=lambda message: True)
def all_messages(message):
    if message.text == "Add new":
        markup = telebot.types.ReplyKeyboardRemove()
        alina_user_id = 816784996
        ya_user_id = 622066887
        if message.chat.id == ya_user_id or message.chat.id == alina_user_id:
            bot.send_message(message.chat.id, "Enter the following movie details: ", reply_markup=markup)
            msg = bot.reply_to(message, "\n\n1. Movie name: ")
            bot.register_next_step_handler(msg, process_movie_name_step)
        else:
            bot.send_message(message.chat.id, "Tebe syuda nelzya")
    elif message.text == "Show movies":
        bot.send_message(message.chat.id, "vot genri:", reply_markup=keyboard('all'))
    elif message.text == "🔙 Back":
        bot.send_message(message.chat.id, "SHO TI HOCHESH???", reply_markup=keyboard('main'))

    if message.text == "✅ Watched":
        cur.execute("SELECT * FROM movies_2 WHERE status = TRUE order by movie_id")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        first_half_result = "\n".join(result_list[:len(result_list) // 4])
        second_half_result = "\n".join(result_list[len(result_list) // 4: len(result_list) // 2])
        third_half_result = "\n".join(result_list[len(result_list) // 2: 3 * len(result_list) // 4])
        fourth_half_result = "\n".join(result_list[3 * len(result_list) // 4:])

        bot.send_message(message.chat.id, first_half_result)
        bot.send_message(message.chat.id, second_half_result)
        bot.send_message(message.chat.id, third_half_result)
        bot.send_message(message.chat.id, fourth_half_result)

    elif message.text == "❌ Unwatched":
        cur.execute("SELECT * FROM movies_2 WHERE status = FALSE")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        first_half_result = "\n".join(result_list[:len(result_list) // 4])
        second_half_result = "\n".join(result_list[len(result_list) // 4: len(result_list) // 2])
        third_half_result = "\n".join(result_list[len(result_list) // 2: 3 * len(result_list) // 4])
        fourth_half_result = "\n".join(result_list[3 * len(result_list) // 4:])

        bot.send_message(message.chat.id, first_half_result)
        bot.send_message(message.chat.id, second_half_result)
        bot.send_message(message.chat.id, third_half_result)
        bot.send_message(message.chat.id, fourth_half_result)

    elif message.text == "👀 All":
        cur.execute("SELECT * FROM movies_2 order by movie_id")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        first_half_result = "\n".join(result_list[:len(result_list) // 4])
        second_half_result = "\n".join(result_list[len(result_list) // 4: len(result_list) // 2])
        third_half_result = "\n".join(result_list[len(result_list) // 2: 3 * len(result_list) // 4])
        fourth_half_result = "\n".join(result_list[3 * len(result_list) // 4:])

        bot.send_message(message.chat.id, first_half_result)
        bot.send_message(message.chat.id, second_half_result)
        bot.send_message(message.chat.id, third_half_result)
        bot.send_message(message.chat.id, fourth_half_result)


    elif message.text == "🧝‍ Fantasy":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '🧝‍ Fantasy' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "👻 Horrors":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '👻 Horrors' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "🍥 Anime":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '🍥 Anime' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "👶🏻 Cartoons":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '👶🏻 Cartoons' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "☠️Thrillers/Drama":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '☠️Thrillers/Drama' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "🎭 Tragicomedy":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '🎭 Tragicomedy' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "⚔️ Historical":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '⚔️Historical' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "🦵 Art House":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '🦵 Art House' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "👨‍👨‍👧 Family friendly":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '👨‍👨‍👧 Family friendly' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "🦸‍ Fiction":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '🦸‍ Fiction' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "🤡 Comedies/trash":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '🤡 Comedies/trash' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK

            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())

    elif message.text == "🎮 Games":
        cur.execute("SELECT * FROM movies_2 WHERE movie_genre = '🎮 Games' order by movie_name")
        rows = cur.fetchall()
        result_list = []
        for row in rows:
            if row['status'] == True:
                status = CHECK_MARK
            else:
                status = CROSS_MARK
            if f"{row['comments']}" == '' or f"{row['comments']}" is None:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']}"
                result_list.append(row_str)
            else:
                row_str = f"{status} | {row['movie_name']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
                result_list.append(row_str)

        result = "\n".join(result_list)

        bot.send_message(message.chat.id, result, reply_markup=keyboard_inline())


input_list = []


def process_movie_name_step(message):
    input_list.append(message.text)
    msg = bot.send_message(message.chat.id, "\n\n2. Movie genre: ", reply_markup=keyboard('genres'))
    bot.register_next_step_handler(msg, process_movie_genre_step)


def process_movie_genre_step(message):
    input_list.append(message.text)
    markup = telebot.types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, "\n\n3. Alevtina's rate: ", reply_markup=markup)
    bot.register_next_step_handler(msg, process_ratings_a_step)


def process_ratings_a_step(message):
    input_list.append(float(message.text))
    msg = bot.send_message(message.chat.id, "\n\n4. Volodya's rate: ")
    bot.register_next_step_handler(msg, process_ratings_v_step)


def process_ratings_v_step(message):
    input_list.append(message.text)
    msg = bot.send_message(message.chat.id, "\n\n5. Status: ", reply_markup=keyboard('boolean'))
    bot.register_next_step_handler(msg, process_status_step)


def process_status_step(message):
    if message.text == "true" or message.text == "false":
        input_list.append(bool(message.text))
    else:
        bot.send_message(message.chat.id, 'dolbaebina')
        return
    markup = telebot.types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, "\n\n6. Any comments? ", reply_markup=markup)
    bot.register_next_step_handler(msg, process_comments_step)


def process_comments_step(message):
    if message.text.lower() == "skip" or message.text.lower() == "скип":
        pass
    else:
        input_list.append(message.text)
    print(input_list)
    if len(input_list) == 5:
        sql = "INSERT INTO movies_2 (movie_name, movie_genre, ratings_a, ratings_v, status)" \
              f"VALUES ('{input_list[0]}', '{input_list[1]}', '{input_list[2]}', '{input_list[3]}', '{input_list[4]}')"
        cur.execute(sql)
    elif len(input_list) == 6:
        sql = "INSERT INTO movies_2 (movie_name, movie_genre, ratings_a, ratings_v, status, comments)" \
              f"VALUES ('{input_list[0]}', '{input_list[1]}', '{input_list[2]}', '{input_list[3]}', '{input_list[4]}', '{input_list[5]}')"
        cur.execute(sql)
    conn.commit()
    input_list.clear()
    bot.send_message(message.chat.id, "Movie was successfully added! 😼", reply_markup=keyboard('main'))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_watched":
        bot.answer_callback_query(call.id, "Let's go!")
        msg = bot.send_message(call.message.chat.id, "Which movie did you watch?",
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_name_update)
        print("callbackquery proshel")


update_list = []


def process_name_update(message):
    update_list.append(message.text)
    msg = bot.send_message(message.chat.id, "Alevtina's rate?", parse_mode=None)
    bot.register_next_step_handler(msg, process_arate_update)


def process_arate_update(message):
    update_list.append(float(message.text))
    msg = bot.send_message(message.chat.id, "Volodya's rate?")
    bot.register_next_step_handler(msg, process_vrate_update)


def process_vrate_update(message):
    update_list.append(float(message.text))
    msg = bot.send_message(message.chat.id, "Any comments?")
    bot.register_next_step_handler(msg, process_comments_update)


def process_comments_update(message):
    if message.text.lower() == "skip" or message.text.lower() == "скип":
        pass
    else:
        update_list.append(message.text)

    if len(update_list) == 3:
        sql = f"UPDATE movies_2 SET ratings_a = '{update_list[1]}', ratings_v = '{update_list[2]}', status = True WHERE movie_name = '{update_list[0]}'"
        cur.execute(sql)
    elif len(update_list) == 4:
        sql = f"UPDATE movies_2 SET ratings_a = '{update_list[1]}', ratings_v = '{update_list[2]}', status = True, comments = '{update_list[3]}' WHERE movie_name = '{update_list[0]}'"
        cur.execute(sql)
    conn.commit()
    bot.send_message(message.chat.id, "Movie was successfully updated! 😼", reply_markup=keyboard('main'))
    update_list.clear()


# def gen_markup():
#     markup = InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
#                                InlineKeyboardButton("No", callback_data="cb_no"))
#     return markup
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     if call.data == "cb_yes":
#         bot.answer_callback_query(call.id, "Yes huy sosi")
#     elif call.data == "cb_no":
#         bot.answer_callback_query(call.id, "No ne sosi")
#
# @bot.message_handler(func=lambda message: True)
# def message_handler(message):
#     bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())


# def send_watched(message):
#     cur.execute("SELECT * FROM movies_2 WHERE status = TRUE")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_unwatched(message):
#     cur.execute("SELECT * FROM movies_2 WHERE status = FALSE")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_all(message):
#     cur.execute("SELECT * FROM movies_2")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
#         result_list.append(row_str)
#
#     first_half_result = "\n".join(result_list[:len(result_list) // 2])
#     second_half_result = "\n".join(result_list[len(result_list) // 2:])
#     return first_half_result, second_half_result
#
#
# def send_fantasy(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Фэнтези' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_horrors(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Хорроры' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_anime(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Аниме' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_tragicomedy(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Трагикомедии' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_historical(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Исторические' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_cartoons(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Мультфильмы' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_trillerdrama(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'ТриллероДрамы' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     return result
#
#
# def send_genres(message):
#     cur.execute("SELECT DISTINCT movie_genre FROM movies_2 order by movie_genre ")
#     rows = cur.fetchall()
#     result = '\n'.join([f"{row['movie_genre']}" for row in rows])
#     return result
#
#
# input_list = []
#
#
# @bot.message_handler(commands=['add_movie'])
# def add_movie_name(message):
#     chat_id = message.chat.id
#     answer = bot.send_message(chat_id, "Enter the following movie details: \n\n1. Movie name: ")
#     bot.register_next_step_handler(answer, add_movie_genre)
#
#
# def add_movie_genre(message):
#     text = message.text
#     input_list.append(text)
#     answer = bot.send_message(message.chat.id, '\n2. Movie genre:')
#     bot.register_next_step_handler(answer, add_ratings_a)
#
#
# def add_ratings_a(message):
#     text = message.text
#     input_list.append(text)
#     answer = bot.send_message(message.chat.id, "\n3. Alevtina's Rate: ")
#     bot.register_next_step_handler(answer, add_ratings_v)
#
# def add_ratings_v(message):
#     text = message.text
#     input_list.append(text)
#     answer = bot.send_message(message.chat.id, "\n4. Volodya's Rate:")
#     bot.register_next_step_handler(answer, add_status)
#
# def add_status(message):
#     text = message.text
#     input_list.append(text)
#     answer = bot.send_message(message.chat.id, "\n5. Status: ")
#     bot.register_next_step_handler(answer, add_comments)
#
# def add_comments(message):
#     text = message.text
#     input_list.append(text)
#     answer = bot.send_message(message.chat.id, "\n6. Comments: ")
#     bot.register_next_step_handler(answer, add_to_table)
#     print(input_list)
# #     ТУТ ПИЗДА, КОММЕНТЫ НЕ ДОБАВЛЯЮТСЯ В ЛИСТ, РАЗБЕРИСЬ ЗАВТРА
#
# def add_to_table(message):
#     for elem in input_list:
#         bot.send_message(message.chat.id, elem)
#
#
#
# @bot.message_handler(commands=['show_all'])
# def handle_show_all(message):
#     bot.send_message(message.chat.id, send_all(message))
#
#
# @bot.message_handler(commands=['show_unwatched'])
# def handle_show_unwatched(message):
#     bot.send_message(message.chat.id, send_unwatched(message))
#
#
# @bot.message_handler(commands=['show_watched'])
# def handle_show_watched(message):
#     bot.send_message(message.chat.id, send_watched(message))
#
#
# @bot.message_handler(commands=['show_fantasy'])
# def handle_show_fantasy(message):
#     bot.send_message(message.chat.id, send_fantasy(message))
#
#
# @bot.message_handler(commands=['show_horrors'])
# def handle_show_horrors(message):
#     bot.send_message(message.chat.id, send_horrors(message))
#
#
# @bot.message_handler(commands=['show_anime'])
# def handle_show_anime(message):
#     bot.send_message(message.chat.id, send_anime(message))
#
#
# @bot.message_handler(commands=['show_tragicomedy'])
# def handle_show_tragicomedy(message):
#     bot.send_message(message.chat.id, send_tragicomedy(message))
#
#
# @bot.message_handler(commands=['show_historical'])
# def handle_show_historical(message):
#     bot.send_message(message.chat.id, send_historical(message))
#
#
# @bot.message_handler(commands=['show_cartoons'])
# def handle_show_cartoons(message):
#     bot.send_message(message.chat.id, send_cartoons(message))
#
#
# @bot.message_handler(commands=['show_trillerdrama'])
# def handle_show_trillerdrama(message):
#     bot.send_message(message.chat.id, send_trillerdrama(message))
#
#
# @bot.message_handler(commands=['show_genres'])
# def handle_show_genres(message):
#     bot.send_message(message.chat.id, send_genres(message))
#
#
# @bot.message_handler(func=lambda message: True)
# def handle_any_message(message):
#     bot.reply_to(message, "Please use the buttons to interact with me.", reply_markup=keyboard)


# @bot.message_handler(commands=['show_all'])
# def send_all(message):
#     cur.execute("SELECT * FROM movies_2")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']} | {row['comments']}"
#         result_list.append(row_str)
#
#     first_half_result = "\n".join(result_list[:len(result_list)//2])
#     second_half_result = "\n".join(result_list[len(result_list)//2:])
#     bot.send_message(message.chat.id, first_half_result)
#
#     bot.send_message(message.chat.id, second_half_result)

# @bot.message_handler(commands=['show_unwatched'])
# def send_unwatched(message):
#     cur.execute("SELECT * FROM movies_2 WHERE status = FALSE")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)


# @bot.message_handler(commands=['show_watched'])
# def send_watched(message):
#     cur.execute("SELECT * FROM movies_2 WHERE status = TRUE")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)


# @bot.message_handler(commands=['show_fantasy'])
# def send_watched(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Фэнтези' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)
#
#
# @bot.message_handler(commands=['show_horrors'])
# def send_horrors(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Хорроры' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)
#
#
#
# @bot.message_handler(commands=['show_anime'])
# def send_anime(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Аниме' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)
#
#
# @bot.message_handler(commands=['show_tragicomedy'])
# def send_tragicomedy(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Трагикомедии' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)
#
#
#
# @bot.message_handler(commands=['show_historical'])
# def send_historical(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Исторические' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)
#
# @bot.message_handler(commands=['show_cartoons'])
# def send_cartoons(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'Мультфильмы' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)
#
#
# @bot.message_handler(commands=['show_trillerdrama'])
# def send_trillerdrama(message):
#     cur.execute("SELECT * FROM movies_2 WHERE movie_genre = 'ТриллероДрамы' order by movie_name")
#     rows = cur.fetchall()
#     result_list = []
#     for row in rows:
#         if row['status'] == True:
#             status = CHECK_MARK
#         else:
#             status = CROSS_MARK
#         row_str = f"{status} | {row['movie_id']} | {row['movie_name']} | {row['movie_genre']} | {row['ratings_a']} | {row['ratings_v']}"
#         result_list.append(row_str)
#
#     result = "\n".join(result_list)
#     bot.send_message(message.chat.id, result)
#
# @bot.message_handler(commands=['show_genres'])
# def send_genres(message):
#     cur.execute("SELECT DISTINCT movie_genre FROM movies_2 order by movie_genre ")
#     rows = cur.fetchall()
#     result = '\n'.join([f"{row['movie_genre']}" for row in rows])
#     bot.send_message(message.chat.id, result)


bot.polling(none_stop=True)

cur.close()
conn.close()

#
#
# @bot.message_handler(commands=['start'])
# def start_bot(message):
#     mess = f'PenisPrivet, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
#     bot.send_message(message.chat.id, mess, parse_mode='html')
#
#
# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#     if message.text == 'PENIS':
#         bot.send_message(message.chat.id, 'Idi nahuy', parse_mode='html')
#     elif message.text == 'id':
#         bot.send_message(message.chat.id, f'Idi nahuy dvazhdi: {message.from_user.id}', parse_mode='html')
#     elif message.text == 'photo':
#         photo = open('photo_2023-02-24_17-18-32.jpg', 'rb')
#         bot.send_photo(message.chat.id ,photo)
#     else:
#         bot.send_message(message.chat.id, 'Vashe idi nahuy', parse_mode='html')
#
#
# @bot.message_handler(content_types=['photo'])
# def get_user_photo(message):
#     bot.send_message(message.chat.id, 'Klassniy mem')
#
#
# @bot.message_handler(commands=['website'])
# def website(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Posetit' Pisun", url="https://bigbang.su/8-sezon-7-seriya"))
#     bot.send_message(message.chat.id, 'Pereidite nahuy', reply_markup=markup)
#
#
# @bot.message_handler(commands=['help'])
# def website(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     website = types.KeyboardButton('Knopka Chlena')
#     start = types.KeyboardButton('Start Chlena')
#     markup.add(website, start)
#     bot.send_message(message.chat.id, 'Pereidite nahuy', reply_markup=markup)
#
# @bot.message_handler(commands=['start'])
# def handle_message(message):
#     reply_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#     show_all_button = types.KeyboardButton('Show All')
#     show_watched_button = types.KeyboardButton('Show Watched')
#     show_unwatched_button = types.KeyboardButton('Show Unwatched')
#     show_fantasies_button = types.KeyboardButton('Show Fantasies')
#     reply_keyboard.add(show_all_button, show_watched_button, show_unwatched_button, show_fantasies_button)
#
#     bot.send_message(message.chat.id, 'Choose the command', reply_markup=reply_keyboard)
