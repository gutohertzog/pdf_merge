""" módulo responsável pela GUI do projeto """

from tkinter import Menu, Tk
from tkinter import BOTTOM, LEFT
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.ttk import Button, Entry, Frame, Label
from PyPDF2 import PdfReader, PdfWriter, errors
from language import IDIOMAS

class Aplicativo(Tk):
    """ classe do aplicativo principal """

    def __init__(self):
        super().__init__()
        self.idioma = IDIOMAS['pt-br']
        self.frames = []
        self.pdfs = []
        self.tipo_arq = [("Arquivos PDF", "*.pdf")]

    # métodos de criação da UI
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

        menu_idioma = Menu(menu_opcoes, tearoff=0)
        menu_opcoes.add_cascade(menu=menu_idioma, label=self.idioma['language'])

        for chave, valor in IDIOMAS.items():
            menu_idioma.add_radiobutton(
                label=valor['acronym'],
                variable=self.idioma,
                value=chave,
                command=self.troca_idioma)

    def titulo(self):
        """ define a etiqueta de título """
        lbl_titulo = Label(self, text=self.idioma['titulo'])
        lbl_titulo.pack()

    def botao_juntar(self):
        """ define o botão de juntar os PDFs """
        btn_juntar = Button(
            self, text=self.idioma['merge'], command=self.merge_pdfs)
        btn_juntar.pack(side=BOTTOM)

    def frame_botoes(self):
        """ define o frame para colocar os 3 botões de ação """
        frm_botoes = Frame(self)
        btn_novo_pdf = Button(
            frm_botoes, text=self.idioma['load'], command=self.cria_frame)
        btn_novo_pdf.pack(side=LEFT)
        btn_remove_pdf = Button(
            frm_botoes, text=self.idioma['remove'], command=self.apaga_frame)
        btn_remove_pdf.pack(side=LEFT)
        btn_limpar = Button(
            frm_botoes, text=self.idioma['clear'], command=self.limpar_pdfs)
        btn_limpar.pack(side=LEFT)
        frm_botoes.pack()

    # métodos de ação
    def apaga_frame(self):
        """ função para apagar o último frame da pilha; funciona como FILO """
        if self.frames:
            para_apagar = self.frames.pop()
            self.pdfs.pop()
            para_apagar.destroy()
            self.update()

    def limpar_pdfs(self):
        """ remove todos os PDFs adicionados previamente """
        for frame in self.frames:
            frame.destroy()
        self.frames = []
        self.pdfs = []
        self.update()

    def cria_frame(self):
        """ abre a janela para carregar novo PDF e adciona o frame """
        arq_path = askopenfilename(
                title=self.idioma['select'],
                filetypes=self.tipo_arq)

        if arq_path:
            frm_novo = Frame(self)
            self.pdfs.append(arq_path)
            arq = arq_path.split('/')[-1]
            ent_arq = Entry(frm_novo)
            ent_arq.insert(0, arq)
            ent_arq.grid(row=0, column=0)
            frm_novo.pack()

            self.frames.append(frm_novo)

    def troca_idioma(self):
        """ método para trocar o idioma do aplicativo """
        self.update()

    def merge_pdfs(self):
        """ método para realizar a fusão """
        if len(self.pdfs) < 2:
            showwarning(self.idioma['warning'], self.idioma['two-or-more'])
            return

        pdf_escritor = PdfWriter()
        pdf_final = asksaveasfile(filetypes=self.tipo_arq)

        for pdf in self.pdfs:
            with open(pdf, 'rb') as arq:
                try:
                    print(f'{pdf = }')
                    pdf_leitor = PdfReader(arq)
                except errors.EmptyFileError as erro:
                    showerror(self.idioma['error'], self.idioma['error_msg'])
                    print(f'{erro = }')
                    return

                for pagina in pdf_leitor.pages:
                    pdf_escritor.add_page(pagina)

        with open(pdf_final.name, 'wb') as arq:
            pdf_escritor.write(arq)

        nome = pdf_final.name.split('/')
        showinfo(
            self.idioma['success'],
            self.idioma['success_msg'] + nome[-1])

if __name__ == '__main__':
    app = Aplicativo()
    app.conf_app()
    app.menu()
    app.titulo()
    app.frame_botoes()
    app.botao_juntar()
    app.mainloop()
