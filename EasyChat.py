import random
import datetime
from time import strftime, localtime
from tkinter import Tk, Entry, StringVar, Text, Frame, Label, Button
from tkinter.messagebox import askyesno, showinfo


class ChatText(Text):
    def __init__(self, *args):
        Text.__init__(self, *args)
        self.tag_config('time', foreground='green')
        self.tag_config('nick', foreground='red')
        self.tag_config('message', foreground='black')

    def insert(self, nick, msg, *args):
        Text.insert(self, 'end', strftime("%H:%M", localtime()), 'time')
        Text.insert(self, 'end', ''.join((':', nick, '\n')), 'nick')
        Text.insert(self, 'end', msg + '\n', 'message')
        Text.see(self, 'end')


class ChatEntry(Frame):
    def __init__(self, command,  *args):
        Frame.__init__(self, *args)
        self.message = Entry(self)
        self.message.pack(side='left', fill='x', expand='true')
        self.btn = Button(self, text='Enter', command=lambda: command())
        self.btn.pack(side='left')

    def get(self):
        msg = self.message.get()
        self.message.delete(0, 10)
        return msg

    def insert(self, index, string):
        self.message.insert(index, string)


class ChatWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('EasyChat')
        self.geometry('400x300')
        self.name = 'Fuzzy Hipo'
        self.log = ChatText(self)
        self.chat = ChatEntry(self.analise)
        self.chat.pack(side='bottom', fill='x')
        self.log.pack(side='top', fill='both', expand='true')
        self.bot = ChatBot()

    def destroy(self):
        if askyesno('!!!', 'Close EasyChat?'):
            Tk.destroy(self)

    def analise(self):
        message = self.chat.get()
        if message:
            answer = self.bot.analise(message)
            self.log.insert('Антон', message)
            if answer:
                self.log.insert(self.name, answer)


class ChatBot(object):
    def __init__(self):
        self.hello = ('hi', 'hello', 'aloha', 'hey')
        self.stupidtalk = ('what?', 'quack', 'quack-quack', 'Dude', 'Ke?', 'bla-bla-bla', 'ORL?')
        self.motivation = ('What about school?', 'Shut up and start your project!')
        self.night = ("It's late. Go to bed!", 'Is it time for you to sleep?')
        self.needtar = ('Give me target word', 'I dont understand you. Give target')
        self.needinfo = ('I need more info', 'Give me more details')

        self.qhelp = ('What you want?', 'How can I help you?', 'M-m-m?', 'I listen you', 'Can I help you?')
        self.ahelp = ('I think about it', "I can't help you", 'Hm...Nothing', 'I do not know')

        self.qjokes = ('Do you want a joke?', 'May be you want a joke?', 'How about a joke?')
        self.ajokes = ("Anton, do you think I’m a bad mother?\nMy name is Paul.",
                       "My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away",
                       "Patient: Oh doctor, I’m just so nervous. This is my first operation.\n"
                       "Doctor: Don't worry. Mine too.")

        self.targets = {'help': self.help, 'yes': self.answer, 'no': self.answer}
        self.talks = {'joke': self.joke, 'python': self.python, 'project': self.progect}
        self.stupid = False
        self.dialog_line = False    # FIXME возможно это лишнее
        self.dialog = ''
        self.dialog_depth = 0

    def analise(self, msg):
        self.msg = msg.lower()
        if not self.check_english(self.msg[0]):
            if self.stupid:
                self.stupid = False
                return 'Ты что, дурак? Я говорю только на анлийском!'
            self.stupid = True
            return 'I do not understand you. Please, use English'
        else:
            self.stupid = False

        if self.dialog_line:
            return self.targets[self.dialog](self.msg)

        for aim in self.targets:
            if aim in self.msg:
                return self.targets[aim](self.msg)

        if self.msg[0] == 'h':
            word = self.msg.split()[0]
            if word in self.hello:
                return self.welcome()
            else:
                self.small_talk(self.msg)
        else:
            return self.small_talk(self.msg)

    def welcome(self):
        branch = random.randint(0, 2)
        answer = random.choice(self.hello)
        if branch == 0:
            return answer
        elif branch == 1:
            current_time = datetime.datetime.now().time().hour
            if current_time < 12:
                return 'Good morning!'
            elif current_time > 22:
                return random.choice(self.night)
            else:
                return answer
        else:
            answer = ''.join((answer[0].upper(), answer[1:]))
            return ''.join((answer, '!', 'How are you?'))

    def help(self, msg):
        targets = ('python', 'project')
        if not self.dialog_line:
            self.dialog = 'help'
            self.dialog_line = True
            self.dialog_depth = 1
            return random.choice(self.qhelp)
        else:
            for aim in targets:
                if aim in msg:
                    return self.talks[aim]()

            if self.dialog_depth == 1:
                self.dialog_depth = 2
                return random.choice(self.needtar)

            elif self.dialog_depth == 2:
                self.dialog_depth = 3
                return random.choice(self.needinfo)

            elif self.dialog_depth == 3:
                self.dialog = ''
                self.dialog_line = False
                self.dialog_depth = 0
                return random.choice(self.ahelp)

    def python(self):
        return 'Have you read Python help already?'

    def progect(self):
        return "I can't help you with your project"

    def small_talk(self, msg):
        branch = random.randint(0, 6)
        if branch == 0:
            return False
        elif branch == 1:
            current_time = datetime.datetime.now().time().hour
            if current_time > 22:
                return random.choice(self.night)
            elif current_time > 18:
                return random.choice(self.motivation)
            else:
                return random.choice(self.stupidtalk)
        elif branch < 5:
            return random.choice(self.stupidtalk)
        elif branch < 6:
            return 'Can you tell something else?'
        elif branch == 6:
            self.dialog = 'joke'
            return random.choice(self.qjokes)

    def joke(self, msg):
        self.dialog = ''
        if msg == 'yes':
            return random.choice(self.ajokes)
        return 'Okay'

    def answer(self, msg):
        if self.dialog in self.talks:
            return self.talks[self.dialog](msg)
        else:
            return self.small_talk(msg)

    @staticmethod
    def check_english(char):
        char = ord(char)
        if (char >= ord('A')) and (char <= ord('z')):
            return True
        return False


if __name__ == '__main__':
    chat = ChatWindow()
    chat.mainloop()

