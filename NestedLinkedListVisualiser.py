from tkinter import Canvas, W, LAST, BOTTOM, Frame

HEIGHT = 15
POINTER_WIDTH = 15
MIN_RIGHT_ARROW_LENGTH = 20
PADDING = 5
NULL_LENGTH = 20


class NestedLinkedListVisualiser:

    def __init__(self, root):
        self.root = root
        frame = Frame(root)
        frame.pack(side=BOTTOM)

        self.canvas = Canvas(frame)
        self.canvas.pack()

    def __del__(self):
        self.root.mainloop()

    def create_node(self, text, x, y):
        text_id = self.canvas.create_text(x, y, text=text, anchor=W)
        x_left, y_top, x_right, y_bottom = self.canvas.bbox(text_id)
        x_right = x_left + PADDING * 2 if x_right < x_left + PADDING * 2 else x_right
        self.canvas.create_rectangle(x_left, y_top, x_right, y_bottom)
        self.canvas.create_rectangle(x_right, y_top, x_right + POINTER_WIDTH, y_bottom)
        return x_left, y_bottom, x_right + POINTER_WIDTH / 2, (y_top + y_bottom) / 2, text_id

    def create_down_arrow(self, x, y):
        self.canvas.create_line(x + PADDING, y, x + PADDING, y + HEIGHT, arrow=LAST)
        return y + HEIGHT

    def create_right_arrow(self, x_left, y, x_right):
        x_right = x_left + MIN_RIGHT_ARROW_LENGTH if x_right < x_left + MIN_RIGHT_ARROW_LENGTH else x_right
        self.canvas.create_line(x_left, y, x_right, y, arrow=LAST)
        return x_right

    def create_diagonal_line(self, x, y):
        self.canvas.create_line(x - POINTER_WIDTH / 2, y + HEIGHT / 2, x + POINTER_WIDTH / 2, y - HEIGHT / 2)
        return x + POINTER_WIDTH / 2

    def create_null_node(self, x, y):
        x0, y0, x1, y1, text_id = self.create_node("null", x, y)
        self.canvas.move(text_id, 0, HEIGHT)
        return self.create_diagonal_line(x1, y1), y1 + HEIGHT

    def create_list(self, linked_list, x_left=PADDING, y=PADDING+HEIGHT/2):
        length = len(linked_list)
        if length == 0:
            return self.create_null_node(x_left, y)

        new_y = y
        for i in range(length):
            if isinstance(linked_list[i], list):
                x0, y0, x1, y1, _ = self.create_node("", x_left, y)
                temp_y = self.create_down_arrow(x0, y0) + HEIGHT / 2
                x_left, temp_y = self.create_list(linked_list[i], x_left, temp_y)
                new_y = temp_y if temp_y > new_y else new_y
            else:
                x0, y0, x1, y1, _ = self.create_node(linked_list[i], x_left, y)
                new_y = y0 if y0 > new_y else new_y
            if i != length - 1:
                x_left = self.create_right_arrow(x1, y1, x_left + PADDING)
            else:
                new_x_left = self.create_diagonal_line(x1, y1)
                x_left = new_x_left if new_x_left > x_left else x_left

        print(x_left, new_y)
        self.resize(x_left, new_y)
        return x_left, new_y

    def resize(self, x, y):
        self.canvas.config(width=x+PADDING, height=y+PADDING)
