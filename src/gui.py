""" módulo responsável pela GUI do projeto """

import os
import platform
import sys
import webbrowser
from tkinter import Menu, Tk, Toplevel
from tkinter import BOTTOM, LEFT
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showinfo, showwarning
from tkinter.ttk import Button, Entry, Frame, Label, Style
from PIL import Image, ImageTk
from PyPDF2 import PdfReader, PdfWriter
from .language import IdiomaAplicativo
from .config import __version__, __url__

class Aplicativo(Tk, IdiomaAplicativo):
    """ classe do aplicativo principal """

    url_univ = 'https://www.ufrgs.br'

    def __init__(self, idioma='pt-br'):
        Tk.__init__(self)
        IdiomaAplicativo.__init__(self, idioma)
        self.estilo = Style(self)

        self.frames:list = []
        self.pdfs:list = []
        self.tipo_arq:list = [(self.pega_texto('pdf-files'), '*.pdf')]
        self.sistema = platform.system()

        # cria a interface
        self.configura_aplicativo()
        self.cria_widgets()
        self.cria_menu()

        # define o idioma da interface para o padrão pt-br
        self.atualiza_interface()

    # métodos de criação da UI
    def configura_aplicativo(self):
        """ método com as configurações da janela """
        self.geometry('480x360')
        # linux não lidam bem com ícones no aplicativo
        if self.sistema == 'Windows':
            icone_path = self.caminho_arquivo('ufrgs.ico')
            self.iconbitmap(icone_path)
        self.maxsize(480, 640)
        self.minsize(480, 360)

    def definir_tema_automatico(self):
        """ define um tema padrão com base no sistema operacional """

        if self.sistema == 'Windows':
            tema = 'vista' if 'vista' in self.estilo.theme_names() else 'clam'
        elif self.sistema == 'Darwin':
            tema = 'clam'
        elif self.sistema == 'Linux':
            tema = 'clam'
        else:
            tema = 'default'

        self.estilo.theme_use(tema)

    def caminho_arquivo(self, nome_arquivo):
        """ retorna o caminho do arquivo, compatível com o executável
        PyInstaller """
        # verifica se está em modo executável
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, 'assets', nome_arquivo)

    def cria_menu(self):
        """ método com a configuração do menu superior """
        self.barra_menu = Menu(self)
        # botões barra de menu
        self.menu_opcoes = Menu(self.barra_menu, tearoff=0)
        self.menu_ajuda = Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(menu=self.menu_opcoes)
        self.barra_menu.add_cascade(menu=self.menu_ajuda)

        # botões submenus
        self.menu_idioma = Menu(self.menu_opcoes, tearoff=0)
        self.menu_temas = Menu(self.menu_opcoes, tearoff=0)
        self.menu_sobre = Menu(self.menu_ajuda, tearoff=0)

        self.menu_opcoes.add_cascade(menu=self.menu_idioma)
        self.menu_opcoes.add_cascade(menu=self.menu_temas)
        self.menu_opcoes.add_command(command=self.quit)
        self.menu_ajuda.add_command(command=self.mostra_dados)

        self.menu_idioma.add_command(command=lambda: self.define_texto('pt-br'))
        self.menu_idioma.add_command(command=lambda: self.define_texto('en-us'))

        for tema in self.estilo.theme_names():
            self.menu_temas.add_command(
                label=tema.capitalize(),
                command=lambda t=tema: self.aplicar_tema(t)
            )

        self.config(menu=self.barra_menu)

    def cria_widgets(self):
        """ cria todos os widgets padrão do aplicativo """
        self.lbl_titulo = Label(self, font=('Arial', 16))
        self.lbl_titulo.pack(pady=10)

        self.btn_juntar = Button(
            self, command=self.merge_pdfs)
        self.btn_juntar.pack(side=BOTTOM, pady=10)

        frm_botoes = Frame(self)
        self.btn_novo_pdf = Button(
            frm_botoes, command=self.cria_frame)
        self.btn_novo_pdf.pack(side=LEFT, padx=10)
        self.btn_remove_pdf = Button(
            frm_botoes, command=self.apaga_frame)
        self.btn_remove_pdf.pack(side=LEFT, padx=10)
        self.btn_limpar = Button(
            frm_botoes, command=self.limpar_pdfs)
        self.btn_limpar.pack(side=LEFT, padx=10)
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
        # barra de menus
        self.barra_menu.entryconfig(1, label=self.pega_texto('options'))
        self.barra_menu.entryconfig(2, label=self.pega_texto('help'))

        # submenus
        self.menu_opcoes.entryconfig(0, label=self.pega_texto('language'))
        self.menu_opcoes.entryconfig(1, label=self.pega_texto('themes'))
        self.menu_opcoes.entryconfig(2, label=self.pega_texto('exit'))
        self.menu_idioma.entryconfig(0, label=self.pega_texto('lang_pt_br'))
        self.menu_idioma.entryconfig(1, label=self.pega_texto('lang_en_us'))
        self.menu_ajuda.entryconfig(0, label=self.pega_texto('about'))

        # variáveis
        self.tipo_arq:list = [(self.pega_texto('pdf-files'), '*.pdf')]

    def aplicar_tema(self, tema):
        """ aplica o tema escolhido pelo usuário """
        self.estilo.theme_use(tema)

    def mostra_dados(self):
        """ cria uma nova janela para mostrar os dados do aplicativo """

        janela_info = Toplevel(self)
        janela_info.title(self.pega_texto('about-title-window'))
        janela_info.geometry('400x300')
        janela_info.resizable(False, False)

        try:
            img_path = self.caminho_arquivo('cpd-logo.jpg')
            img_logo = Image.open(img_path)
            largura, altura = img_logo.size
            img_logo = img_logo.resize((largura//6, altura//6), Image.LANCZOS)
            logo = ImageTk.PhotoImage(img_logo)
            lbl_logo = Label(janela_info, image=logo, cursor='hand2')
            lbl_logo.image = logo
            lbl_logo.pack(pady=10)
            # evento de clique para abrir o link da UFRGS
            lbl_logo.bind(
                    '<Button-1>',
                    lambda e: webbrowser.open(Aplicativo.url_univ))
        except Exception as e:
            print(f'Não foi possível carregar o logo: {e}')

        texto_info = (
            self.pega_texto('contributor') + '\n\n' +
            self.pega_texto('project') + ' ('+__version__+')' +
            '\n\nUFRGS\n\n' + __url__
        )
        lbl_info = Label(
                janela_info, text=texto_info, justify="center", cursor="hand2")
        lbl_info.pack(pady=10)

        # evento de clique para abrir o link do repositório no navegador
        lbl_info.bind(
            '<Button-1>',
            lambda e: webbrowser.open(__url__))

        btn_fechar = Button(
                janela_info,
                text=self.pega_texto('close'),
                command=janela_info.destroy)
        btn_fechar.pack(pady=10)

        janela_info.wait_window(janela_info)

    # métodos de ação
    def apaga_frame(self):
        """ função para apagar o último frame da pilha;
        até o momento, funciona como FILO """
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
            ent_arq = Entry(frm_novo, font=('Arial', 12), justify='center')
            ent_arq.insert(0, arq)
            ent_arq['state'] = 'disabled'
            ent_arq.grid(row=0, column=0)
            frm_novo.pack(pady=5)

            self.frames.append(frm_novo)

    def merge_pdfs(self):
        """ método para realizar a fusão """
        if len(self.pdfs) < 2:
            showwarning(
                    self.pega_texto('warning'), self.pega_texto('two-or-more'))
            return

        pdf_escritor = PdfWriter()
        for pdf in self.pdfs:
            with open(pdf, 'rb') as arq:
                pdf_leitor = PdfReader(arq)

                for pagina in pdf_leitor.pages:
                    pdf_escritor.add_page(pagina)

        novo_pdf = asksaveasfile(
                filetypes=self.tipo_arq, defaultextension='.pdf')

        # nenhum nome foi escolhido para salvar
        # (janela fechada com Cancel ou no X)
        if not novo_pdf:
            showwarning(self.pega_texto('warning'), self.pega_texto('no-name'))
            return

        with open(novo_pdf.name, 'wb') as arq:
            pdf_escritor.write(arq)

        nome = novo_pdf.name.split('/')
        showinfo(
            self.pega_texto('success'),
            self.pega_texto('success-msg') + nome[-1])
