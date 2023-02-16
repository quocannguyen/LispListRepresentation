from tkinter import Tk, Label, Entry, LEFT, RIGHT, Frame, Button
from NestedLinkedListVisualiser import NestedLinkedListVisualiser


def parse_string_to_list(list_string):
    nested_list = []
    word = ""
    i = 0
    while i < len(list_string):
        character = list_string[i]
        if character == '(':
            if word != "":
                nested_list.append(word)
                word = ""
            inner_list, new_index = parse_string_to_list(list_string[i + 1:])
            nested_list.append(inner_list)
            i += new_index + 1
        elif character == ')':
            if word != "":
                nested_list.append(word)
            return nested_list, i
        elif character == ' ':
            if word != "":
                nested_list.append(word)
                word = ""
        else:
            word += character

        i += 1

    return nested_list[0]


def main():
    root = Tk()
    frame = Frame(root)
    frame.pack()
    Label(frame, text="LISP list: '").pack(side=LEFT)
    entry = Entry(frame)
    entry.pack(side=LEFT)

    def button_callback():
        nested_linked_list = parse_string_to_list(entry.get())
        nested_linked_list_visualiser = NestedLinkedListVisualiser(root)
        nested_linked_list_visualiser.create_list(nested_linked_list)

    Button(frame, text="Visualise", command=button_callback).pack(side=RIGHT)
    root.mainloop()


if __name__ == '__main__':
    main()
