# RAG Project

## Project Structure

 - [`.editorconfig`](#editorconfig)
 - [`pyproject.toml`](#pyproject-toml)
<!---
[WHITESPACE RULES]
- Same topic = "10" Whitespace character.
- Different topic = "50" Whitespace character.
--->


















































<!--- ( .editorconfig ) --->

---

<div id="editorconfig"></div>

## `.editorconfig`

O arquivo [.editorconfig](../.editorconfig) é usado para **padronizar o estilo de código** entre diferentes editores e IDEs (como VS Code, PyCharm, Sublime, etc.).

Ele garante que, independentemente de quem edite o código e onde, as regras de formatação — como indentação, codificação de caracteres e finais de linha — sejam consistentes em todo o projeto.

[.editorconfig](../.editorconfig)
```yaml
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8

# 4 space indentation
[*.{py,html, js}]
indent_style = space
indent_size = 4

# 2 space indentation
[*.{json,y{a,}ml,cwl}]
indent_style = space
indent_size = 2
```

 - `root = true`
   - ➡️ Indica que este é o arquivo `.editorconfig` principal.
   - Ou seja, o EditorConfig não deve procurar configurações em diretórios superiores.
   - Se houvesse outro `.editorconfig` acima na hierarquia, ele seria ignorado.

```yaml
[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
```

 - `[*]`
   - ➡️ Essa seção aplica-se a todos os arquivos (`*` é um curinga que significa “qualquer nome e extensão”).
   - Tudo o que vier abaixo até outra seção será aplicado globalmente.
 - `end_of_line = lf`
   - ➡️ Define o tipo de quebra de linha a ser usado:
     - lf = Line Feed (Unix/Linux/Mac)
     - crlf = Carriage Return + Line Feed (Windows)
   - 👉 Aqui, está sendo forçado o estilo Unix (LF), mesmo que alguém edite no Windows.
 - `insert_final_newline = true`
   - ➡️ Garante que haverá uma linha em branco no final do arquivo.
   - Muitos compiladores e ferramentas de versionamento esperam isso (boas práticas em Unix).
 - `charset = utf-8`
   - ➡️ Define o conjunto de caracteres padrão para todos os arquivos: *UTF-8*, o mais usado atualmente.
   - Isso evita erros de acentuação ou caracteres especiais ao abrir o arquivo em diferentes sistemas.

```yaml
# 4 space indentation
[*.{py,html, js}]
indent_style = space
indent_size = 4
```

 - `[*.{py,html, js}]`
   - ➡️ Aplica estas regras a arquivos com extensões `.py`, `.html` e `.js`.
   - O `{}` indica um grupo de extensões.
 - `indent_style = space`
   - ➡️ Usa espaços em vez de tabs para indentar o código.
 - `indent_size = 4`
   - ➡️ Define que cada nível de indentação terá 4 espaços.

```yaml
# 2 space indentation
[*.{json,y{a,}ml,cwl}]
indent_style = space
indent_size = 2
```

> **NOTE:**  
> Segue a mesma lógico do bloco anterior, porém, para arquivos com extensões `.json`, `.y{a,}ml` e `.cwl` e `indentação de 2 espaços`.


















































<!--- ( pyproject.toml ) --->

---

<div id="pyproject-toml"></div>

## `pyproject.toml`

O arquivo `pyproject.toml` é um arquivo de configuração padrão para projetos Python.
Ele centraliza informações sobre:

 - Dependências (bibliotecas necessárias para rodar o projeto);
 - Configuração de build (empacotamento e instalação);
 - Ferramentas de desenvolvimento (como Black, isort, Flake8, pytest, mypy, entre outras);
 - Metadados do projeto (nome, versão, autor, licença, etc.).

> **📦 Em resumo:**  
> O pyproject.toml é o coração da configuração moderna de um projeto Python.

#### 🏗️ Por que ele foi criado

Antes do `pyproject.toml`, cada ferramenta tinha seu próprio arquivo:

 - `setup.py` (empacotamento e distribuição);
 - `requirements.txt` (dependências);
 - `tox.ini` / `.flake8` / `pytest.ini` (configurações de ferramentas).

Isso tornava os projetos fragmentados e difíceis de manter.

> **👉 A partir do PEP 518 (e depois PEP 621)**  
> O Python passou a adotar o `TOML` como formato de configuração padrão — assim, tudo fica unificado em um só arquivo.














---

**Rodrigo** **L**eite da **S**ilva - **rodirgols89**
