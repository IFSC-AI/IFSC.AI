# IFSC.AI

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![Projeto](https://img.shields.io/badge/tipo-projeto%20acad%C3%AAmico-blue)

**Agente de Inteligência Artificial integrado ao WhatsApp para facilitar o acesso a informações sobre o IFSC Câmpus Chapecó.**

O IFSC.AI é um projeto acadêmico desenvolvido no Instituto Federal de Santa Catarina (IFSC), Câmpus Chapecó. A solução busca facilitar a orientação de estudantes, servidores, visitantes e comunidade externa por meio de um agente de IA acessível pelo WhatsApp e de um site informacional.

---

## Sobre o projeto

Encontrar informações sobre setores, serviços, espaços e procedimentos de uma instituição pode ser difícil quando os dados estão distribuídos entre diferentes canais.

O IFSC.AI propõe centralizar o acesso a essas informações por meio de um agente de IA integrado ao WhatsApp, utilizando uma base de conhecimento com informações institucionais verificadas.

O projeto também conta com um site de ajuda que apresenta a solução, explica como utilizar o agente e responde às dúvidas mais frequentes sobre seu funcionamento.

**Objetivo:** facilitar o acesso a informações institucionais do IFSC Câmpus Chapecó, oferecendo orientação inicial de maneira simples e acessível.

## Funcionalidades

- **Agente de IA no WhatsApp:** permite que os usuários enviem perguntas em linguagem natural.
- **Orientação institucional:** fornece informações sobre setores, blocos, cursos, serviços e procedimentos do câmpus, conforme os dados disponíveis na base de conhecimento.
- **Base de conhecimento:** organiza informações institucionais para apoiar as respostas do agente.
- **Central de ajuda:** apresenta instruções de uso, perguntas frequentes e informações sobre o projeto.
- **Integração com API própria:** permite que o site obtenha conteúdos armazenados no banco de dados, por meio de requisições HTTP e respostas em JSON.

> O backend, o banco de dados e a integração dinâmica do conteúdo do site estão em desenvolvimento.

## Arquitetura

O projeto é organizado em dois fluxos principais.

### 1. Site informacional

O frontend apresenta o conteúdo ao usuário, enquanto a API própria disponibiliza os dados armazenados no banco de dados.

\`\`\`text
Frontend (HTML, CSS e JavaScript)
                 |
                 | Requisição HTTP
                 v
          API própria (Flask)
                 |
                 | Consultas
                 v
             SQLite
                 |
                 | Dados em JSON
                 v
           Frontend atualizado
\`\`\`

### 2. Agente de IA no WhatsApp

O n8n coordena o fluxo de automação, a integração com o WhatsApp e a execução do agente de IA.

\`\`\`text
Usuário
   |
   v
WhatsApp
   |
   v
WhatsApp Business Platform
   |
   v
n8n
   |
   v
Agente de IA + Base de conhecimento
   |
   v
Geração da resposta
   |
   v
WhatsApp
   |
   v
Usuário
\`\`\`

A lógica de Inteligência Artificial fica no n8n. O backend em Python tem como finalidade fornecer a API do site e acessar os dados armazenados no banco de dados.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
| --- | --- |
| HTML5 | Estrutura das páginas web |
| CSS3 | Estilização e identidade visual |
| JavaScript | Interatividade e consumo da API |
| Python | Desenvolvimento do backend |
| Flask | Criação da API própria |
| SQLite | Armazenamento dos conteúdos do site |
| n8n | Orquestração dos fluxos e do agente de IA |
| WhatsApp Business Platform | Integração com o WhatsApp |
| Git e GitHub | Versionamento e colaboração |

O Flask e o SQLite integram a arquitetura planejada para o backend e o banco de dados.

## Estrutura do projeto

Estrutura prevista para a organização dos arquivos:

\`\`\`text
IFSC.AI/
├── frontend/
│   ├── index.html
│   ├── quem-nos-somos.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   └── ifsc_ai.db
│
├── README.md
└── ifscai.json
└── WireFrame site Help IFSC AI.pdf
\`\`\`

O arquivo `ifsc_ai.db` será utilizado para armazenar os dados do site. O banco pode ser criado automaticamente pelo backend na primeira execução.

A estrutura poderá ser ajustada conforme a implementação evoluir. Credenciais, tokens e outros dados sensíveis não devem ser incluídos no repositório.

## Site informacional

O site funciona como uma central de ajuda e não como uma segunda interface de conversação com o agente de IA.

Suas principais seções são:

- **Início:** apresentação do IFSC.AI e acesso ao WhatsApp.
- **Como usar:** instruções para iniciar uma conversa com o agente.
- **Quem nós somos:** apresentação do projeto e da equipe.
- **Perguntas frequentes:** respostas sobre o funcionamento e o escopo da solução.
- **Contato:** direcionamento para o agente e para os canais de atendimento pertinentes.

A identidade visual utiliza um tema escuro, com destaque em verde e a fonte EB Garamond.

## API e banco de dados

A API própria será responsável por disponibilizar os conteúdos do site em formato JSON. O JavaScript fará requisições assíncronas para buscar esses dados e atualizar os elementos da interface.

Os endpoints iniciais previstos são:

| Método | Endpoint | Finalidade |
| --- | --- | --- |
| GET | `/api/conteudo` | Consultar os textos das seções do site |
| GET | `/api/faq` | Consultar as perguntas frequentes |

Esses endpoints representam o contrato inicial planejado e deverão ser implementados no backend.

O banco SQLite armazenará os textos informativos, títulos, descrições, perguntas e respostas. Assim, o conteúdo poderá ser atualizado no banco sem exigir alterações manuais em cada trecho do HTML.

## Como executar

### Executar o frontend

Para visualizar a versão atual do site:

1. Clone o repositório ou baixe o código-fonte.
2. Abra a pasta do projeto no Visual Studio Code.
3. Abra a pasta `frontend`.
4. Execute o arquivo `index.html` com a extensão Live Server ou Live Preview.
5. Acesse o endereço local exibido pela extensão no navegador.

A visualização estática utiliza o conteúdo presente no HTML. A consulta dinâmica à API dependerá da conclusão e da configuração do backend.

### Executar o backend

A execução integrada do backend será documentada após a implementação da API Flask, incluindo a instalação das dependências, a inicialização do servidor e a configuração da conexão com o banco SQLite.

### Configurar o agente de IA

A execução do agente depende da configuração do fluxo no n8n, das credenciais necessárias e da integração com a WhatsApp Business Platform.

As credenciais devem ser configuradas no ambiente correspondente, sem serem publicadas no GitHub.

## Boas práticas e limitações

- As informações utilizadas pelo agente devem ter origem verificável e ser mantidas atualizadas.
- O agente não deve inventar informações institucionais.
- Quando não houver dados suficientes para responder com segurança, o usuário deverá ser orientado a procurar o setor responsável.
- A solução não substitui os canais oficiais nem o atendimento humano.
- A integração entre frontend, API, banco de dados e agente deve ser testada em um ambiente executável antes da demonstração.

## Contribuição e versionamento

O projeto utiliza Git e GitHub para organizar o desenvolvimento e registrar a contribuição dos integrantes.

As alterações devem ser pequenas, objetivas e acompanhadas de mensagens de commit descritivas.

Exemplos:

\`\`\`text
feat: adiciona endpoint para perguntas frequentes
fix: corrige carregamento dos dados da API
docs: atualiza instruções de execução
refactor: organiza consultas ao banco de dados
\`\`\`

Cada integrante deve utilizar sua própria identidade Git, manter o histórico de contribuições e registrar as alterações realizadas durante o desenvolvimento.

## Equipe

Projeto desenvolvido por estudantes do Instituto Federal de Santa Catarina — Câmpus Chapecó.

- Bruno J. Hohenberger
- Juan A. Lopes
- Lorenzo P. Reginato
- Mateus Pizzi
- Otavio A. M. da Silva
- Rafael P. Costa
- Vicenzo Scalvi

## Licença

A licença de distribuição do projeto ainda não foi definida.

---

**IFSC.AI — Informação acessível, orientação inteligente.**