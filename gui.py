from tkinter import Menu, Tk
from tkinter.ttk import Button, Entry, Frame, Label
from tkinter import BOTTOM, LEFT
from tkinter.filedialog import askopenfilename

frames = []
pdfs = []

def apaga_frame():
    global frames
    global pdfs
    para_apagar = frames.pop()
    pdfs.pop()
    para_apagar.destroy()
    toggle_btn()
    janela.update()

def limpar_pdfs():
    global frames
    global pdfs
    for frame in frames:
        frame.destroy()
    frames = []
    pdfs = []
    toggle_btn()
    janela.update()

def toggle_btn():
    global pdfs
    if len(pdfs) > 1:
        btn_juntar['state'] = 'normal'
    else:
        btn_juntar['state'] = 'disabled'

def cria_frame():
    arq_path = askopenfilename(
            title='Selecione o Arquivo',
            filetypes=[("Arquivos PDF", "*.pdf")])

    if arq_path:
        frm_novo = Frame(janela)
        pdfs.append(arq_path)
        arq = arq_path.split('/')[-1]
        ent_arq = Entry(frm_novo)
        ent_arq.insert(0, arq)
        ent_arq.grid(row=0, column=0)
        frm_novo.pack()

        toggle_btn()

        frames.append(frm_novo)

janela = Tk()

janela.title('Juntador PDFs')
janela.minsize(300,400)

menu_princ = Menu(janela)
janela.config(menu=menu_princ)

menu_sec = Menu(menu_princ, tearoff=0)
menu_princ.add_cascade(label='Opções', menu=menu_sec)
menu_sec.add_command(label='Sair', command=janela.quit)

lbl_titulo = Label(janela, text="Bem-vindo ao Juntador de PDFs")
lbl_titulo.pack()

frm_botoes = Frame(janela)
btn_novo_pdf = Button(frm_botoes, text='Carregar', command=cria_frame)
btn_novo_pdf.pack(side=LEFT)
btn_remove_pdf = Button(frm_botoes, text='Remover', command=apaga_frame)
btn_remove_pdf.pack(side=LEFT)
btn_limpar = Button(frm_botoes, text='Limpar', command=limpar_pdfs)
btn_limpar.pack(side=LEFT)
frm_botoes.pack()

btn_juntar = Button(janela, text='Juntar', state='disable')
btn_juntar.pack(side=BOTTOM)

janela.mainloop()

