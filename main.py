from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(pdfs, pdf_final):

    pdf_escritor = PdfWriter()

    for pdf in pdfs:
        with open(pdf, 'rb') as arq:
            pdf_leitor = PdfReader(arq)

            for pg_num in range(len(pdf_leitor.pages)):
                pagina = pdf_leitor.pages[pg_num]
                pdf_escritor.add_page(pagina)

    with open(pdf_final, 'wb') as arq:
        pdf_escritor.write(arq)

    print(f'PDF fundido como : {pdf_final}')

if __name__ == '__main__':
    arqs_pdf = ['arq1.pdf', 'arq2.pdf']
    arq_final = 'pdf_final.pdf'
    merge_pdfs(arqs_pdf, arq_final)

