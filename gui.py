from tkinter import Button, Entry, Frame, Label, Tk
from tkinter import BOTTOM
from tkinter.filedialog import askopenfilename

fonte = ('Arial',24)

frames = []
indice = 0
pdfs = []

def apaga_frame(i):
    print(f'{i = }')
    para_apagar = frames[i]
    del frames[i]
    para_apagar.destroy()
    print(f'{len(frames) = }')
    print(f'{pdfs = }')
    janela.update()

def cria_frame():
    global indice
    frm_novo = Frame(janela)

    arq_path = askopenfilename(
            title='Selecione o Arquivo',
            filetypes=[("Arquivos PDF", "*.pdf")])

    if arq_path:
        pdfs.append(arq_path)
        arq = arq_path.split('/')[-1]
        ent_arq = Entry(frm_novo, font=fonte)
        ent_arq.insert(0, arq)
        ent_arq.grid(row=0, column=0)
        #btn_edita = Button(frm_novo, text='E', font=fonte)
        #btn_edita.grid(row=0, column=1)
        btn_remove = Button(
            frm_novo,
            text='A',
            font=fonte,
            command=lambda:apaga_frame(indice))
        indice += 1
        btn_remove.grid(row=0, column=1)
        frm_novo.pack()

        frames.append(frm_novo)
        print(f'{len(frames) = }')
        print(f'{pdfs = }')

janela = Tk()

janela.title('Juntador PDFs')
janela.minsize(300,400)

lbl_titulo = Label(janela, text="Bem-vindo ao Juntador de PDFs", font=fonte)
lbl_titulo.pack()

btn_teste = Button(janela, text='cria frame', command=cria_frame, font=fonte)
btn_teste.pack()

btn_juntar = Button(janela, text='Juntar', font=fonte)
btn_juntar.pack(side=BOTTOM)

janela.mainloop()

