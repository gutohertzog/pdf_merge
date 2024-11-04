# pdf_merge

Juntador de PDFs

Repositório para o programa de juntar dois ou mais arquivos PDFs em um arquivo. Ele usa o [Python](https://www.python.org/) e a interface gráfica [tkinter](https://docs.python.org/3/library/tkinter.html).
Repositório para guardar o programa em Tkinter que vai juntar dois ou mais arquivos PDFs.

Pacotes externos :
- [PyPDF2](https://pypi.org/project/PyPDF2/) para realizar a fusão dos arquivos;
- [pyinstaller](https://pypi.org/project/pyinstaller/) para criar o executável;
- Pillow para exibir as imagens;

## preparação

Abaixo há a realação de comandos necessários para criar um ambiente virtual, ativá-lo e instalar as dependências.

### linux e macos

```bash
> python -m venv .venv
> source .venv/bin/activate
> pip install -r requisitos.txt
```

### windows

```powershell
> python -m venv .venv
> .venv\Scripts\activate
> pip install -r requisitos.txt
```

Para executar, basta digitar no terminal / prompt de comando :

```bash
pdf_merge❯ python main.py
```

## build

Para criar o executável, é preciso executar o `pyinstaller` a partir do Terminal/Prompt de Comando. Isso vai criar um executável que pode ser distribuído.

### linux

```bash
pyinstaller --onefile --add-data "assets/cpd-logo.jpg:assets" --hidden-import="PIL._tkinter_finder" --noconsole main.py
```

### windows

```powershell
pyinstaller --onefile --icon "assets/ufrgs.ico" --add-data "assets/cpd-logo.jpg:assets" --add-data "assets/ufrgs.ico:assets" --hidden-import="PIL._tkinter_finder" --noconsole main.py
```

## todo

- [ ] adicionar remoção individual do frame (atualmente funciona com FILO);
- [ ] arrumar o tema das janelas (está apenas no widgets);
- [ ] adicionar mais idiomas (italiano e alemão);

## versões

- `v1.0.3` : ajustes diversos e melhor organização;
- `v1.0.0` : lançada a primeira versão para Windows e Linux;
