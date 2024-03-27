""" HoverButton"""

from tkinter import FLAT, Button, PhotoImage

from classifypdf._util import LIGHT_BLUE
from classifypdf.tooltip import ToolTip

# class HoverButton(Button):
#     """HoverButton is a subclass of tkinter.Button that adds a tool tip to the button."""
#
#     def __init__(self, master, tool_tip=None, image_path=None, keep_pressed=False, **kw):
#         Button.__init__(self, master=master, **kw)
#         self.config(bg="blue", activebackground="sky blue")
#         self.default_background = self["background"]
#         self.bind("<Enter>", self.on_enter)
#         self.bind("<Leave>", self.on_leave)
#         if keep_pressed:
#             self.bind("<Button-1>", self.on_click)
#         if image_path:
#             self.image = PhotoImage(file=image_path)
#             self.configure(image=self.image)
#         # if tool_tip:
#         #     ToolTip(self, text=tool_tip)
#
#     def on_click(self, e):
#         """On_click is called when the mouse enters the button."""
#         # pylint: disable=unused-argument
#         if self["background"] == self.default_background:
#             self["background"] = self["activebackground"]
#         else:
#             self["background"] = self.default_background
#
#     def on_enter(self, e):
#         """on_enter is called when the mouse enters the button."""
#         # pylint: disable=unused-argument
#         self["background"] = self["activebackground"]
#
#     def on_leave(self, e):
#         """on_leave is called when the mouse leaves the button."""
#         # pylint: disable=unused-argument
#         self["background"] = self.default_background


class HoverButton(Button):
    """CustomButton is a subclass of tkinter.Button that adds a tool tip to the button."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=FLAT,  # Remove button relief
            bd=0,  # Remove border
            highlightthickness=0,  # Remove highlight
            padx=10,  # Add horizontal padding
            pady=5,  # Add vertical padding
            font=("Arial", 12),  # Set font
            foreground="white",  # Text color
            background="orange",  # Background color
        )
        # Bind events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(background="lightblue")  # Change color on hover

    def on_leave(self, event):
        self.config(background="green")  # Restore original color
