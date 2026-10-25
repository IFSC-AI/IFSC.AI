// Sc4lv1
// script.js — integração entre o frontend e a API do IFSC.AI

const CONFIG = {
  // URL local da API FastAPI.
  // Em produção, substituir pela URL publicada da API.
  API_BASE: 'http://127.0.0.1:8000/api',
  TIMEOUT_MS: 8000,
};

const ROTAS = {
  conteudos: '/conteudos',
};

const ponteAtiva = () => Boolean(CONFIG.API_BASE);


/**
 * Consulta a API e retorna os dados em JSON.
 */
async function api(caminho) {
  if (!ponteAtiva()) {
    throw new Error('Backend não configurado.');
  }

  const controller = new AbortController();

  const timer = setTimeout(() => {
    controller.abort();
  }, CONFIG.TIMEOUT_MS);

  try {
    const resposta = await fetch(`${CONFIG.API_BASE}${caminho}`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
      signal: controller.signal,
    });

    if (!resposta.ok) {
      throw new Error(`Erro HTTP ${resposta.status}`);
    }

    return await resposta.json();
  } finally {
    clearTimeout(timer);
  }
}


/**
 * Obtém os dados de um conteúdo pela chave.
 */
function obterConteudo(conteudos, chave) {
  return conteudos.get(chave);
}


/**
 * Atualiza o texto de um elemento HTML.
 * Usa textContent para evitar a interpretação de HTML vindo da API.
 */
function atualizarTexto(conteudos, chave, seletor, campo = 'titulo') {
  const conteudo = obterConteudo(conteudos, chave);
  const elemento = document.querySelector(seletor);

  if (!conteudo || !elemento) return;

  const valor = conteudo[campo];

  if (typeof valor === 'string') {
    elemento.textContent = valor;
  }
}


/**
 * Atualiza o texto e o endereço de um link.
 */
function atualizarLink(conteudos, chave, seletor) {
  const conteudo = obterConteudo(conteudos, chave);
  const elemento = document.querySelector(seletor);

  if (!conteudo || !elemento) return;

  if (typeof conteudo.titulo === 'string') {
    elemento.textContent = conteudo.titulo;
  }

  if (typeof conteudo.url === 'string' && conteudo.url.trim() !== '') {
    elemento.href = conteudo.url;
  }
}


/**
 * Atualiza a marca do cabeçalho preservando o destaque visual.
 */
function atualizarMarcaCabecalho(conteudos) {
  const conteudo = obterConteudo(conteudos, 'marca');
  const marca = document.querySelector('.nav .brand');

  if (!conteudo || !marca || typeof conteudo.titulo !== 'string') {
    return;
  }

  const titulo = conteudo.titulo;
  const separador = titulo.indexOf('.');

  if (separador === -1) {
    marca.textContent = titulo;
  } else {
    const texto = document.createTextNode(titulo.slice(0, separador));
    const destaque = document.createElement('span');

    destaque.textContent = titulo.slice(separador);

    marca.replaceChildren(texto, destaque);
  }

  if (typeof conteudo.url === 'string' && conteudo.url.trim() !== '') {
    marca.href = conteudo.url;
  }
}


/**
 * Atualiza a marca do rodapé preservando o destaque visual.
 */
function atualizarMarcaRodape(conteudos) {
  const conteudo = obterConteudo(conteudos, 'footer_marca');
  const marca = document.querySelector('.brand-footer');

  if (!conteudo || !marca || typeof conteudo.titulo !== 'string') {
    return;
  }

  const titulo = conteudo.titulo;
  const separador = titulo.indexOf(' ');

  if (separador === -1) {
    marca.textContent = titulo;
  } else {
    const texto = document.createTextNode(titulo.slice(0, separador + 1));
    const destaque = document.createElement('span');

    destaque.textContent = titulo.slice(separador + 1);

    marca.replaceChildren(texto, destaque);
  }

  if (typeof conteudo.url === 'string' && conteudo.url.trim() !== '') {
    marca.classList.add('brand-footer');
  }
}


/**
 * Atualiza o título principal mantendo a linha e o destaque em itálico.
 */
function atualizarTituloPrincipal(conteudos) {
  const conteudo = obterConteudo(conteudos, 'hero_titulo');
  const titulo = document.querySelector('.hero h1');

  if (!conteudo || !titulo || typeof conteudo.titulo !== 'string') {
    return;
  }

  const texto = conteudo.titulo;
  const separador = ' Pergunte ao ';
  const indice = texto.indexOf(separador);

  if (indice === -1) {
    titulo.textContent = texto;
    return;
  }

  const primeiraParte = texto.slice(0, indice);
  const segundaParte = texto.slice(indice + 1);

  const quebra = document.createElement('br');
  const destaque = document.createElement('em');

  destaque.textContent = segundaParte;

  titulo.replaceChildren(
    document.createTextNode(primeiraParte),
    quebra,
    destaque
  );
}


/**
 * Atualiza os três passos de utilização.
 */
