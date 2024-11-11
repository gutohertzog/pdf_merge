""" módulo responsável pela GUI do projeto """

import os
import platform
import sys
import webbrowser
import themes.sv_ttk as sv_ttk
from tkinter import Tk, Toplevel
from tkinter import BOTTOM, LEFT, RIGHT, X
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.messagebox import showinfo, showwarning
from tkinter.ttk import Button, Entry, Frame, Label, Separator, Style
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

        self.frames:list = []
        self.pdfs:list = []
        self.tipo_arq:list = [(self.pega_texto('pdf-files'), '*.pdf')]
        self.sistema = platform.system()

        # cria a interface
        self.configura_aplicativo()
        self.cria_frame_menu()
        self.cria_frame_principal()
        sv_ttk.set_theme("light")  # interface clara padrão

        self.atualiza_idioma_main()  # idioma padrão pt-br

    def configura_aplicativo(self):
        """ método com as configurações da janela """
        self.geometry('480x360')
        # linux não lidam bem com ícones no aplicativo
        if self.sistema == 'Windows':
            icone_path = self.caminho_arquivo('assets', 'ufrgs.ico')
            self.iconbitmap(icone_path)
        self.maxsize(480, 640)
        self.minsize(480, 360)

    def caminho_arquivo(self, pasta, nome_arquivo):
        """ busca o caminho do arquivo, compatível com o PyInstaller """
        # verifica se está em modo executável
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, pasta, nome_arquivo)

    def cria_frame_menu(self):
        """ cria os widgets para o menu do aplicativo """
        self.frm_menu = Frame(self)
        self.frm_menu.pack(fill=X)

        self.btn_opcoes = Button(
            self.frm_menu, command=self.abre_janela_opcoes)
        self.btn_opcoes.pack(side=LEFT, padx=5, pady=(5, 0))

        self.btn_sobre = Button(
            self.frm_menu, command=self.abre_janela_sobre)
        self.btn_sobre.pack(side=LEFT, padx=5, pady=(5, 0))

        self.btn_sair = Button(
            self.frm_menu, command=self.quit)
        self.btn_sair.pack(side=RIGHT, padx=5, pady=(5, 0))

    def cria_frame_principal(self):
        """ cria os widgets envolvidos no merge dos PDFs """
        self.frm_main = Frame(self)
        self.frm_main.pack(expand=True, fill='both')

        Separator(
            self.frm_main,
            orient='horizontal').pack(fill=X, pady=(5, 10))

        self.lbl_titulo = Label(self.frm_main, font=('Arial', 16))
        self.lbl_titulo.pack(pady=(0, 10))

        self.btn_juntar = Button(
            self.frm_main, command=self.merge_pdfs)
        self.btn_juntar.pack(side=BOTTOM, pady=10)

        frm_botoes = Frame(self.frm_main)
        frm_botoes.pack()

        self.btn_novo_pdf = Button(
            frm_botoes, command=self.cria_frame)
        self.btn_novo_pdf.pack(side=LEFT, padx=10)
        self.btn_remove_pdf = Button(
            frm_botoes, command=self.apaga_frame)
        self.btn_remove_pdf.pack(side=LEFT, padx=10)
        self.btn_limpar = Button(
            frm_botoes, command=self.limpar_pdfs)
        self.btn_limpar.pack(side=LEFT, padx=10)

    def atualiza_interface(self):
        """ método usado para criar e atualizar os textos da aplicação. essa
        separação dos métodos de atualização é necessária porque não é possível
        atualizar o idioma dos widgets da janela de opções antes de ter sido
        criada. """
        self.atualiza_idioma_main()
        self.atualiza_idioma_janela_menu()

    def atualiza_idioma_janela_menu(self):
        """ método usado para criar e atualizar os textos da janela aberta pelo
        menu com base no idioma escolhido """
        self.janela_opcoes.title(self.pega_texto('options'))

        # botões e label do tema
        self.lbl_temas['text'] = self.pega_texto('themes')
        self.btn_claro['text'] = self.pega_texto('light')
        self.btn_escuro['text'] = self.pega_texto('dark')
        self.btn_fechar['text'] = self.pega_texto('close')

        # botões e label dos idiomas
        self.lbl_idioma['text'] = self.pega_texto('language')
        self.btn_pt_br ['text'] = self.pega_texto('lang_pt_br')
        self.btn_en_us ['text'] = self.pega_texto('lang_en_us')
        self.btn_de ['text'] = self.pega_texto('lang_de')
        self.btn_it ['text'] = self.pega_texto('lang_it')

    def atualiza_idioma_main(self):
        """ método usado para criar e atualizar os textos da janela principal
        com base no idioma escolhido """
        self.title(self.pega_texto('title-window'))

        # botões de menu
        self.btn_opcoes['text'] = self.pega_texto('options')
        self.btn_sobre['text'] = self.pega_texto('about')
        self.btn_sair['text'] = self.pega_texto('exit')

        # botões e label do frame principal
        self.lbl_titulo['text'] = self.pega_texto('title')
        self.btn_juntar['text'] = self.pega_texto('merge')
        self.btn_novo_pdf['text'] = self.pega_texto('load')
        self.btn_remove_pdf['text'] = self.pega_texto('remove')
        self.btn_limpar['text'] = self.pega_texto('clear')

        # variáveis
        self.tipo_arq:list = [(self.pega_texto('pdf-files'), '*.pdf')]

    def aplicar_tema(self, tema):
        """ aplica o tema escolhido pelo usuário """
        if tema == 'claro':
            sv_ttk.use_light_theme()
        else:
            sv_ttk.use_dark_theme()

        if self.sistema == 'Windows':
            self.aplica_tema_barra_titulo()

    def aplica_tema_barra_titulo(self):
        """ devido a uma limitação do Windows, é necessário usar essa função
        para ser possível alterar também a barra de título no Windows
        https://github.com/rdbende/Sun-Valley-ttk-theme#dark-mode-title-bar-on-windows """
        import pywinstyles

        versao = sys.getwindowsversion()

        if versao.major == 10 and versao.build >= 22000:
            # define a cor da barra de título para a cor de fundo no Windows 11
            # para melhor aparência
            pywinstyles.change_header_color(
                self, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif versao.major == 10:
            pywinstyles.apply_style(
                self, "dark" if sv_ttk.get_theme() == "dark" else "normal")

            # gambiara para atualizar a cor da barra de título no Windows 10
            # (não atualiza instantaneamente como no Windows 11)
            self.wm_attributes("-alpha", 0.99)
            self.wm_attributes("-alpha", 1)

    def abre_janela_opcoes(self):
        """ abre um toplevel com as opções disponíveis """
        self.janela_opcoes = Toplevel(self)
        self.janela_opcoes.minsize(200, 275)
        self.janela_opcoes.transient(self)
        self.janela_opcoes.grab_set()

        self.lbl_temas = Label(self.janela_opcoes)
        self.lbl_temas.pack(pady=(10, 5))
        self.btn_claro = Button(
            self.janela_opcoes, command=lambda: self.aplicar_tema('claro'))
        self.btn_claro.pack(pady=5)
        self.btn_escuro = Button(
            self.janela_opcoes, command=lambda: self.aplicar_tema('escuro'))
        self.btn_escuro.pack(pady=5)

        Separator(
            self.janela_opcoes,
            orient='horizontal').pack(fill=X, padx=10, pady=15)

        self.lbl_idioma = Label(self.janela_opcoes)
        self.lbl_idioma.pack(pady=5)
        self.btn_pt_br = Button(
            self.janela_opcoes,command=lambda: self.define_texto('pt-br'))
        self.btn_pt_br.pack(pady=5)
        self.btn_en_us = Button(
            self.janela_opcoes, command=lambda: self.define_texto('en-us'))
        self.btn_en_us.pack(pady=5)
        self.btn_de = Button(
            self.janela_opcoes, command=lambda: self.define_texto('de'))
        self.btn_de.pack(pady=5)
        self.btn_it = Button(
            self.janela_opcoes, command=lambda: self.define_texto('it'))
        self.btn_it.pack(pady=5)

        Separator(
            self.janela_opcoes,
            orient='horizontal').pack(fill=X, padx=10, pady=15)

        self.btn_fechar = Button(
            self.janela_opcoes, command=self.janela_opcoes.destroy)
        self.btn_fechar.pack(pady=(5, 10))

        self.atualiza_interface()

    def abre_janela_sobre(self):
        """ cria uma nova janela para mostrar os dados do aplicativo. tornando
        a janela grab_set, evita que se tenha a janela aberta quando for tentar
        alterar o texto e também evita que várias instâncias sejam criadas de
        qualquer janela. """

        janela_sobre = Toplevel(self)
        janela_sobre.title(self.pega_texto('about-title-window'))
        janela_sobre.geometry('400x300')
        janela_sobre.resizable(False, False)
        janela_sobre.transient(self)
        janela_sobre.grab_set()

        try:
            img_caminho = self.caminho_arquivo('assets', 'cpd-logo.jpg')
            img_logo = Image.open(img_caminho)
            img_largura, img_altura = img_logo.size
            img_logo = img_logo.resize(
                (img_largura//6, img_altura//6), Image.LANCZOS)
            logo = ImageTk.PhotoImage(img_logo)
            lbl_logo = Label(janela_sobre, image=logo, cursor='hand2')
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
            self.pega_texto('project') +
            ' ('+__version__+')' +
            '\n\nUFRGS\n\n' +
            __url__
        )
        lbl_info = Label(
                janela_sobre, text=texto_info, justify="center", cursor="hand2")
        lbl_info.pack(pady=10)

        # evento de clique para abrir o link do repositório no navegador
        lbl_info.bind(
            '<Button-1>',
            lambda e: webbrowser.open(__url__))

        btn_fechar = Button(
                janela_sobre,
                text=self.pega_texto('close'),
                command=janela_sobre.destroy)
        btn_fechar.pack(pady=10)

        # necessário para mostrar as imagens
        janela_sobre.wait_window(janela_sobre)

    def apaga_frame(self):
        """ função para apagar o último frame da pilha;
        até o momento, funciona como FILO """
        if self.frames:
            para_apagar = self.frames.pop()
            self.pdfs.pop()
            para_apagar.destroy()
            self.update()

    def limpar_pdfs(self):
        """ remove todos os PDFs adicionados """
        for frame in self.frames:
            frame.destroy()
        self.frames = []
        self.pdfs = []
        self.update()

    def cria_frame(self):
        """ abre a janela para carregar novo PDF e adcionar um novo frame """
        arq_path = askopenfilename(
                title=self.pega_texto('select'),
                filetypes=self.tipo_arq)

        if arq_path:
            frm_novo = Frame(self.frm_main)
            self.pdfs.append(arq_path)
            arq = arq_path.split('/')[-1]
            ent_arq = Entry(frm_novo, font=('Arial', 12), justify='center')
            ent_arq.insert(0, arq)
            ent_arq['state'] = 'disabled'
            ent_arq.grid(row=0, column=0)
            frm_novo.pack(pady=5)

            self.frames.append(frm_novo)

    def merge_pdfs(self):
        """
        <(-_-<)            (>-_-)>    FUU
          ^(-_-)^         ^(-_-)^     UUU
              (>-_-)>  <(-_-<)        UUU
             <(-_-<)    (>-_-)>       SÃO
               (>-_-)><(-_-<)         HA!
                    (Ò-Ó)
        """
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
