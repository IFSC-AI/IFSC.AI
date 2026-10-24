# IFSC.AI



![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![Frontend](https://img.shields.io/badge/frontend-HTML%20%7C%20CSS%20%7C%20JavaScript-blue)
![Backend](https://img.shields.io/badge/backend-Python%20%7C%20Flask-3776AB)
![Database](https://img.shields.io/badge/database-Supabase-3ECF8E)
![IA](https://img.shields.io/badge/IA-n8n-EA4B71)

**Agente de Inteligência Artificial integrado ao WhatsApp para facilitar o acesso a informações sobre o IFSC Câmpus Chapecó.**

Projeto acadêmico desenvolvido no Instituto Federal de Santa Catarina (IFSC), Câmpus Chapecó, com o objetivo de tornar mais simples e acessível a orientação de estudantes, servidores, visitantes e comunidade externa.

---

## Sobre o projeto

Encontrar informações sobre setores, serviços, espaços e procedimentos institucionais pode ser difícil quando os dados estão distribuídos entre diferentes canais.

O IFSC.AI busca solucionar esse problema por meio de um agente de Inteligência Artificial integrado ao WhatsApp, capaz de responder a perguntas utilizando uma base de conhecimento com informações institucionais.

O projeto também possui uma central de ajuda na web, que apresenta a solução, explica como utilizar o agente e disponibiliza informações sobre seu funcionamento.

**Objetivo:** facilitar o acesso a informações institucionais do IFSC Câmpus Chapecó por meio de uma solução acessível, integrada e baseada em Inteligência Artificial.

## Funcionalidades

- **Agente de IA no WhatsApp:** permite que os usuários enviem perguntas em linguagem natural.
- **Orientação institucional:** fornece informações sobre setores, blocos, cursos, serviços e procedimentos do câmpus, conforme os dados disponíveis.
- **Base de conhecimento:** organiza informações institucionais para fundamentar as respostas do agente.
- **Central de ajuda:** apresenta instruções de utilização, perguntas frequentes e informações sobre o projeto.
- **API própria:** disponibiliza os conteúdos do site por meio de endpoints desenvolvidos pela equipe.
- **Conteúdo dinâmico:** permite que o frontend consulte os dados armazenados no banco de dados, sem depender exclusivamente de textos fixos no HTML.

> O frontend está em desenvolvimento. A API, a integração com o banco de dados e o carregamento dinâmico dos conteúdos serão implementados e testados durante o desenvolvimento do projeto.

## Arquitetura

O IFSC.AI possui dois fluxos principais: o site informacional e o agente de IA integrado ao WhatsApp.

### 1. Site informacional

O site utiliza uma API própria para consultar os conteúdos armazenados no banco de dados.

```text
Usuário
   |
   v
Frontend (HTML, CSS e JavaScript)
   |
   | Requisições HTTP / fetch()
   v
API própria (Python + Flask)
   |
   | Consultas ao banco
   v
Supabase (PostgreSQL)
   |
   | Dados em JSON
   v
Frontend atualizado
```

O frontend será hospedado no Vercel, assim como a API Flask. O Supabase será responsável pelo armazenamento dos dados.

### 2. Agente de IA no WhatsApp

```text
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
Agente de Inteligência Artificial
   |
   v
Base de conhecimento
   |
   v
Resposta ao usuário pelo WhatsApp
```

O n8n é responsável por coordenar o fluxo de automação e executar a lógica do agente de IA. A aplicação web possui uma finalidade informacional e não funciona como uma segunda interface de conversação com o agente.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
| --- | --- |
| HTML5 | Estrutura das páginas web |
| CSS3 | Estilização e identidade visual |
| JavaScript | Interatividade e consumo da API |
| Python | Desenvolvimento do backend |
| Flask | Criação da API própria |
| PostgreSQL | Armazenamento dos dados |
| Supabase | Hospedagem e gerenciamento do banco PostgreSQL |
| Vercel | Hospedagem do frontend e da API |
| n8n | Automação dos fluxos e execução do agente de IA |
| WhatsApp Business Platform | Integração com o WhatsApp |
| Git e GitHub | Versionamento e colaboração |

## Estrutura do projeto

A organização lógica prevista para o repositório é:

```text
IFSC.AI/
├── frontend/
│   ├── index.html
│   ├── quem-nos-somos.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

A configuração de implantação no Vercel poderá exigir ajustes na localização dos arquivos, no ponto de entrada do Flask e no direcionamento das rotas da API.

As credenciais e demais configurações sensíveis serão mantidas em variáveis de ambiente, e não diretamente no código-fonte.

## Site informacional

O site funciona como uma central de ajuda para orientar os usuários sobre o projeto e facilitar o acesso ao agente no WhatsApp.

Suas principais seções são:

- **Início:** apresentação do IFSC.AI e acesso ao agente.
- **Como usar:** instruções para iniciar uma conversa pelo WhatsApp.
- **Quem nós somos:** apresentação do projeto e da equipe.
- **Perguntas frequentes:** respostas às dúvidas sobre o funcionamento da solução.
- **Contato:** direcionamento ao agente e aos canais de atendimento pertinentes.

A identidade visual utiliza um tema escuro, com destaque em verde e a fonte EB Garamond.

## API e banco de dados

A API própria será desenvolvida em Python com Flask e disponibilizará os dados do site em formato JSON.

O JavaScript realizará requisições assíncronas para consultar esses dados e atualizar os elementos correspondentes da interface.

### Endpoints previstos

| Método | Endpoint | Finalidade |
| --- | --- | --- |
| GET | `/api/conteudo` | Consultar os textos das seções do site |
| GET | `/api/faq` | Consultar as perguntas frequentes |

Os endpoints acima representam a estrutura planejada e deverão ser implementados no backend.

### Banco de dados

O banco PostgreSQL será hospedado no Supabase.

Os dados previstos incluem:

- **Conteúdos:** títulos, descrições e textos informativos das seções.
- **Perguntas frequentes:** perguntas e respectivas respostas.

A API será responsável por consultar o banco e retornar os dados necessários ao frontend.

Essa estrutura permitirá atualizar os conteúdos armazenados sem precisar alterar manualmente cada texto diretamente no HTML.

## Hospedagem

A hospedagem foi planejada para uma demonstração acadêmica, utilizando os serviços abaixo.

| Serviço | Responsabilidade |
| --- | --- |
| [Vercel](https://vercel.com/) | Hospedar o frontend e a API Flask. |
| [Supabase](https://supabase.com/) | Hospedar e gerenciar o banco PostgreSQL. |
| [n8n](https://n8n.io/) | Executar o fluxo do agente de IA integrado ao WhatsApp. |

O Vercel e o Supabase oferecem planos gratuitos sujeitos a limites e condições de uso. A disponibilidade do agente também depende da configuração do n8n, do WhatsApp e dos serviços externos utilizados.

### Publicação prevista

1. Enviar o código do projeto para o repositório GitHub.
2. Criar um projeto no Supabase e configurar as tabelas necessárias.
3. Importar o repositório no Vercel e configurar a implantação do frontend e da API.
4. Configurar as variáveis de ambiente necessárias para a conexão com o banco.
5. Publicar e testar a aplicação, verificando o carregamento das páginas e as respostas dos endpoints.

## Execução local

### Visualizar o frontend

1. Clone o repositório.
2. Abra a pasta do projeto no Visual Studio Code.
3. Abra a pasta `frontend`.
4. Execute o arquivo `index.html` utilizando a extensão Live Server ou Live Preview.
5. Acesse o endereço local exibido no navegador.

Essa sequência permite visualizar a versão estática do site. O funcionamento integrado dependerá da implementação e da configuração da API e do banco de dados.

### Executar o backend

A execução local da API será documentada após a implementação do Flask, incluindo as dependências, as variáveis de ambiente e as instruções necessárias para conectar ao Supabase.

## Boas práticas e limitações

- As informações institucionais devem ter origem verificável e ser mantidas atualizadas.
- O agente deve evitar inventar informações ou fornecer orientações sem dados suficientes.
- Quando não puder responder com segurança, deverá orientar o usuário a procurar o setor responsável.
- O agente não substitui os canais oficiais nem o atendimento humano.
- As credenciais utilizadas na API e nas integrações não devem ser publicadas no GitHub.
- O funcionamento completo deverá ser validado em uma demonstração real, sem depender de respostas simuladas ou dados fictícios.

## Versionamento e contribuição

O projeto utiliza Git e GitHub para organizar o desenvolvimento e registrar as contribuições dos integrantes.

As alterações devem ser pequenas, objetivas e acompanhadas de mensagens de commit descritivas.

Exemplos:

```text
feat: adiciona endpoint de perguntas frequentes
fix: corrige carregamento dos dados da API
docs: atualiza instruções de execução
refactor: organiza consultas ao banco de dados
```

Cada integrante deve utilizar sua própria identidade Git e registrar suas contribuições ao longo do desenvolvimento.

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
ifsc.AI-DataBase
**IFSC.AI — Informação acessível, orientação inteligente.**