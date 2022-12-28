from telegram_part import Bot, answer_dict, command_list
from telebot import types
from _comics_database import Comic

TOKEN = 'TOKEN'

admin_id = [1234]  # your telegram id

# sort part starts
class sort_class(Bot):

    def sort_command(self, message):
        answer_dict.clear()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('By genre')
        item2 = types.KeyboardButton('By kind')
        item3 = types.KeyboardButton('By adaptation')
        item4 = types.KeyboardButton('By artist')
        item5 = types.KeyboardButton('By author')
        item6 = types.KeyboardButton('By translation')
        item7 = types.KeyboardButton('By name')
        item8 = types.KeyboardButton('menu')
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
        self.bot.send_message(message.chat.id, 'Choose type of sorting', reply_markup=markup)
        self.bot.register_next_step_handler(message, self.find_in_database)

    def find_in_database(self, message):
        if message.text == 'By genre':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(self.comics_db.find_genre(), markup)
            self.bot.send_message(message.chat.id, 'By genre', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_genre)
        elif message.text == 'By kind':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(self.comics_db.find_kind(), markup)
            self.bot.send_message(message.chat.id, 'By kind', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_kind)
        elif message.text == 'By adaptation':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(self.comics_db.find_adaptation(), markup)
            self.bot.send_message(message.chat.id, 'By adaptation', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_adaptation)
        elif message.text == 'By artist':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(self.comics_db.find_artist(), markup)
            self.bot.send_message(message.chat.id, 'By artist', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_artist)
        elif message.text == 'By author':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(self.comics_db.find_author(), markup)
            self.bot.send_message(message.chat.id, 'By author', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_author)
        elif message.text == 'By translation':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(self.comics_db.find_translation(), markup)
            self.bot.send_message(message.chat.id, 'By translation', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_translation)
        elif message.text == 'By name':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(self.comics_db.sort_comic(), markup)
            self.bot.send_message(message.chat.id, 'By name', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_database)
        elif message.text == 'menu':
            self.menu_command(message)
        else:
            self.bot.send_message(message.chat.id, 'Invalid input')
            self.bot.register_next_step_handler(message, self.sort_command)

    def sort_in_genre(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        temp = self.comics_db.sort_genre(message.text)
        if not temp:
            self.bot.send_message(message.chat.id, 'Not found such genre comics', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_genre)
        else:
            markup = self.make_buttons(temp, markup)
            self.bot.send_message(message.chat.id, 'Found', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_database)

    def sort_in_kind(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        temp = self.comics_db.sort_kind(message.text)
        if not temp:
            self.bot.send_message(message.chat.id, 'Not found such kind comics', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_kind)
        else:
            markup = self.make_buttons(temp, markup)
            self.bot.send_message(message.chat.id, 'Found', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_database)

    def sort_in_adaptation(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        temp = self.comics_db.sort_adaptation(message.text)
        if not temp:
            self.bot.send_message(message.chat.id, 'Not found such adaptation comics', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_adaptation)
        else:
            markup = self.make_buttons(temp, markup)
            self.bot.send_message(message.chat.id, 'Found', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_database)

    def sort_in_artist(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        temp = self.comics_db.sort_artist(message.text)
        if not temp:
            self.bot.send_message(message.chat.id, 'Not found such comics', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_artist)
        else:
            markup = self.make_buttons(temp, markup)
            self.bot.send_message(message.chat.id, 'Found', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_database)

    def sort_in_author(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        temp = self.comics_db.sort_author(message.text)
        if not temp:
            self.bot.send_message(message.chat.id, 'Not found such comics', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_author)
        else:
            markup = self.make_buttons(temp, markup)
            self.bot.send_message(message.chat.id, 'Found', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_database)

    def sort_in_translation(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        temp = self.comics_db.sort_translation(message.text)
        if not temp:
            self.bot.send_message(message.chat.id, 'Not found such translation', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_translation)
        else:
            markup = self.make_buttons(temp, markup)
            self.bot.send_message(message.chat.id, 'Found', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.sort_in_database)

    def sort_in_database(self, message):
        if self.request_comic(message):
            self.print_in_sort_database(message)
            markup = self.menu_keyboard(message)
            self.bot.reply_to(message, "If you want to try again enter /sort.", reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, "Your input is invalid or not such comics")

    def print_in_sort_database(self, message):
        key = message.text.lower()
        if self.comics_db.search_comics([key]):
            self.print_comic(message, '/search')
        elif key in command_list:
            self.command_choose(message, key)
        else:
            self.bot.reply_to(message, "Sorry, I don't find your comic.\n")

    def make_buttons(self, sort, markup):
        if not sort:
            return markup
        i = 0
        while i < len(sort):
            item = sort[i][0]
            item = types.KeyboardButton(str(item))
            markup.add(item)
            i += 1
        return markup

    def request_comic(self, message):
        i = 0
        sort = self.comics_db.sort_comic()
        while i < len(sort):
            item = sort[i][0]
            if message.text == item:
                return True
            i += 1
        return False


# sort part ends

# sort part ends
class recommend_class(Bot):
    def check_repeat(self, list, value):
        i = len(list) - 1
        while i >= 0:
            if list[i][0] == value:
                del list[i]
            i -= 1
        unique_list = []
        i = len(list) - 1
        while i >= 0:
            if list[i] not in unique_list:
                unique_list.append(list[i])
            i -= 1
        return unique_list

    def ask_recommendation(self, message):
        recommendation = message.text
        self.bot.send_message(message.chat.id, "Do you want to check some recommendations?(yes/no)")
        self.bot.register_next_step_handler(message, self.recommend_or_not, recommendation)

    def recommend_or_not(self, message, recommendation):
        if message.text == 'yes':
            self.recommend_comic(message, recommendation)
        elif message.text == 'no':
            markup = self.menu_keyboard(message)
            self.bot.reply_to(message, "If you want to try again enter /search.", reply_markup=markup)
        else:
            markup = self.menu_keyboard(message)
            self.bot.reply_to(message, "I don't recognize your command.\n\nIf you want to try again enter /search.",
                              reply_markup=markup)

    def recommend_comic(self, message, recommendation):
        recommend_list = []
        recommend_list.extend(self.comics_db.find_idauthor_recommend(recommendation))
        if len(recommend_list) < 3:
            recommend_list.extend(self.comics_db.find_idgenre_recommend(recommendation))
        if len(recommend_list) < 3:
            recommend_list.extend(self.comics_db.find_idauthor_recommend(recommendation))
        recommend_list = self.check_repeat(recommend_list, recommendation)
        if not recommend_list:
            markup = self.menu_keyboard(message)
            self.bot.send_message(message.chat.id,
                                  "Not found anything related ¯\_(ツ)_/¯. If you want to try again enter /search",
                                  reply_markup=markup)
        else:
            while len(recommend_list) > 3:
                recommend_list.pop()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = self.make_buttons(recommend_list, markup)
            self.bot.send_message(message.chat.id, 'Recommended\n', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.print_in_database)


class DBFinding(Comic):
    def find_adaptation(self):
        cursor = self.mydb.cursor()
        sql = "SELECT DISTINCT adaptation.type FROM comics1.adaptation ORDER BY type"
        cursor.execute(sql)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def find_artist(self):
        cursor = self.mydb.cursor()
        sql = "SELECT DISTINCT artist.surname FROM comics1.artist ORDER BY surname"
        cursor.execute(sql)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def find_author(self):
        cursor = self.mydb.cursor()
        sql = "SELECT DISTINCT author.surname FROM comics1.author ORDER BY surname"
        cursor.execute(sql)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def find_genre(self):
        cursor = self.mydb.cursor()
        sql = "SELECT DISTINCT genre.name FROM comics1.genre ORDER BY name"
        cursor.execute(sql)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def find_kind(self):
        cursor = self.mydb.cursor()
        sql = "SELECT DISTINCT kind.name FROM comics1.kind ORDER BY name"
        cursor.execute(sql)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def find_translation(self):
        cursor = self.mydb.cursor()
        sql = "SELECT DISTINCT translation.language FROM comics1.translation ORDER BY language"
        cursor.execute(sql)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist


class DBSorting(Comic):

    def sort_adaptation(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics\
    JOIN adaptation ON comics.adaptation_idadaptation = adaptation.idadaptation\
    WHERE adaptation.type = %s  ORDER BY comics.name"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def sort_artist(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics\
    JOIN artist ON comics.artist_idartist = artist.idartist\
    WHERE artist.surname = %s ORDER BY comics.name"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def sort_author(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics\
    JOIN author ON comics.author_idauthor = author.idauthor\
    WHERE author.surname = %s ORDER BY comics.name"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def sort_comic(self):
        cursor = self.mydb.cursor()
        sql = "SELECT name FROM comics1.comics ORDER BY name"
        cursor.execute(sql)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def sort_genre(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics\
    JOIN genre ON comics.genre_idgenre = genre.idgenre \
    WHERE genre.name = %s ORDER BY comics.name"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def sort_kind(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics\
    JOIN kind ON comics.kind_idkind = kind.idkind\
    WHERE kind.name = %s ORDER BY comics.name"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def sort_translation(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics\
    JOIN translation ON comics.translation_idtranslation = translation.idtranslation\
    WHERE translation.language = %s ORDER BY translation.language"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist


class DBRecommend(Comic):

    def find_idauthor_recommend(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.author_idauthor FROM comics WHERE comics.name = %s"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        val = self.find_author_recommend(mylist)
        return val

    def find_author_recommend(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics WHERE comics.author_idauthor = %s"
        cursor.execute(sql, int(value[0][0]))
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def find_idgenre_recommend(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.genre_idgenre FROM comics WHERE comics.name = %s"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        val = self.find_genre_recommend(mylist)
        return val

    def find_genre_recommend(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics WHERE comics.genre_idgenre = %s"
        cursor.execute(sql, int(value[0][0]))
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist

    def find_idartist_recommend(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.artist_idartist FROM comics WHERE comics.name = %s"
        cursor.execute(sql, value)
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        val = self.find_artist_recommend(mylist)
        return val

    def find_artist_recommend(self, value):
        cursor = self.mydb.cursor()
        sql = "SELECT comics.name FROM comics WHERE comics.artist_idartist = %s"
        cursor.execute(sql, int(value[0][0]))
        result = cursor.fetchall()
        mylist = list(result)
        self.mydb.commit()
        return mylist
