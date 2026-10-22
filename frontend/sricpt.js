// Sc4lv1
//script.js — ponte entre o front-end (este site) e para o backend do IFSC.AI
//
// Como linkar o backend após o termino de configuração do backend:
//   1. Preencher CONFIG.API_BASE com a URL do backend (em produção, HTTPS).
//   2. Liberar CORS no backend para o domínio do site.
//   3. Garantir que as rotas abaixo respondam no formato combinado.
//
// Enquanto CONFIG.API_BASE estiver vazio, a ponte fica DESLIGADA: nenhuma requisição
// é feita, não aparece erro no console e o site funciona só com o HTML estático.
//
// ATENÇÃO: tudo que está neste arquivo é público. Não coloque chaves, tokens ou senhas aqui.
//
// CONTRATO COMBINADO COM O BACKEND:
//   GET /faq  ->  200  [ { "pergunta": "texto", "resposta": "texto" }, ... ]
//
// Quando foi  criar uma nova integração: adicione a rota em ROTAS e chame api(ROTAS.suaRota).
 
const CONFIG = {
  // Ex.: 'http://localhost:3000/api' (teste local) ou 'https://api.seudominio.com/api' (produção)
  API_BASE: '',
  TIMEOUT_MS: 8000,
};
 
const ROTAS = {
  faq: '/faq',
};
 
const ponteAtiva = () => Boolean(CONFIG.API_BASE);
 
/**
 * Chamada genérica ao backend: com timeout, checagem de status e retorno em JSON.
 * GET:  await api(ROTAS.faq)
 * POST: await api('/rota', { method: 'POST', body: JSON.stringify({ campo: 'valor' }) })
 */
async function api(caminho, opcoes = {}) {
  if (!ponteAtiva()) throw new Error('Backend não configurado (CONFIG.API_BASE vazio).');
 
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), CONFIG.TIMEOUT_MS);
 
  // Content-Type só quando há corpo; em GET evita uma requisição "preflight" desnecessária.
  const headers = { Accept: 'application/json' };
  if (opcoes.body) headers['Content-Type'] = 'application/json';
 
  try {
    const resposta = await fetch(`${CONFIG.API_BASE}${caminho}`, {
      ...opcoes,
      headers: { ...headers, ...opcoes.headers },
      signal: controller.signal,
    });
    if (!resposta.ok) throw new Error(`Erro HTTP ${resposta.status}`);
    return await resposta.json();
  } finally {
    clearTimeout(timer);
  }
}
 