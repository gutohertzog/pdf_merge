""" módulo responsável pela GUI do projeto """

from tkinter import Menu, Tk
from tkinter import BOTTOM, LEFT
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showinfo, showwarning
from tkinter.ttk import Button, Entry, Frame, Label
from PyPDF2 import PdfReader, PdfWriter
from language import IdiomaAplicativo

class Aplicativo(Tk, IdiomaAplicativo):
    """ classe do aplicativo principal """

    def __init__(self, idioma='pt-br'):
        Tk.__init__(self)
        IdiomaAplicativo.__init__(self, idioma)

        self.frames:list = []
        self.pdfs:list = []
        self.tipo_arq:list = [("Arquivos PDF", "*.pdf")]
        self.nome_novo_pdf:str = ''

        # cria a interface
        self.configura_aplicativo()
        self.cria_widgets()
        self.cria_menu()

        # atualiza o idioma da interface
        self.atualiza_interface()

    # métodos de criação da UI
    def configura_aplicativo(self):
        """ método com as configurações da janela """
        self.geometry('480x360')
        self.iconbitmap('assets/ufrgs.ico')
        self.maxsize(480, 640)
        self.minsize(480, 360)

    def cria_menu(self):
        """ método com a configuração do menu superior """
        self.barra_menu = Menu(self)
        self.menu_opcoes = Menu(self.barra_menu, tearoff=0)
        self.menu_idioma = Menu(self.menu_opcoes, tearoff=0)

        self.barra_menu.add_cascade(menu=self.menu_opcoes)

        self.menu_opcoes.add_cascade(menu=self.menu_idioma)
        self.menu_opcoes.add_command(command=self.quit)

        self.menu_idioma.add_command(command=lambda: self.define_texto('pt-br'))
        self.menu_idioma.add_command(command=lambda: self.define_texto('en-us'))

        self.config(menu=self.barra_menu)

    def cria_widgets(self):
        """ cria todos os widgets padrão do aplicativo """
        self.lbl_titulo = Label(self)
        self.lbl_titulo.pack()

        self.btn_juntar = Button(self, command=self.merge_pdfs)
        self.btn_juntar.pack(side=BOTTOM)

        frm_botoes = Frame(self)
        self.btn_novo_pdf = Button(frm_botoes, command=self.cria_frame)
        self.btn_novo_pdf.pack(side=LEFT)
        self.btn_remove_pdf = Button(frm_botoes, command=self.apaga_frame)
        self.btn_remove_pdf.pack(side=LEFT)
        self.btn_limpar = Button(frm_botoes, command=self.limpar_pdfs)
        self.btn_limpar.pack(side=LEFT)
        frm_botoes.pack()

    def atualiza_interface(self):
        """ método usado para criar os textos com base no idioma escolhido """
        self.title(self.pega_texto('title-window'))

        # atualiza os widgets
        self.lbl_titulo['text'] = self.pega_texto('title')
        self.btn_juntar['text'] = self.pega_texto('merge')
        self.btn_novo_pdf['text'] = self.pega_texto('load')
        self.btn_remove_pdf['text'] = self.pega_texto('remove')
        self.btn_limpar['text'] = self.pega_texto('clear')

        # atualiza os menus
        self.barra_menu.entryconfig(1, label=self.pega_texto('options'))

        self.menu_opcoes.entryconfig(0, label=self.pega_texto('language'))
        self.menu_opcoes.entryconfig(1, label=self.pega_texto('exit'))

        self.menu_idioma.entryconfig(0, label=self.pega_texto('lang_pt_br'))
        self.menu_idioma.entryconfig(1, label=self.pega_texto('lang_en_us'))

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
                title=self.pega_texto('select'),
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

    def escolhe_como_salvar(self):
        """ método para pegar o nome do novo PDF, testar se foi inserido
        a extensão .pdf nele; insere caso não exista

        o arquivo é aberto como leitura, pois apenas o seu caminho e nome são
        necessários, o 'mode' original é como escrita e isso apaga o arquivo
        de origem, caso tenha sido escolhido para ser também o destino, isso
        ajuda a evitar o EmptyFileError levantado
        """
        novo_pdf = asksaveasfile(mode='r', filetypes=self.tipo_arq)

        # nenhum nome foi escolhido para salvar
        # (janela fechada com Cancel ou no X)
        if not novo_pdf:
            self.nome_novo_pdf = ''
            return

        self.nome_novo_pdf = novo_pdf.name

        # adiciona a extensão .pdf caso ainda não tenha
        if '.pdf' != self.nome_novo_pdf[-4:]:
            self.nome_novo_pdf += '.pdf'

    def merge_pdfs(self):
        """ método para realizar a fusão """
        if len(self.pdfs) < 2:
            showwarning(self.pega_texto('warning'), self.pega_texto('two-or-more'))
            return

        self.escolhe_como_salvar()
        if not self.nome_novo_pdf:
            showwarning(self.pega_texto('warning'), self.pega_texto('no-name'))
            return

        pdf_escritor = PdfWriter()
        for pdf in self.pdfs:
            with open(pdf, 'rb') as arq:
                pdf_leitor = PdfReader(arq)

                for pagina in pdf_leitor.pages:
                    pdf_escritor.add_page(pagina)

        with open(self.nome_novo_pdf, 'wb') as arq:
            pdf_escritor.write(arq)

        nome = self.nome_novo_pdf.split('/')
        showinfo(
            self.pega_texto('success'),
            self.pega_texto('success-msg') + nome[-1])

if __name__ == '__main__':
    app = Aplicativo()
    app.mainloop()
