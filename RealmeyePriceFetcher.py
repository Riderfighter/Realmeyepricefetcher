# coding=UTF-8
from lxml import html
import requests
import re
import time
from bs4 import BeautifulSoup
import numpy as np

try:
    # Python 2
    from Tkinter import *
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from tkinter import *
    from urllib.request import urlopen

window = Tk()
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)

# Constants
OFFERS_AMOUNT = 8


class Splash():
    def __init__(self, root, wait):
        self.__root = root
        self.__wait = wait + time.clock()
        self.__data = """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"""

    def __enter__(self):
        self.__root.withdraw()
        window = Toplevel(self.__root)
        canvas = Canvas(window)
        splash = PhotoImage(master=window, data=self.__data)
        scrW = window.winfo_screenwidth()
        scrH = window.winfo_screenheight()
        imgW = splash.width()
        imgH = splash.height()
        Xpos = (scrW - imgW) // 2
        Ypos = (scrH - imgH) // 2
        window.overrideredirect(True)
        window.geometry('+{}+{}'.format(Xpos, Ypos))
        canvas.configure(width=imgW, height=imgH, highlightthickness=0)
        canvas.grid()
        canvas.create_image(imgW // 2, imgH // 2, image=splash)
        window.update()

        self.__window = window
        self.__canvas = canvas
        self.__splash = splash

    def __exit__(self, exc_type, exc_val, exc_tb):
        now = time.clock()
        if now < self.__wait:
            time.sleep(self.__wait - now)

        del self.__splash
        self.__canvas.destroy()
        self.__window.destroy()

        self.__root.update_idletasks()
        self.__root.deiconify()


class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        def matches(fieldValue, acListEntry):
            pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
            return re.match(pattern, acListEntry)

        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)
            self.matchesFunction = matches
        Entry.__init__(self, *args, **kwargs)
        self.focus()
        self.autocompleteList = autocompleteList
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()
        self.bg = "white"
        self.fg = "black"
        self.h_bg = "#eee8aa"
        self.h_fg = "blue"
        self.current = -1
        self.var.trace('w', self.changed)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.optionsListbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.optionsListbox = Listbox(width=self["width"], height=self.listboxLength)

                    self.optionsListbox.bind("<<ListboxSelect>>", self.selection)
                    self.optionsListbox.bind("<Motion>", self.on_motion)
                    self.optionsListbox.bind("<Leave>", self.on_leave)
                    self.optionsListbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                self.optionsListbox.delete(0, END)
                for w in words:
                    self.optionsListbox.insert(END, w)
            else:
                if self.listboxUp:
                    self.optionsListbox.destroy()
                    self.listboxUp = False

    def reset_colors(self):
        for item in self.optionsListbox.get(0, END):
            self.optionsListbox.itemconfig(self.current, {"bg": self.bg})
            self.optionsListbox.itemconfig(self.current, {"fg": self.fg})

    def set_highlighted_item(self, index):
        self.optionsListbox.itemconfig(index, {"bg": self.h_bg})
        self.optionsListbox.itemconfig(index, {"fg": self.h_fg})

    def on_motion(self, event):
        if self.listboxUp:
            index = self.optionsListbox.index("@%s,%s" % (event.x, event.y))
            if self.current != -1 and self.current != index:
                self.reset_colors()
                self.set_highlighted_item(index)
            elif self.current == -1:
                self.set_highlighted_item(index)
            self.current = index

    def on_leave(self, event):
        if self.listboxUp:
            self.reset_colors()
            self.current = -1

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.optionsListbox.get(self.current))
            self.optionsListbox.destroy()
            self.listboxUp = False
            self.current = -1
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.optionsListbox.curselection() == ():
                index = '0'
            else:
                index = self.optionsListbox.curselection()[0]
            if index != '0':
                self.optionsListbox.selection_clear(first=index)
                index = str(int(index) - 1)
                self.optionsListbox.see(index)
                self.optionsListbox.selection_set(first=index)
                self.optionsListbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.optionsListbox.curselection() == ():
                index = '0'
            else:
                index = self.optionsListbox.curselection()[0]

            if index != END:
                self.optionsListbox.selection_clear(first=index)
                index = str(int(index) + 1)
                self.optionsListbox.see(index)
                self.optionsListbox.selection_set(first=index)
                self.optionsListbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]


