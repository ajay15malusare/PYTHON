import tkinter


class Application(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.master.minsize(width=256, height=256)
        self.master.config()
        self.pack()

        self.main_frame = tkinter.Frame()

        self.some_list = [
            'One',
            'Two',
            'Three',
            'Four'
        ]

        self.some_listbox = tkinter.Listbox(self.main_frame)
        self.some_listbox.pack(fill='both', expand=True)
        self.main_frame.pack(fill='both', expand=True)

        # insert our items into the list box
        for i, item in enumerate(self.some_list):
            self.some_listbox.insert(i, item)

        # add a button to select the next item
        self.some_button = tkinter.Button(
            self.main_frame, text="Next", command=self.next_selection)
        self.some_button.pack(side='top')

        # not really necessary, just make things look nice and centered
        self.main_frame.place(in_=self.master, anchor='c', relx=.5, rely=.5)

    def next_selection(self):
        selection_indices = self.some_listbox.curselection()

        # default next selection is the beginning
        next_selection = 0

        # make sure at least one item is selected
        if len(selection_indices) > 0:
            # Get the last selection, remember they are strings for some reason
            # so convert to int
            last_selection = int(selection_indices[-1])

            # clear current selections
            self.some_listbox.selection_clear(selection_indices)

            # Make sure we're not at the last item
            if last_selection < self.some_listbox.size() - 1:
                next_selection = last_selection + 1

        self.some_listbox.activate(next_selection)
        self.some_listbox.selection_set(next_selection)

root = tkinter.Tk()
app = Application(root)
app.mainloop()