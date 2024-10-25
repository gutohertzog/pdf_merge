from tkinter import Menu, Tk
from tkinter.ttk import Button, Entry, Frame, Label
from tkinter import BOTTOM, LEFT
from tkinter.filedialog import askopenfilename
from language import IDIOMAS

class Aplicativo(Tk):
    def __init__(self):
        super().__init__()
        self.idioma = IDIOMAS['pt-br']
        self.frames = []
        self.pdfs = []

    # métodos de criação
    def conf_app(self):
        """ método com as configurações da janela """
        self.title(self.idioma['titulo-janela'])
        self.minsize(480, 640)

    def menu(self):
        """ método com a configuração do menu superior """
        main_menu = Menu(self)
        self.config(menu=main_menu)

        menu_opcoes = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(menu=menu_opcoes, label=self.idioma['opcoes'])

        menu_opcoes.add_command(label=self.idioma['sair'], command=self.quit)

    def titulo(self):
        lbl_titulo = Label(self, text=self.idioma['titulo'])
        lbl_titulo.pack()

    def botao_juntar(self):
        self.btn_juntar = Button(self, text=self.idioma['merge'], state='disable')
        self.btn_juntar.pack(side=BOTTOM)


    def frame_botoes(self):
        frm_botoes = Frame(self)
        btn_novo_pdf = Button(frm_botoes, text=self.idioma['load'], command=self.cria_frame)
        btn_novo_pdf.pack(side=LEFT)
        btn_remove_pdf = Button(frm_botoes, text=self.idioma['remove'], command=self.apaga_frame)
        btn_remove_pdf.pack(side=LEFT)
        btn_limpar = Button(frm_botoes, text=self.idioma['clear'], command=self.limpar_pdfs)
        btn_limpar.pack(side=LEFT)
        frm_botoes.pack()

    # métodos de ação
    def apaga_frame(self):
        para_apagar = self.frames.pop()
        self.pdfs.pop()
        para_apagar.destroy()
        self.toggle_btn()
        self.janela.update()

    def limpar_pdfs(self):
        for frame in self.frames:
            frame.destroy()
        self.frames = []
        self.pdfs = []
        self.toggle_btn()
        self.janela.update()

    def toggle_btn(self):
        if len(self.pdfs) > 1:
            self.btn_juntar['state'] = 'normal'
        else:
            self.btn_juntar['state'] = 'disabled'

    def cria_frame(self):
        arq_path = askopenfilename(
                title='Selecione o Arquivo',
                filetypes=[("Arquivos PDF", "*.pdf")])

        if arq_path:
            frm_novo = Frame(self)
            self.pdfs.append(arq_path)
            arq = arq_path.split('/')[-1]
            ent_arq = Entry(frm_novo)
            ent_arq.insert(0, arq)
            ent_arq.grid(row=0, column=0)
            frm_novo.pack()

            self.toggle_btn()

            self.frames.append(frm_novo)

if __name__ == '__main__':
    app = Aplicativo()
    app.conf_app()
    app.menu()
    app.titulo()
    app.frame_botoes()
    app.botao_juntar()
    app.mainloop()

