import random
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
        answer = self.bot.analise(message)
        self.log.insert('Антон', message)
        if answer:
            self.log.insert(self.name, answer)


class ChatBot(object):
    def __init__(self):
        self.hello = ('hi', 'hello', 'hey', 'aloha')
        self.answer = ('What?', 'quack', 'quack-quack', 'dude!', 'Keep it up!')
        self.stupid = False

    def analise(self, message):
        self.msg = message.lower()
        if not self.check_english(self.msg[0]):
            if self.stupid:
                self.stupid = False
                return 'Ты что, дурак? Я говорю только на анлийском!'
            self.stupid = True
            return 'I do not understand you. Please, use English!'
        else:
            self.stupid = False

        if self.msg[0] == 'h':
            word = self.msg.split()[0]
            if word in self.hello:
                return random.choice(self.hello)
            else:
                return random.choice(self.answer)

    @staticmethod
    def check_english(char):
        char = ord(char)
        if (char >= ord('A')) and (char <= ord('z')):
            return True
        return False

if __name__ == '__main__':
    chat = ChatWindow()
    chat.mainloop()

