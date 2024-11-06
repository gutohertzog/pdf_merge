""" módulo com a classe para guardar as opções de idiomas """

from .config import __author__

class IdiomaAplicativo:
    textos: dict[str, dict[str, str]] = {
        'pt-br': {
            'about': 'Sobre',
            'about-title-window': 'Sobre o Juntador',
            'clear': 'Limpar',
            'close': 'Fechar',
            'contributor': f'Um projeto de {__author__}',
            'dark': 'Escuro',
            'exit': 'Sair',
            'help': 'Ajuda',
            'lang_en_us': 'Inglês (EUA)',
            'lang_pt_br': 'Português (Brasil)',
            'language': 'Idioma',
            'light': 'Claro',
            'load': 'Carregar',
            'merge': 'Juntar',
            'no-name': 'Digite um nome válido para o novo PDF',
            'options': 'Opções',
            'pdf-files': 'Arquivos PDF',
            'project': 'Juntador de PDFs',
            'remove': 'Remover',
            'select': 'Selecione o Arquivo',
            'success': 'Sucesso',
            'success-msg': 'PDF juntado como :\n',
            'themes': 'Temas',
            'title': 'Bem-vindo ao Juntador de PDFs',
            'title-window': 'Juntador PDFs',
            'two-or-more': 'Escolha dois ou mais PDFs',
            'warning': 'Aviso',
            'wrong-name': 'Não escolha um arquivo PDF de origem como destino',
        },
        'en-us': {
            'about': 'About',
            'about-title-window': 'About Merger',
            'clear': 'Clear',
            'close': 'Close',
            'contributor': f'A project by {__author__}',
            'dark': 'Dark',
            'exit': 'Exit',
            'help': 'Help',
            'lang_en_us': 'English (USA)',
            'lang_pt_br': 'Portuguese (Brazil)',
            'language': 'Language',
            'light': 'Light',
            'load': 'Load',
            'merge': 'Merge',
            'no-name': 'Enter a valid name for the new PDF',
            'options': 'Options',
            'pdf-files': 'PDF Files',
            'project': 'PDFs Merger',
            'remove': 'Remove',
            'select': 'Select file',
            'success': 'Success',
            'success-msg': 'PDF merged as :\n',
            'themes': 'Themes',
            'title': 'Welcome to the PDFs Merger',
            'title-window': 'PDFs Merger',
            'two-or-more': 'Select two or more PDFs',
            'warning': 'Warning',
            'wrong-name': 'Do not select a source PDF file as the destination',
        }
    }

    def __init__(self, idioma:str='pt-br'):
        """ define o idioma padão """
        self.idioma:str = idioma

    def pega_texto(self, chave:str):
        return self.textos[self.idioma].get(chave, '')

    def define_texto(self, idioma):
        self.idioma = idioma
        self.atualiza_interface()

    def atualiza_interface(self):
        """ método a ser implementado pela classe filha para atualizar idioma
        da interface """
        pass