class App():
    def __init__(self, window):
        self.__window = window
        scrW = self.__window.winfo_screenwidth()
        scrH = self.__window.winfo_screenheight()
        winWid = self.__window.winfo_width()
        winHei = self.__window.winfo_height()

        Xpos = (scrW - winWid) // 2
        Ypos = (scrH - winHei) // 2
        self.__window.title('RealmEye Prices')
        self.__window.config(background='black')
        self.__window.geometry('+{}+{}'.format(Xpos, Ypos))
        self.__root = Frame(self.__window, background='black')
        self.__root.grid(row=1, column=0, sticky=W)

        self.itemids = {}

        self.label = Label(self.__root, text="Buy", foreground='white', background='black')
        self.label.grid(row=1, column=0)
        self.label1 = Label(self.__root, text="Sell", foreground='white', background='black')
        self.label1.grid(row=2, column=0)
        self.entry = AutocompleteEntry(self.itemids, self.__root, highlightbackground='black')
        self.entry.grid(row=1, column=1, sticky=W)
        self.entry1 = AutocompleteEntry(self.itemids, self.__root, highlightbackground='black')
        self.entry1.grid(row=2, column=1, sticky=W)
        self.encode = Button(self.__root, text='Fetch', command=self.getrealmeyeInfo, highlightbackground='black')
        self.encode.grid(row=1, column=3, sticky=W)
        self.seller = Text(self.__root, height=1, width=1, borderwidth=0, state="normal")
        self.seller.grid(row=3, column=1, sticky=W)
        self.averagel = Label(self.__root, text="Average", foreground='white', background='black')
        self.averagel.grid(row=2, column=3)
        self.offersListbox = Listbox(self.__window, width=40, height=7)
        self.offersListbox.grid(row=4)
        self.offersListbox.bind("<Motion>", self.on_motion)
        self.offersListbox.bind("<<ListboxSelect>>", self.getSeller)

        self.Sellerlist = []

        self.current = -1

        c = requests.get('https://www.realmeye.com/current-offers')
        v = c.content
        soup = BeautifulSoup(v, 'lxml')
        for x, y in zip([item['href'] for item in soup.find_all('a', {'class': 'item-selling'})],
                        [item['title'] for item in soup.find_all('a', {'class': 'item-selling'})]):
            if 'Offers to sell Any item with ' in y:
                pass
            else:
                self.itemids[y.replace('Offers to sell ', '')] = int(x.replace('/offers-to/sell/', ''))

    def reject_outliers(self, data, m=2.):
        self.d = np.abs(data - np.median(data))
        self.mdev = np.median(self.d)
        self.s = self.d / self.mdev if self.mdev else 0.
        return data[self.s < m]

    def dictionaryCheck(self, word):
        try:
            for key, value in iter(self.itemids.items()):
                if word == key:
                    return self.itemids[word]
        except AttributeError:
            print("Fatal Error: 001")
        return word

    def getPageWithNewInfo(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        headers = {'User-Agent': user_agent}
        try:
            url = 'http://www.realmeye.com/offers-to/sell/' + str(self.dictionaryCheck(self.entry.get())) + '/'+str(self.dictionaryCheck(self.entry1.get()))+''
            page = requests.get(url, headers=headers)
            return page
        except AttributeError:
            print("Fatal Error: 002")

    def getrealmeyeInfo(self):
        del self.Sellerlist[:]
        self.offersListbox.delete(0, END)
        self.seller.delete("1.0", END)
        self.seller.config(width=1)
        page = self.getPageWithNewInfo()
        tree = html.fromstring(page.content)
        i = 1
        offerIndex = 1
        priceList = []
        while i < OFFERS_AMOUNT:
            Buy = tree.xpath('//*[@id="g"]/tbody/tr['+str(offerIndex)+']/td[1]/span[1]/span/text()')
            Sell = tree.xpath('//*[@id="g"]/tbody/tr['+str(offerIndex)+']/td[2]/span[1]/span/text()')
            Pure = tree.xpath('//*[@id="g"]/tbody/tr['+str(offerIndex)+']/td[2]/span[2]/span/text()')
            Pure2 = tree.xpath('//*[@id="g"]/tbody/tr['+str(offerIndex)+']/td[1]/span[2]/span/text()')
            Seller = tree.xpath('//*[@id="g"]/tbody/tr['+str(offerIndex)+']/td[6]/a/text()')
            WarningTag = tree.xpath('//*[@id="g"]/tbody/tr['+str(offerIndex)+']/td[5]/i/@class')
            if not Buy and not Sell and not Seller:
                break
            if ''.join(Pure) != '' or ''.join(Pure2) != '' or ''.join(Buy).replace('×','') == '' or ''.join(Sell).replace('×','') == '':
                offerIndex += 1
            else:
                self.offersListbox.insert(END, str(self.entry.get())+' : '+''.join(Buy).replace('×','')+'; '+str(self.entry1.get())+' : '+''.join(Sell).replace('×',''))
                self.Sellerlist.append(str('').join(Seller))
                if int(''.join(Sell).replace('×','')) <= 1:
                    priceList.append(int(''.join(Buy).replace('×','')))
                if 'glyphicon glyphicon-info-sign' in WarningTag:
                    self.offersListbox.itemconfig(i-1,{'bg':'orange'})
                elif 'glyphicon glyphicon-exclamation-sign' in WarningTag:
                    self.offersListbox.itemconfig(i-1,{'bg':'red'})
                i += 1
            offerIndex += 1
        if self.offersListbox.index(END) == 0:
            self.offersListbox.insert(END, "No trades found")
        self.averagel.config(text=str(np.median(self.reject_outliers(np.array(priceList)))))

    def on_motion(self, event):
        index = self.offersListbox.index("@%s,%s" % (event.x, event.y))
        self.current = index

    def getSeller(self, event):
        self.offersListbox.configure(exportselection=False)
        if self.current != -1:
            self.seller.delete("1.0", END)
            self.seller.config(width=len(self.Sellerlist[self.current]))
            self.seller.insert(END, self.Sellerlist[self.current])


if __name__ == "__main__":
    with Splash(window, 1.0):
        App(window)
    window.mainloop()
