""" Class to display pdf and allow classification"""

# import io
import os
from tkinter import LEFT, RIGHT, SUNKEN, Frame, Label

# from classifypdf._util import BACKGROUND_COLOR, HIGHLIGHT_COLOR, ROOT_PATH,MyException
from classifypdf._util import BACKGROUND_COLOR, HIGHLIGHT_COLOR, ROOT_PATH
from classifypdf.display_canvas import DisplayCanvas
from classifypdf.hoverbutton import HoverButton
from classifypdf.menubox import MenuBox

# import PyPDF2
# import pytesseract
# from PIL import Image


class PdfViewer(Frame):  # pylint: disable=too-many-instance-attributes
    """Class to display pdf and allow classification"""

    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.pdf = None
        self.page = None
        self.paths = []
        self.pathidx = -1
        self.total_pages = 0
        self.pageidx = 0
        self.scale = 1.0
        self.rotate = 0
        self.save_path = None
        self._init_ui()

    def _init_ui(self):  # pylint: disable=too-many-statements,too-many-locals
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        h = int(hs - 100)
        w = int(h / 1.414) + 100
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        # noinspection PyUnresolvedReferences
        self.master.geometry(f"{w}x{h}+{x}+{y}")
        # noinspection PyUnresolvedReferences
        self.master.title("PDFViewer")

        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(0, weight=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)

        self.configure(bg=BACKGROUND_COLOR, bd=0)

        tool_frame = Frame(self, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        pdf_frame = Frame(self, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)

        tool_frame.grid(row=0, column=0, sticky="news")
        pdf_frame.grid(row=0, column=1, sticky="news")

        # Tool Frame
        tool_frame.columnconfigure(0, weight=1)
        tool_frame.rowconfigure(0, weight=0)
        tool_frame.rowconfigure(1, weight=1)
        tool_frame.rowconfigure(2, weight=0)
        tool_frame.rowconfigure(3, weight=2)

        options = MenuBox(tool_frame, image_path=os.path.join(ROOT_PATH, "resources/options.png"))
        options.grid(row=0, column=0)

        options.add_item("Open Files...", self._open_file)
        options.add_item("Open Directory...", self._open_dir, seperator=True)
        options.add_item("Next File", self._next_file)
        options.add_item("Previous File", self._prev_file, seperator=True)
        options.add_item("Help...", self._help, seperator=True)
        options.add_item("Exit", self.master.quit)

        tools = Frame(tool_frame, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        tools.grid(row=2, column=0)

        HoverButton(
            tools,
            # image_path=os.path.join(ROOT_PATH, "resources/clear.png"),
            command=self._clear,
            width=50,
            height=50,
            bg=BACKGROUND_COLOR,
            # bg="sky blue",
            bd=0,
            # tool_tip="Clear",
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
            # activebackground="blue",
        ).pack(pady=2)
        HoverButton(
            tools,
            # image_path=os.path.join(ROOT_PATH, "resources/open_file.png"),
            command=self._open_file,
            width=50,
            height=50,
            bg=BACKGROUND_COLOR,
            bd=0,
            # tool_tip="Open Files",
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(pady=2)
        HoverButton(
            tools,
            # image_path=os.path.join(ROOT_PATH, "resources/open_dir.png"),
            command=self._open_dir,
            width=50,
            height=50,
            bg=BACKGROUND_COLOR,
            bd=0,
            # tool_tip="Open Directory",
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(pady=2)
        # HoverButton(
        #     tools,
        #     image_path=os.path.join(ROOT_PATH, "resources/search.png"),
        #     command=self._search_text,
        #     width=50,
        #     height=50,
        #     bg=BACKGROUND_COLOR,
        #     bd=0,
        #     tool_tip="Search Text",
        #     highlightthickness=0,
        #     activebackground=HIGHLIGHT_COLOR,
        # ).pack(pady=2)
        # HoverButton(
        #     tools,
        #     image_path=os.path.join(ROOT_PATH, "resources/extract.png"),
        #     command=self._extract_text,
        #     width=50,
        #     height=50,
        #     bg=BACKGROUND_COLOR,
        #     bd=0,
        #     tool_tip="Extract Text",
        #     keep_pressed=True,
        #     highlightthickness=0,
        #     activebackground=HIGHLIGHT_COLOR,
        # ).pack(pady=2)
        # HoverButton(
        #     tools,
        #     image_path=os.path.join(ROOT_PATH, "resources/ocr.png"),
        #     command=self._run_ocr,
        #     width=50,
        #     height=50,
        #     bg=BACKGROUND_COLOR,
        #     bd=0,
        #     tool_tip="Run OCR",
        #     highlightthickness=0,
        #     activebackground=HIGHLIGHT_COLOR,
        # ).pack(pady=2)

        file_frame = Frame(tools, width=50, height=50, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        file_frame.pack(pady=2)

        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)

        HoverButton(
            file_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/prev_file.png"),
            command=self._prev_file,
            width=25,
            height=50,
            bg=BACKGROUND_COLOR,
            bd=0,
            # tool_tip="Previous File",
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).grid(row=0, column=0)
        HoverButton(
            file_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/next_file.png"),
            command=self._next_file,
            width=25,
            height=50,
            bg=BACKGROUND_COLOR,
            bd=0,
            # tool_tip="Next File",
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).grid(row=0, column=1)

        HoverButton(
            tool_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/help.png"),
            command=self._help,
            width=50,
            height=50,
            bg=BACKGROUND_COLOR,
            bd=0,
            # tool_tip="Help",
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).grid(row=3, column=0, sticky="s")

        # PDF Frame
        pdf_frame.columnconfigure(0, weight=1)
        pdf_frame.rowconfigure(0, weight=0)
        pdf_frame.rowconfigure(1, weight=0)

        page_tools = Frame(pdf_frame, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        page_tools.grid(row=0, column=0, sticky="news")

        page_tools.rowconfigure(0, weight=1)
        page_tools.columnconfigure(0, weight=1)
        page_tools.columnconfigure(1, weight=0)
        page_tools.columnconfigure(2, weight=2)
        page_tools.columnconfigure(3, weight=0)
        page_tools.columnconfigure(4, weight=1)

        nav_frame = Frame(page_tools, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        nav_frame.grid(row=0, column=1, sticky="ns")

        HoverButton(
            nav_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/first.png"),
            command=self._first_page,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=LEFT, expand=True)
        HoverButton(
            nav_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/prev.png"),
            command=self._prev_page,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=LEFT, expand=True)

        self.page_label = Label(
            nav_frame,
            bg=BACKGROUND_COLOR,
            bd=0,
            fg="white",
            font="Arial 8",
            text=f"Page {self.pageidx} of {self.total_pages}",
        )
        self.page_label.pack(side=LEFT, expand=True)

        HoverButton(
            nav_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/next.png"),
            command=self._next_page,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=LEFT, expand=True)
        HoverButton(
            nav_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/last.png"),
            command=self._last_page,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=LEFT, expand=True)

        zoom_frame = Frame(page_tools, bg=BACKGROUND_COLOR, bd=0, relief=SUNKEN)
        zoom_frame.grid(row=0, column=3, sticky="ns")

        HoverButton(
            zoom_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/rotate.png"),
            command=self._rotate,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=RIGHT, expand=True)
        HoverButton(
            zoom_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/fullscreen.png"),
            command=self._fit_to_screen,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=RIGHT, expand=True)

        self.zoom_label = Label(
            zoom_frame,
            bg=BACKGROUND_COLOR,
            bd=0,
            fg="white",
            font="Arial 8",
            text=f"Zoom {int(self.scale * 100)}%",
        )
        self.zoom_label.pack(side=RIGHT, expand=True)

        HoverButton(
            zoom_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/zoomout.png"),
            command=self._zoom_out,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=RIGHT, expand=True)
        HoverButton(
            zoom_frame,
            # image_path=os.path.join(ROOT_PATH, "resources/zoomin.png"),
            command=self._zoom_in,
            bg=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=HIGHLIGHT_COLOR,
        ).pack(side=RIGHT, expand=True)

        canvas_frame = Frame(pdf_frame, bg=BACKGROUND_COLOR, bd=1, relief=SUNKEN)
        canvas_frame.grid(row=1, column=0, sticky="news")

        self.canvas = DisplayCanvas(canvas_frame, page_height=h - 42, page_width=w - 70)
        self.canvas.pack()

        self.grid(row=0, column=0, sticky="news")
        # noinspection PyUnresolvedReferences
        self.master.minsize(height=h, width=w)
        # noinspection PyUnresolvedReferences
        self.master.maxsize(height=h, width=w)

    def _clear(self):
        if self.pdf is None:
            return
        self.canvas.reset()
        self._update_page()

    def _first_page(self):
        pass

    def _prev_page(self):
        pass

    def _next_page(self):
        pass

    def _last_page(self):
        pass

    def _rotate(self):
        pass

    def _zoom_out(self):
        pass

    def _zoom_in(self):
        pass

    def _open_file(self):
        pass

    def _open_dir(self):
        pass

    def _next_file(self):
        pass

    def _prev_file(self):
        pass

    def _help(self):
        pass

    def _fit_to_screen(self):
        pass

    def _update_page(self):
        pass


if __name__ == "__main__":
    nn = PdfViewer()
    print(nn)
