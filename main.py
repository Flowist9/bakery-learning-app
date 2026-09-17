"""Image-free bakery training demo, adapted from the original Kivy app."""

import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


# Fictional examples: (name, category, baking program).
# Program assignments are demonstration data, not baking instructions.
items = [
    ("Classic Baguette", "Baguettes", "Program 1"),
    ("Wholegrain Baguette", "Baguettes", "Program 1"),
    ("Seeded Baguette", "Baguettes", "Program 1"),
    ("White Loaf", "Bread", "Program 2"),
    ("Rye Loaf", "Bread", "Program 2"),
    ("Oat Loaf", "Bread", "Program 2"),
    ("Butter Croissant", "Pastries", "Program 3"),
    ("Chocolate Croissant", "Pastries", "Program 3"),
    ("Cinnamon Roll", "Pastries", "Program 4"),
    ("Vanilla Swirl", "Pastries", "Program 4"),
    ("Cheese Roll", "Savory Snacks", "Program 5"),
    ("Vegetable Pocket", "Savory Snacks", "Program 5"),
    ("Tomato Twist", "Savory Snacks", "Program 5"),
    ("Glazed Donut", "Donuts", "Program 6"),
    ("Chocolate Donut", "Donuts", "Program 6"),
    ("Berry Donut", "Donuts", "Program 6"),
    ("Blueberry Muffin", "Muffins", "Program 7"),
    ("Lemon Muffin", "Muffins", "Program 7"),
    ("Chocolate Muffin", "Muffins", "Program 7"),
    ("Oat Cookie", "Cookies", "Program 8"),
    ("Cocoa Cookie", "Cookies", "Program 8"),
    ("Vanilla Cookie", "Cookies", "Program 8"),
]


class BakeryTrainingApp(App):
    title = "Bakery Training App"

    def build(self):
        Window.clearcolor = (0.10, 0.12, 0.16, 1)
        self.pending_event = None
        self.layout = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        self.menu_section()
        return self.layout

    def cancel_pending_event(self):
        if self.pending_event is not None:
            self.pending_event.cancel()
            self.pending_event = None

    def on_stop(self):
        self.cancel_pending_event()

    def make_label(self, text, height=64, font_size=18):
        label = Label(text=text, size_hint_y=None, height=dp(height),
                      font_size=font_size, halign="center", valign="middle")
        label.bind(size=lambda widget, size: setattr(
            widget, "text_size", (max(0, size[0] - dp(12)), size[1])))
        return label

    def make_button(self, text, callback):
        button = Button(text=text, size_hint_y=None, height=dp(48),
                        background_normal="", background_color=(0.25, 0.36, 0.48, 1))
        button.bind(on_release=callback)
        return button

    def begin_section(self, title, back=True):
        self.cancel_pending_event()
        self.layout.clear_widgets()
        if back:
            self.layout.add_widget(self.make_button("Back to menu", self.back_to_menu))
        self.label = self.make_label(title, height=64, font_size=24)
        self.layout.add_widget(self.label)

    def add_scrolling_grid(self):
        scroll = ScrollView(do_scroll_x=False)
        grid = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        scroll.add_widget(grid)
        self.layout.add_widget(scroll)
        return grid

    def menu_section(self, instance=None):
        self.begin_section(self.title, back=False)
        self.layout.add_widget(self.make_label("Learn products, categories and baking programs."))
        for text, callback in (("Play Quiz", self.start_new_round),
                               ("Learn / Search", self.learn_section),
                               ("Program Section", self.program_section)):
            self.layout.add_widget(self.make_button(text, callback))
        self.layout.add_widget(Label(text="Fictional demonstration data"))

    def get_unique_numbers(self):
        return sorted({program for _, _, program in items},
                      key=lambda program: int(program.rsplit(" ", 1)[1]))

    def program_section(self, instance=None):
        self.begin_section("Program Section")
        programs = self.get_unique_numbers()
        self.number_dropdown = Spinner(text=programs[0] if programs else "No programs",
                                       values=programs, size_hint_y=None, height=dp(48))
        self.layout.add_widget(self.number_dropdown)
        self.item_grid = self.add_scrolling_grid()
        self.number_dropdown.bind(text=self.on_number_select)
        self.display_program_items(self.number_dropdown.text)

    def on_number_select(self, spinner, text):
        self.display_program_items(text)

    def display_program_items(self, filter_number=""):
        matching = [item for item in items if item[2] == filter_number]
        self.render_items(self.item_grid, matching)

    def start_new_round(self, *args):
        self.begin_section("Quiz")
        if not items:
            self.layout.add_widget(self.make_label("No example products available."))
            return
        self.correct_item = random.choice(items)
        name, category, program = self.correct_item
        self.layout.add_widget(self.make_label(
            f"Which baking program belongs to {name}?\nCategory: {category}", height=110))
        incorrect = [value for value in self.get_unique_numbers() if value != program]
        self.options = random.sample(incorrect, min(3, len(incorrect))) + [program]
        random.shuffle(self.options)
        self.button_layout = self.add_scrolling_grid()
        for option in self.options:
            self.button_layout.add_widget(self.make_button(option, self.check_answer))

    def check_answer(self, instance):
        # Prevent repeated clicks from scheduling multiple rounds.
        if self.pending_event is not None:
            return
        for button in self.button_layout.children:
            button.disabled = True
        if instance.text == self.correct_item[2]:
            self.label.text = "Correct!"
            instance.background_color = (0.15, 0.65, 0.30, 1)
            self.pending_event = Clock.schedule_once(self.load_next_round, 1.5)
        else:
            self.label.text = "Wrong! Try again."
            instance.background_color = (0.80, 0.20, 0.20, 1)
            self.pending_event = Clock.schedule_once(self.enable_buttons, 1.5)

    def enable_buttons(self, dt=0):
        self.pending_event = None
        self.label.text = "Quiz"
        for button in self.button_layout.children:
            button.disabled = False
            button.background_color = (0.25, 0.36, 0.48, 1)

    def load_next_round(self, dt):
        self.pending_event = None
        self.start_new_round()

    def back_to_menu(self, *args):
        self.menu_section()

    def learn_section(self, instance=None):
        self.begin_section("Learn / Search")
        self.category_dropdown = Spinner(text="All", values=self.get_categories(),
                                         size_hint_y=None, height=dp(48))
        self.search_input = TextInput(hint_text="Search product names...", multiline=False,
                                      size_hint_y=None, height=dp(48))
        self.layout.add_widget(self.category_dropdown)
        self.layout.add_widget(self.search_input)
        self.item_layout = self.add_scrolling_grid()
        self.category_dropdown.bind(text=self.on_category_select)
        self.search_input.bind(text=self.on_search_text_change)
        self.refresh_items()

    def get_categories(self):
        return ["All"] + sorted({category for _, category, _ in items})

    def on_category_select(self, spinner, text):
        self.refresh_items()

    def on_search_text_change(self, instance, value):
        self.refresh_items()

    def refresh_items(self):
        self.display_items(items, self.category_dropdown.text, self.search_input.text)

    def display_items(self, source_items, filter_category="All", search_query=""):
        query = search_query.strip().casefold()
        matching = [item for item in source_items
                    if (filter_category == "All" or item[1] == filter_category)
                    and query in item[0].casefold()]
        self.render_items(self.item_layout, matching)

    def render_items(self, grid, matching):
        grid.clear_widgets()
        if not matching:
            grid.add_widget(self.make_label("No matching products."))
        for name, category, program in matching:
            grid.add_widget(self.make_label(f"{name}\n{category}  |  {program}", height=88))


if __name__ == "__main__":
    BakeryTrainingApp().run()
