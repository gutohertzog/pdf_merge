# pdf-merge

Juntador de PDFs

Repositório para o programa de juntar dois ou mais arquivos PDFs em um arquivo. Ele usa o [Python](https://www.python.org/) e a interface gráfica [tkinter](https://docs.python.org/3/library/tkinter.html).
Repositório para guardar o programa em Tkinter que vai juntar dois ou mais arquivos PDFs.

Pacotes externos :
- [PyPDF2](https://pypi.org/project/PyPDF2/) para realizar a fusão dos arquivos;
- [pyinstaller](https://pypi.org/project/pyinstaller/) para criar o executável;
- Pillow para exibir as imagens;

## preparação

Para preparar o ambiente e realizar alterações no projeto, execute o arquivo [setup-win.bat](setup-win.bat) para sistemas Windows e [setup-unix.sh](setup-unix.sh) para Linux / macOS.

Ele vai remover (caso não exista) a pasta `.venv` que é usada para configurar o ambiente virtual, criará uma nova e instalará as [dependências](requisitos.txt) para que o projeto possa ser executado diretamente do fonte.

Uma vez criada a pasta do ambiente virtual, é preciso ativá-la :
- Windows : `.venv\Scripts\activate`
- Linux / macOS : `source .venv/bin/activate`

Para executar, basta digitar no terminal / prompt de comando :

```bash
pdf-merge❯ python main.py
```

## build

Para criar o executável, é preciso executar o `pyinstaller` a partir do Terminal/Prompt de Comando. Isso vai criar um executável que pode ser distribuído.

### Linux

```bash
pyinstaller --onefile --add-data "assets/cpd-logo.jpg:assets" --hidden-import="PIL._tkinter_finder" --noconsole main.py
```

### Windows

```bash
pyinstaller --onefile --icon "assets/ufrgs.ico" --add-data "assets/cpd-logo.jpg:assets" --add-data "assets/ufrgs.ico:assets" --hidden-import="PIL._tkinter_finder" --noconsole main.py
```

## todo

- [ ] adicionar remoção individual do frame (atualmente funciona com FILO);
- [ ] arrumar o tema das janelas (está apenas no widgets);
- [ ] adicionar mais idiomas (italiano e alemão);

## versões

- `v1.0.0` : lançada a primeira versão para Windows e Linux;

