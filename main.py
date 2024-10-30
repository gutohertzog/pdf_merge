""" módulo principal """

__author__ = "Augusto Hertzog"
__version__ = "v1.0.0"
__url__ = "https://github.com/gutohertzog/pdf-merge"

from gui import Aplicativo


if __name__ == '__main__':
    app = Aplicativo()
    app.mainloop()