function carregarPassos(conteudos) {
  const chaves = [
    'passo_1',
    'passo_2',
    'passo_3',
  ];

  const cards = document.querySelectorAll('#como-usar .steps .card');

  cards.forEach((card, indice) => {
    const conteudo = obterConteudo(conteudos, chaves[indice]);

    if (!conteudo) return;

    const titulo = card.querySelector('h3');
    const descricao = card.querySelector('p');

    if (titulo && typeof conteudo.titulo === 'string') {
      titulo.textContent = conteudo.titulo;
    }

    if (descricao && typeof conteudo.descricao === 'string') {
      descricao.textContent = conteudo.descricao;
    }
  });
}


/**
 * Atualiza as perguntas frequentes.
 * Se os dados estiverem incompletos, mantém o FAQ original do HTML.
 */
function carregarFaq(conteudos) {
  const lista = document.querySelector('#perguntas .faq');

  if (!lista) return;

  const chaves = [
    'faq_o_que_e',
    'faq_tipos_perguntas',
    'faq_agente_nao_sabe',
    'faq_confiabilidade',
  ];

  const itens = chaves.map((chave) => obterConteudo(conteudos, chave));

  if (itens.some((item) => !item ||
      typeof item.titulo !== 'string' ||
      typeof item.descricao !== 'string')) {
    return;
  }

  const elementos = itens.map((item) => {
    const detalhes = document.createElement('details');
    const pergunta = document.createElement('summary');
    const resposta = document.createElement('p');

    pergunta.textContent = item.titulo;
    resposta.textContent = item.descricao;

    detalhes.append(pergunta, resposta);

    return detalhes;
  });

  lista.replaceChildren(...elementos);
}


/**
 * Atualiza os conteúdos gerais da página.
 */
function atualizarPagina(conteudos) {
  // Marca e navegação principal
  atualizarMarcaCabecalho(conteudos);

  atualizarLink(conteudos, 'nav_como_usar',
    '.nav-links a[href="#como-usar"]');

  atualizarLink(conteudos, 'nav_quem_nos_somos',
    '.nav-links a[href="quem-nos-somos.html"]');

  atualizarLink(conteudos, 'nav_perguntas',
    '.nav-links a[href="#perguntas"]');

  atualizarLink(conteudos, 'nav_contato',
    '.nav-links a[href="#contato"]');

  atualizarLink(conteudos, 'btn_abrir_whatsapp',
    '.nav > a.btn.btn-small');


  // Seção principal
  atualizarTexto(conteudos, 'hero_eyebrow',
    '.hero .eyebrow');

  atualizarTituloPrincipal(conteudos);

  atualizarTexto(conteudos, 'hero_descricao',
    '.hero .lead', 'descricao');

  atualizarLink(conteudos, 'hero_btn_whatsapp',
    '.hero .hero-actions a');


  // Seção Como usar
  atualizarTexto(conteudos, 'como_usar_eyebrow',
    '#como-usar .eyebrow');

  atualizarTexto(conteudos, 'como_usar_titulo',
    '#como-usar h2');

  carregarPassos(conteudos);


  // Perguntas frequentes
  atualizarTexto(conteudos, 'faq_eyebrow',
    '#perguntas .eyebrow');

  atualizarTexto(conteudos, 'faq_titulo',
    '#perguntas h2');

  carregarFaq(conteudos);


  // Contato
  atualizarTexto(conteudos, 'contato_titulo',
    '#contato .cta h2');

  atualizarTexto(conteudos, 'contato_descricao',
    '#contato .cta p', 'descricao');

  atualizarLink(conteudos, 'contato_btn_whatsapp',
    '#contato .cta a.btn');


  // Rodapé
  atualizarMarcaRodape(conteudos);

  atualizarTexto(conteudos, 'footer_descricao',
    '.footer-text', 'descricao');

  atualizarLink(conteudos, 'footer_nav_como_usar',
    '.footer-links a[href="#como-usar"]');

  atualizarLink(conteudos, 'footer_nav_quem_nos_somos',
    '.footer-links a[href="quem-nos-somos.html"]');

  atualizarLink(conteudos, 'footer_nav_perguntas',
    '.footer-links a[href="#perguntas"]');

  atualizarLink(conteudos, 'footer_nav_contato',
    '.footer-links a[href="#contato"]');

  atualizarTexto(conteudos, 'footer_copyright',
    '.footer-bottom p', 'descricao');
}


/**
 * Consulta os conteúdos do Supabase por meio da API própria.
 * Em caso de falha, mantém o HTML original.
 */
async function carregarConteudos() {
  if (!ponteAtiva()) return;

  try {
    const itens = await api(ROTAS.conteudos);

    if (!Array.isArray(itens) || itens.length === 0) {
      console.warn('A API não retornou conteúdos. Mantendo o HTML original.');
      return;
    }

    const conteudos = new Map(
      itens.map((item) => [item.chave, item])
    );

    atualizarPagina(conteudos);

    console.log('Conteúdos carregados da API:', itens.length);

  } catch (erro) {
    console.warn(
      'Não foi possível carregar os conteúdos da API. Mantendo o HTML original.',
      erro
    );
  }
}


document.addEventListener('DOMContentLoaded', carregarConteudos);