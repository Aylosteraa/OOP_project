from _comics_database import Comic
import telebot
from telebot import custom_filters
from telebot import types

TOKEN = 'TOKEN'

admin_id = [1234]  # your telegram id

btn_list = ['title', 'author', 'artist', 'genre', 'periodicity', 'magazine',
            'chapters', 'status', 'colorization', 'kind', 'adaptation', 'translation', 'end', 'menu']
key_list = ['name', 'author', 'artist', 'genre', 'periodicity', 'magazine',
            'chapters', 'status', 'colorization', 'kind', 'adaptation', 'translation']
periodicity_list = ['every day', 'every week', 'every month', 'non-periodical']
kind_list = ['manga', 'manhwa', 'manhua', 'comics', 'maliopys']
status_list = ['frozen', 'ongoing', 'completed']
colorization_list = ['monochrome', 'non-monochrome', 'lineart']
adaptation_list = ['film', 'cartoon', 'tvshow', 'show', 'anime']
answer_dict = {}
saved = []
user_id = []
database_id = []
command_list = ['/start', '/help', '/insert', '/update', '/delete', '/search', '/sort', '/random', '/saved']


class menu_class:
    def admin_start(self, message):
        markup = self.menu_keyboard(message)
        self.bot.send_message(message.chat.id, "Hello! Let's start.\nChoose a command.", reply_markup=markup)

    def not_admin_start(self, message):
        user_id.clear()
        user_id.append(message.chat.id)
        if not self.comics_db.select_user(user_id):
            self.comics_db.insert_user(user_id[0])
        else:
            pass
        markup = self.menu_keyboard(message)
        self.bot.send_message(message.chat.id, "Hello! Let's start.\nChoose a command.", reply_markup=markup)

    def help_command(self, message):
        self.bot.send_message(
            message.chat.id,
            "/insert - add new comics\n/delete - delete comics\n/update - update comics\n/search - search comics"
            "\n/sort - sort comics\n/random - random comics\n/saved - saved comics")

    def not_admin_help_command(self, message):
        self.bot.send_message(
            message.chat.id, "/search - search comics"
                             "\n/sort - sort comics\n/random - random comics\n/saved - saved comics")

    def generate_buttons(self, button_list, markup):
        for button in button_list:
            markup.add(types.KeyboardButton(button))
        return markup

    def create_keyboards(self, button_list, width=2):
        markup = types.ReplyKeyboardMarkup(row_width=width)
        markup = self.generate_buttons(button_list, markup)
        return markup

    def keyboard_insert(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('title')
        item2 = types.KeyboardButton('author')
        item3 = types.KeyboardButton('artist')
        item4 = types.KeyboardButton('genre')
        item5 = types.KeyboardButton('periodicity')
        item6 = types.KeyboardButton('magazine')
        item7 = types.KeyboardButton('chapters')
        item8 = types.KeyboardButton('status')
        item9 = types.KeyboardButton('colorization')
        item10 = types.KeyboardButton('kind')
        item11 = types.KeyboardButton('adaptation')
        item12 = types.KeyboardButton('translation')
        item13 = types.KeyboardButton('end')
        item14 = types.KeyboardButton('menu')
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13,
                   item14)
        return markup

    def menu_keyboard(self, message):
        user_id.clear()
        user_id.append(message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if user_id == admin_id:
            item1 = types.KeyboardButton('/insert')
            item2 = types.KeyboardButton('/delete')
            item3 = types.KeyboardButton('/update')
            item4 = types.KeyboardButton('/search')
            item5 = types.KeyboardButton('/sort')
            item6 = types.KeyboardButton('/random')
            item7 = types.KeyboardButton('/saved')
            markup.add(item1, item2, item3, item4, item5, item6, item7)
        else:
            item4 = types.KeyboardButton('/search')
            item5 = types.KeyboardButton('/sort')
            item6 = types.KeyboardButton('/random')
            item7 = types.KeyboardButton('/saved')
            markup.add(item4, item5, item6, item7)
        return markup

    def command_choose(self, message, command):
        user_id.clear()
        user_id.append(message.chat.id)
        if command == '/start':
            if user_id == admin_id:
                self.admin_start(message)
            else:
                self.not_admin_start(message)
        elif command == '/help':
            if user_id == admin_id:
                self.help_command(message)
            else:
                self.not_admin_help_command(message)
        elif command == '/insert':
            self.insert_command(message)
        elif command == '/update':
            self.update_command(message)
        elif command == '/delete':
            self.delete_command(message)
        elif command == '/search':
            self.print_command(message)
            self.menu_command(message)
        elif command == '/sort':
            self.sort_command(message)
        elif command == '/random':
            self.random_command(message)
            self.menu_command(message)
        elif command == '/saved':
            self.saved_command(message)
        else:
            pass

    def menu_command(self, message):
        markup = self.menu_keyboard(message)
        self.bot.send_message(message.chat.id, "Choose a command.", reply_markup=markup)

    def return_to_main(self, message, key, command, key1):
        self.bot.reply_to(message, "You can't choose this answer. Try again.")
        self.bot.register_next_step_handler(message, self.insert_comics, key, command, key1)

            
# insert part starts


class insert_update_class(menu_class):
    def insert_command(self, message):
        command = 1
        answer_dict.clear()
        markup = self.keyboard_insert()
        self.bot.reply_to(message, "Insert comics. Choose what you want to add.", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command)

    def update_command(self, message):
        answer_dict.clear()
        self.bot.reply_to(message, "Update comics. Enter name of comics.")
        self.bot.register_next_step_handler(message, self.update_in_database)

    def enter_update(self, message, key1):
        command = 2
        markup = self.keyboard_insert()
        self.print_comic(message)
        self.bot.reply_to(message, "Update comics. Choose what you want to update.", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)

    def update_in_database(self, message):
        key = message.text.lower()
        if self.comics_db.search_comics([key]):
            key1 = self.comics_db.search_comics([key])
            self.enter_update(message, key1)
        elif message.text == '/update':
            self.update_command(message)
        else:
            self.bot.reply_to(message, "Sorry, I don't find your comic.\n\nYou can /insert it or try /update again")

    def select_something(self, message, keyl, choice, leg):
        if choice == 'author':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_author(keyl))])
        elif choice == 'artist':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_artist(keyl))])
        elif choice == 'translation':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_translation(keyl, leg))])
        elif choice == 'magazine':
            answer_dict[choice] = ([x[0] for x in (self.comics_db.search_magazine(keyl))])

    def update_something(self, message, keyl, choice, key1, leg):
        if choice == 'author':
            self.comics_db.update_author(keyl, key1)
        elif choice == 'artist':
            self.comics_db.update_artist(keyl, key1)
        elif choice == 'translation':
            self.comics_db.update_trans(keyl, key1, leg)
        elif choice == 'magazine':
            self.comics_db.update_magazine(keyl, key1)

    def quation(self, message, quation, key, commmand, key1):
        self.bot.reply_to(message, quation)
        self.bot.register_next_step_handler(message, self.insert_comics, key, commmand, key1)

    def quation_choose(self, message, button_list, quation, key, commmand, key1):
        markup = self.create_keyboards(button_list)
        message = self.bot.reply_to(message, quation, reply_markup=markup)
        self.bot.register_next_step_handler(message, self.insert_comics, key, commmand, key1)
        # bot.register_next_step_handler(message, return_to_main, key, button_list, commmand, key1)

    def incorrect_message(self, message, command, key1):
        self.bot.reply_to(message, "I don't recognize your messege.")
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)

    def check_key(self):
        answer_list = []
        not_in_answer = []
        for key in answer_dict:
            answer_list.append(key)
        for key1 in key_list:
            if key1 not in answer_list:
                not_in_answer.append(key1)
        return not_in_answer

    def end(self, message, command, key1):
        if command == 1:
            if self.check_key():
                key_l = self.check_key()
                self.bot.reply_to(message, ', '.join(map(str,
                                                         key_l)) + " wasn't add.\n\nChoose what you want to add.")
                self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
                return
            else:
                self.comics_db.insert_all(answer_dict)
                markup = self.menu_keyboard(message)
                self.bot.send_message(message.chat.id, "The end of inserting.\n\nChoose a command.",
                                      reply_markup=markup)
        else:
            markup = self.menu_keyboard(message)
            self.bot.send_message(message.chat.id, "The end of updating.\n\nChoose a command.", reply_markup=markup)

    def bot_asks(self, message, command, key1=None):
        value = message.text
        if value == 'title':
            self.quation(message, "Enter title of comics", value, command, key1)
        elif value == 'author':
            self.quation(message, "Enter author's surname of comics", value, command, key1)
        elif value == 'artist':
            self.quation(message, "Enter artist's surname of comics", value, command, key1)
        elif value == 'genre':
            self.quation(message, "Enter genre of comics", value, command, key1)
        elif value == 'periodicity':
            self.quation_choose(message, periodicity_list,
                           'Choose periodicity of comics', value, command, key1)
        elif value == 'magazine':
            self.quation(message, "Enter magazine", value, command, key1)
        elif value == 'chapters':
            self.quation(message, "Enter number of comics' chapters", value, command, key1)
        elif value == 'status':
            self.quation_choose(message, status_list, 'Choose status of comics', value, command, key1)
        elif value == 'colorization':
            self.quation_choose(message, colorization_list,
                           'Choose colorization', value, command, key1)
        elif value == 'kind':
            self.quation_choose(message, kind_list, 'Choose kind of comics', value, command, key1)
        elif value == 'adaptation':
            self.quation_choose(message, adaptation_list, 'Choose adaptation', value, command, key1)
        elif value == 'translation':
            self.quation(message, "Enter language", value, command, key1)
        elif value in command_list:
            self.command_choose(message, value)
        elif value == 'menu':
            self.menu_command(message)
        elif value == 'end':
            self.end(message, command, key1)
        else:
            self.incorrect_message(message, command, key1)

    def insert_comics(self, message, choice, command, key1):
        key = message.text.lower()
        if key in command_list:
            self.command_choose(message, key)
            return
        keyl = list()
        keyl.append(key)
        if choice == 'title':
            if command == 1:
                answer_dict['name'] = self.comics_db.select_name(key)
            else:
                self.comics_db.update_name(key, key1)
        elif choice == 'genre':
            if self.comics_db.search_genre(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_genre(keyl))])
                else:
                    self.comics_db.update_genre(keyl, key1)
            else:
                self.comics_db.insert_genre(keyl)
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_genre(keyl))])
                else:
                    self.comics_db.update_genre(keyl, key1)
        elif choice == 'author':
            if self.comics_db.search_author(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_author(keyl))])
                else:
                    self.comics_db.update_author(keyl, key1)
            else:
                self.extra_not_in_base(message,
                    "It seems that your author is not in our database.\nDo you want to insert it? (yes or no)\n",
                                  keyl, choice, command, key1)
                return
        elif choice == 'artist':
            if self.comics_db.search_artist(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_artist(keyl))])
                else:
                    self.comics_db.update_artist(keyl, key1)
            else:
                self.extra_not_in_base(message,
                    "It seems that your artist is not in our database.\nDo you want to insert it? (yes or no)\n",
                                  keyl, choice, command, key1)
                return
        elif choice == 'periodicity':
            if key not in periodicity_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_period(key, keyl))])
            else:
                self.comics_db.update_period(key, keyl, key1)
        elif choice == 'magazine':
            if self.comics_db.search_magazine(keyl):
                if command == 1:
                    answer_dict[choice] = ([x[0] for x in (self.comics_db.search_magazine(keyl))])
                else:
                    self.comics_db.update_magazine(key, key1)
            else:
                self.extra_not_in_base(message,
                                  "It seems that your magazine is not in our database.\nDo you want to insert it? (yes or no)\n",
                                  keyl, choice, command, key1)
                return
        elif choice == 'chapters':
            if not key.isdigit():
                self.bot.reply_to(message, "Chapters is number. Please try again.")
                self.bot.register_next_step_handler(message, self.insert_comics, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = self.comics_db.select_num(int(key))
            else:
                self.comics_db.update_num(key, key1)
        elif choice == 'status':
            if key not in status_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_status(key, keyl))])
            else:
                self.comics_db.update_status(key, keyl, key1)
        elif choice == 'colorization':
            if key not in colorization_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_color(key, keyl))])
            else:
                self.comics_db.update_color(key, keyl, key1)
        elif choice == 'kind':
            if key not in kind_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_kind(key, keyl))])
            else:
                self.comics_db.update_kind(key, keyl, key1)
        elif choice == 'adaptation':
            if key not in adaptation_list:
                self.return_to_main(message, choice, command, key1)
                return
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.select_adapt(key, keyl))])
            else:
                self.comics_db.update_adapt(key, keyl, key1)
        elif choice == 'translation':
            self.translation_legality(message, keyl, choice, command, key1)
            return
        else:
            raise TypeError
        markup = self.keyboard_insert()
        self.bot.reply_to(message, 'Choose what you want to add.', reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
        print(answer_dict)

    # author, artist and magazine
    def extra_not_in_base(self, message, quation, keyl, choice, command, key1=None, extra=None):
        self.bot.reply_to(message, quation)
        self.bot.register_next_step_handler(message, self.add_new_or_not, keyl, choice, command, key1, extra)

    def magazine_periodicity(self, message, keyl, choice, command, key1):
        circ = message.text
        if not circ.isdigit():
            self.bot.reply_to(message, "Circulation is number. Try again.\n")
            self.bot.register_next_step_handler(message, self.magazine_periodicity, keyl, choice, command, key1)
            return
        markup = self.create_keyboards(periodicity_list)
        self.bot.reply_to(message, "Thank you! Also enter, please, its periodicity!\n", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, circ)

    # translation
    def translation_legality(self, message, keyl, choice, command, key1=None):
        self.bot.reply_to(message, "Is your translation official or non-official?")
        self.bot.register_next_step_handler(message, self.translate_select, keyl, choice, command, key1)

    def translate_select(self, message, keyl, choice, command, key1):
        leg = message.text.lower()
        if leg not in ('official', 'non-official'):
            self.bot.reply_to(message, "Legality is official or non-official. Try again.\n")
            self.bot.register_next_step_handler(message, self.translate_select, keyl, choice, command, key1)
            return
        elif leg in command_list:
            self.command_choose(message, leg)
            return
        if self.comics_db.search_translation(keyl, leg):
            if command == 1:
                answer_dict[choice] = ([x[0] for x in (self.comics_db.search_translation(keyl, leg))])
            else:
                self.comics_db.update_trans(keyl, key1, leg)
            self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
        else:
            self.bot.reply_to(message,
                    "It seems that your translation is not in our database.\nDo you want to insert it? (yes or no)\n")
            self.bot.register_next_step_handler(message, self.add_new_or_not, keyl, choice, command, key1, leg)

    def add_new_or_not(self, message, keyl, choice, command, key1, extra):
        key = message.text.lower()
        if key == 'yes':
            if choice in ('author', 'artist'):
                self.bot.reply_to(message, 'Enter name:')
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
            elif choice == 'magazine':
                self.bot.reply_to(message, 'Enter circulation:')
                self.bot.register_next_step_handler(message, self.magazine_periodicity, keyl, choice, command, key1)
            elif choice == 'translation':
                markup = self.create_keyboards(status_list)
                self.bot.reply_to(message, "Enter translation status:\n", reply_markup=markup)
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
        elif key == 'no':
            markup = self.keyboard_insert()
            self.bot.reply_to(message, 'Choose what you want to add.', reply_markup=markup)
            self.bot.register_next_step_handler(message, self.bot_asks, command, key1)
            return
        elif key in command_list:
            self.command_choose(message, key)
            return
        else:
            self.bot.reply_to(message, "I don't recognize your command. Try again!")
            self.bot.register_next_step_handler(message, self.add_new_or_not, keyl, choice, command, key1, extra)

    def extra_insert(self, message, keyl, choice, command, key1, extra):
        key = message.text.lower()
        if key in command_list:
            self.command_choose(message, key)
            return
        if choice == 'author':
            self.comics_db.insert_author(key, keyl)
        elif choice == 'artist':
            self.comics_db.insert_artist(key, keyl)
        elif choice == 'translation':
            if key not in status_list:
                self.bot.reply_to(message, "You can't choose this answer. Try again.")
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
                return
            se = list()
            se.append(key)
            self.comics_db.insert_translation(keyl, extra, self.comics_db.select_status(key, se))
        elif choice == 'magazine':
            if key not in periodicity_list:
                self.bot.reply_to(message, "You can't choose this answer. Try again.")
                self.bot.register_next_step_handler(message, self.extra_insert, keyl, choice, command, key1, extra)
                return
            se = list()
            se.append(key)
            self.comics_db.insert_magazine(keyl, extra, self.comics_db.select_period(key, se))
        if command == 1:
            self.select_something(message, keyl, choice, extra)
        else:
            self.update_something(message, keyl, choice, key1, extra)
        markup = self.keyboard_insert()
        self.bot.reply_to(message, choice.capitalize() + ' was inserted. Choose what you want to add next.',
                     reply_markup=markup)
        self.bot.register_next_step_handler(message, self.bot_asks, command, key1)


# chooses

# insert or update part ends
# random part starts
class random_class:
    def random_command(self, message):
        key = self.comics_db.get_random()
        row = self.comics_db.print_comics(key)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Save', callback_data='save')
        markup.add(btn1)
        saved.clear()
        saved.append(key)
        user_id.clear()
        user_id.append(message.chat.id)
        print(user_id)
        l = ([x[0] for x in self.comics_db.select_user(user_id)])
        database_id.clear()
        database_id.append(l[0])
        self.bot.reply_to(message, self.print_info(row[0]), disable_notification=True, reply_markup=markup)
            
# random part ends
