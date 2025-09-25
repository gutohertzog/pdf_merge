""" módulo principal """

from .classes import Aplicativo


if __name__ == "__main__":
    app: Aplicativo = Aplicativo()
    app.mainloop()
