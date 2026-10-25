# IFSC.AI

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)
![Frontend](https://img.shields.io/badge/frontend-HTML%20%7C%20CSS%20%7C%20JavaScript-blue)
![Backend](https://img.shields.io/badge/backend-Python%20%7C%20FastAPI-3776AB)
![Database](https://img.shields.io/badge/database-Supabase-3ECF8E)
![IA](https://img.shields.io/badge/IA-n8n-EA4B71)

**Agente de Inteligência Artificial integrado ao WhatsApp para facilitar o acesso a informações sobre o IFSC Câmpus Chapecó.**

Projeto acadêmico desenvolvido no Instituto Federal de Santa Catarina (IFSC), Câmpus Chapecó, com o objetivo de tornar mais simples e acessível a orientação de estudantes, servidores, visitantes e comunidade externa.

## Sobre o projeto

Encontrar informações sobre setores, serviços, espaços e procedimentos institucionais pode ser difícil quando os dados estão distribuídos entre diferentes canais.

O IFSC.AI busca facilitar esse acesso por meio de um agente de Inteligência Artificial integrado ao WhatsApp, que utiliza uma base de conhecimento com informações institucionais. O projeto também conta com uma central de ajuda na web, que apresenta a solução, explica como utilizar o agente e disponibiliza informações sobre seu funcionamento.

**Objetivo:** facilitar o acesso a informações institucionais do IFSC Câmpus Chapecó por meio de uma solução acessível, integrada e baseada em Inteligência Artificial.

## Estado atual do projeto

- **Frontend:** site desenvolvido com HTML, CSS e JavaScript e hospedado no Vercel.
- **Backend:** API própria desenvolvida em Python com FastAPI e publicada no Vercel.
- **Banco de dados:** Supabase/PostgreSQL conectado à API.
- **Conteúdo dinâmico:** o frontend consome a API do backend e recebe os conteúdos cadastrados no banco, sem depender exclusivamente de textos fixos no HTML.
- **Agente no WhatsApp:** a arquitetura prevê integração com a WhatsApp Business Platform e automações no n8n. A implementação e a validação desse fluxo fazem parte do desenvolvimento do projeto.

### Aplicação publicada

- **Site:** [https://ifscai-frontend.vercel.app/](https://ifscai-frontend.vercel.app/)
- **API — status:** [https://ifscai-api.vercel.app/](https://ifscai-api.vercel.app/)
- **API — conteúdos:** [https://ifscai-api.vercel.app/api/conteudos](https://ifscai-api.vercel.app/api/conteudos)

A rota de conteúdos consulta o Supabase e, no estado atual, retorna os 31 registros cadastrados na tabela `conteudos`.

## Funcionalidades

- **Central de ajuda:** apresenta o IFSC.AI e orienta o usuário sobre como utilizar o serviço.
- **Consumo de conteúdo via API:** o JavaScript busca os dados publicados pelo backend e atualiza os elementos correspondentes da página.
- **Gerenciamento de conteúdo:** títulos, descrições e links do site são armazenados no Supabase e consultados pela API.
- **API própria:** fornece os conteúdos do site em formato JSON.
- **Agente de IA no WhatsApp:** previsto para receber perguntas em linguagem natural e orientar os usuários com base na base de conhecimento institucional.
- **Respostas fundamentadas:** o comportamento planejado do agente prioriza informações verificáveis e deve direcionar o usuário ao setor responsável quando não houver dados suficientes.

## Arquitetura

O IFSC.AI possui dois fluxos principais: o site informacional e o agente de IA integrado ao WhatsApp.

### 1. Site informacional

O site consulta os conteúdos armazenados no Supabase por meio de uma API própria.

```text
Usuário
   |
   v
Frontend (HTML, CSS e JavaScript)
   |
   | Requisição HTTP / fetch()
   v
API própria (Python + FastAPI)
   |
   | Consulta ao banco de dados
   v
Supabase (PostgreSQL)
   |
   | Resposta em JSON
   v
Frontend atualizado
```

O frontend e a API estão hospedados no Vercel. O Supabase é responsável pelo armazenamento e gerenciamento dos conteúdos.

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
Base de conhecimento institucional
   |
   v
Resposta ao usuário pelo WhatsApp
```

O n8n coordena o fluxo de automação do agente. A base de conhecimento é utilizada para fundamentar as respostas. O site informacional tem a função de apresentar o projeto e orientar os usuários; ele não funciona como uma segunda interface de conversa com o agente.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
| --- | --- |
| HTML5 | Estrutura das páginas web |
| CSS3 | Estilização e identidade visual |
| JavaScript | Interatividade e consumo da API |
| Python | Desenvolvimento do backend |
| FastAPI | Criação da API própria |
| PostgreSQL | Armazenamento dos dados |
| Supabase | Hospedagem e gerenciamento do banco PostgreSQL |
| Vercel | Hospedagem do frontend e da API |
| n8n | Automação do fluxo do agente de IA |
| WhatsApp Business Platform | Integração do agente com o WhatsApp |
| Git e GitHub | Versionamento e colaboração |

## Estrutura do projeto

Estrutura resumida dos principais arquivos utilizados no site e na API:

```text
IFSC.AI/
├── frontend/
│   ├── index.html
│   ├── quem-nos-somos.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── main.py
│   ├── app.py
│   ├── importar_base.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Base de conhecimento IFSC AI — IFSC Câmpus Chapecó Markdown.md
│
├── .gitignore
└── README.md
└── ifscai.json
└── Wireframe_IFSC.AI.pdf
```

A API de conteúdos do site utiliza `backend/main.py` como ponto de entrada do FastAPI, configurado em `backend/pyproject.toml`. O arquivo `backend/app.py` pertence a outro componente do backend; não é o ponto de entrada da API de conteúdos publicada no Vercel.

## Site informacional

O site funciona como uma central de ajuda para apresentar o projeto e facilitar o acesso ao agente no WhatsApp.

Suas principais seções são:

- **Início:** apresentação do IFSC.AI e acesso ao agente.
- **Como usar:** instruções para iniciar uma conversa pelo WhatsApp.
- **Quem nós somos:** apresentação do projeto e da equipe.
- **Perguntas frequentes:** respostas às dúvidas sobre o funcionamento da solução.
- **Contato:** direcionamento ao agente e aos canais de atendimento pertinentes.

A identidade visual utiliza um tema escuro, com destaque em verde e a fonte EB Garamond.

Os conteúdos da página são consultados pela API. Para atualizar um texto cadastrado, é possível editar o registro correspondente no Supabase sem precisar alterar manualmente aquele texto no HTML.

## API e banco de dados

A API foi desenvolvida em Python com FastAPI. Ela consulta a tabela `conteudos` no Supabase e retorna os resultados em JSON.

### Endpoints disponíveis

| Método | Endpoint | Finalidade |
| --- | --- | --- |
| `GET` | `/` | Verificar o estado da API |
| `GET` | `/api/conteudos` | Consultar todos os conteúdos cadastrados |
| `GET` | `/api/conteudos/{chave}` | Consultar um conteúdo específico pela sua chave |

Exemplo de chave: `hero_titulo`.

A rota `/api/conteudos` retorna registros com os campos `id`, `created_at`, `chave`, `titulo`, `descricao` e `url`. No estado atual, os 31 conteúdos do site estão cadastrados na tabela `conteudos`.

### Banco de dados

O banco utiliza PostgreSQL, gerenciado pelo Supabase. A tabela `conteudos` contém os dados necessários para montar as seções informacionais do site, incluindo:

- **Chave:** identificador utilizado pelo frontend para localizar o conteúdo.
- **Título:** texto principal do item, quando aplicável.
- **Descrição:** texto complementar, quando aplicável.
- **URL:** endereço de destino de links, quando aplicável.

O JavaScript solicita os dados à API e associa cada registro à sua chave para atualizar a interface. O backend é responsável por consultar o banco e disponibilizar os dados ao frontend.

## Hospedagem

| Serviço | Responsabilidade |
| --- | --- |
| [Vercel](https://vercel.com/) | Hospedar o frontend e a API FastAPI |
| [Supabase](https://supabase.com/) | Hospedar e gerenciar o banco PostgreSQL |
| [n8n](https://n8n.io/) | Coordenar o fluxo de automação do agente de IA |

Os serviços utilizados podem estar sujeitos a limites, condições de uso e configurações específicas dos respectivos planos. O funcionamento completo do agente também depende da configuração do n8n, da integração com o WhatsApp e dos serviços externos utilizados.

## Execução local

### Visualizar o frontend

1. Clone o repositório e abra a pasta do projeto no Visual Studio Code.
2. Abra a pasta `frontend`.
3. Execute `index.html` utilizando uma extensão como Live Server ou Live Preview.
4. Acesse o endereço local exibido no navegador.

O `script.js` está configurado para consultar a API publicada. Para testar a API localmente, altere temporariamente `CONFIG.API_BASE` em `frontend/script.js` para `http://127.0.0.1:8000/api`.

### Executar a API localmente

É necessário ter Python instalado e configurar as variáveis de ambiente para a conexão com o Supabase.

1. Na raiz do repositório, crie um arquivo `.env` com as variáveis necessárias:

   ```env
   SUPABASE_URL=https://SEU-PROJETO.supabase.co
   SUPABASE_KEY=SUA_CHAVE_DO_SUPABASE
   FRONTEND_URL=http://127.0.0.1:5500
   ```

   Substitua os valores de exemplo pelos valores da sua configuração. O arquivo `.env` é lido a partir da raiz do repositório.

2. No terminal, entre na pasta `backend`:

   ```powershell
   cd backend
   ```

3. Crie e ative um ambiente virtual no Windows:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   No Linux ou macOS, a ativação pode ser feita com `source .venv/bin/activate` após criar o ambiente virtual com `python3 -m venv .venv`.

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Inicie a API:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. Teste os endpoints no navegador:

   - `http://127.0.0.1:8000/`
   - `http://127.0.0.1:8000/api/conteudos`
   - `http://127.0.0.1:8000/api/conteudos/hero_titulo`

A execução local depende de variáveis válidas e de conectividade com o Supabase.

## Configuração e segurança

Configure as variáveis de ambiente exigidas pela aplicação no ambiente local e no painel do Vercel. O frontend publicado utiliza a URL da API de produção; o backend utiliza as variáveis `SUPABASE_URL`, `SUPABASE_KEY` e, quando definida, `FRONTEND_URL` para configurar o CORS.

Não coloque credenciais administrativas, chaves secretas ou valores sensíveis no README. Não utilize uma chave `service_role` ou outra chave privilegiada no frontend. Em produção, utilize somente as credenciais necessárias ao backend e configure adequadamente as permissões do banco.

## Boas práticas e limitações

- As informações institucionais devem ter origem verificável e ser mantidas atualizadas.
- O agente deve evitar inventar informações ou fornecer orientações sem dados suficientes.
- Quando não puder responder com segurança, deverá orientar o usuário a procurar o setor responsável.
- O agente não substitui os canais oficiais nem o atendimento humano.
- O funcionamento do fluxo de WhatsApp deve ser validado com a integração e os serviços externos configurados.

## Versionamento e contribuição

O projeto utiliza Git e GitHub para organizar o desenvolvimento e registrar as contribuições dos integrantes. As alterações devem ser pequenas, objetivas e acompanhadas de mensagens de commit descritivas.

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

**IFSC.AI — Informação acessível, orientação inteligente.**