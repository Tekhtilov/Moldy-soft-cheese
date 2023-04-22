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
        input_list.append(message.text)
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


bot.polling(none_stop=True)

cur.close()
conn.close()
