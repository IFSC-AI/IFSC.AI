-- IFSC.AI — esquema do banco (SQLite)
-- A base de conhecimento (tabela 'conhecimento') é carregada de base_conhecimento.md por importar_base.py.

CREATE TABLE IF NOT EXISTS setores (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  nome           TEXT NOT NULL,
  bloco          TEXT,
  descricao      TEXT,
  horario        TEXT,
  contato        TEXT,
  palavras_chave TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS faq (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  pergunta  TEXT NOT NULL,
  resposta  TEXT NOT NULL,
  ordem     INTEGER DEFAULT 0,
  ativo     INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS feedback (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  nota       INTEGER CHECK (nota BETWEEN 1 AND 5),
  comentario TEXT,
  criado_em  TEXT DEFAULT (datetime('now','localtime'))
);

-- Log de perguntas feitas ao agente (pelo site ou enviadas pelo n8n)
CREATE TABLE IF NOT EXISTS conversas (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  origem    TEXT DEFAULT 'site',        -- 'site' ou 'whatsapp'
  pergunta  TEXT NOT NULL,
  resposta  TEXT,
  encontrou INTEGER DEFAULT 1,          -- 0 = agente não soube responder
  criado_em TEXT DEFAULT (datetime('now','localtime'))
);

-- Base de conhecimento: uma linha por pergunta/resposta (ou bloco de contexto) do .md
CREATE TABLE IF NOT EXISTS conhecimento (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  ordem    INTEGER,
  numero   TEXT,        -- ex.: '6.2' ou '6.ctx1' (contexto)
  secao    TEXT,        -- ex.: '6. Biblioteca'
  pergunta TEXT,
  resposta TEXT,
  status   TEXT,        -- Base | Relato | Pendente | PPC | Contexto
  setor    TEXT         -- setor responsável (pode ser NULL)
);

-- Índice de busca por texto (FTS5), ignora acentos: "emprestimo" acha "empréstimo"
CREATE VIRTUAL TABLE IF NOT EXISTS conhecimento_fts USING fts5(
  pergunta, resposta, secao, tokenize = "unicode61 remove_diacritics 2"
);

-- Configurações em chave/valor (guarda as regras de comportamento do agente)
CREATE TABLE IF NOT EXISTS config (chave TEXT PRIMARY KEY, valor TEXT);

-- ---------- Dados iniciais ----------
-- Setores reais citados na base (seção 12.1). Horários/contatos: preencher quando forem confirmados.
INSERT INTO setores (nome, bloco, descricao, horario, contato, palavras_chave) VALUES
 ('DAE — Departamento de Assuntos Estudantis','Bloco A','Atendimento geral aos estudantes, horários de aula, alimentação escolar, orientação sobre acessibilidade e visitantes perdidos.',NULL,NULL,'dae atendimento estudante horario aula alimentacao lanche'),
 ('Registro Acadêmico (RA)','Bloco A','Matrícula, registros acadêmicos, faltas e frequência, aproveitamento de estudos, trancamento e cancelamento.',NULL,NULL,'ra matricula faltas frequencia trancamento cancelamento transferencia documentos'),
 ('Biblioteca','Bloco A','Acervo, empréstimos, Minha Biblioteca e doações de livros.',NULL,NULL,'livros emprestimo acervo estudo leitura doacao'),
 ('Núcleo de Acessibilidade Educacional (NAE)',NULL,'Atendimento e orientação sobre acessibilidade.',NULL,NULL,'nae acessibilidade apoio inclusao'),
 ('Coordenadoria de Relações Externas',NULL,'Visitas de escolas e turmas; sugestões sobre divulgação de eventos.',NULL,NULL,'visita escola turma eventos divulgacao'),
 ('Guarita','Entrada principal (Rua Canários da Terra)','Entrada e orientação a visitantes.',NULL,NULL,'entrada visitante portaria');

INSERT INTO faq (pergunta, resposta, ordem) VALUES
 ('O que é o IFSC AI?','Um projeto que facilita o acesso a informações do IFSC Câmpus Chapecó para estudantes, servidores e visitantes, por meio de um agente de IA no WhatsApp.',1),
 ('Que tipo de pergunta posso fazer?','Perguntas sobre setores, blocos, horários, serviços e procedimentos do câmpus.',2),
 ('E se o agente não souber responder?','Ele não inventa informações. Quando não tiver dados suficientes, vai orientar você a procurar o setor responsável.',3),
 ('As informações são confiáveis?','As respostas se baseiam em uma base de conhecimento organizada e validada previamente. Em caso de dúvida, confirme diretamente com o setor responsável.',4);
