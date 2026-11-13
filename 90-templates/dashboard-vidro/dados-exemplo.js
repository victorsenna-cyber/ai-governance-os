// Dados de EXEMPLO do modelo "dashboard-vidro" (empresa fictícia).
// Para instanciar: copie este arquivo como dados.js na pasta da conta e troque os valores.
// Cada seção em `secoes` só aparece se o bloco de dados dela existir.
// Os KPIs de Funil, Clientes e Produtos são CALCULADOS dos itens; não se digitam.
window.DADOS = {
  marca: {
    nome: "Empresa Exemplo",
    acento: "#3B82F6",          // cor de destaque (anel, barra em foco, chave ligada)
    fundo: ""                   // url de foto de ambiente; vazio = fundo gerado
  },
  usuario: { nome: "Ana Souza" },
  notificacoes: 3,
  atualizado_em: "2026-11-10 15:45",
  // de onde vem o número de cada tela (marcação de fonte da casa)
  fontes: { visao: "exemplo, digitado", relatorios: "calculado das telas", funil: "exemplo, cartões do funil", clientes: "exemplo, lista de clientes", produtos: "exemplo, catálogo" },

  secoes: [
    { id: "visao",      rotulo: "Visão geral", icone: "home" },
    { id: "relatorios", rotulo: "Relatórios",  icone: "chart",  titulo: "Relatórios", subtitulo: "O que os números dizem, lidos do próprio painel" },
    { id: "funil",      rotulo: "Funil",       icone: "kanban", titulo: "Funil de negócios", subtitulo: "Arraste um negócio entre as etapas para atualizar o funil" },
    { id: "clientes",   rotulo: "Clientes",    icone: "users",  titulo: "Clientes", subtitulo: "Cada cliente, quem cuida e quanto já rendeu" },
    { id: "produtos",   rotulo: "Produtos",    icone: "box",    titulo: "Produtos", subtitulo: "Catálogo, preço e o que está à venda agora" }
  ],

  visao_geral: {
    abas: ["Visão geral", "Vendas", "Marketing", "Atendimento"],
    equipe: { titulo: "Equipe", legenda: "4 pessoas ativas", membros: ["Ana Souza", "Bruno Lima", "Carla Dias", "Diego Rocha"], extra: 3 },
    meta: { titulo: "Meta do trimestre", legenda: "T4 2026 · empresa toda", realizado: 192000, alvo: 300000 },
    atalhos: [
      { rotulo: "Receita",   icone: "dollar" },
      { rotulo: "Negócios",  icone: "kanban" },
      { rotulo: "Ligações",  icone: "phone" },
      { rotulo: "Reuniões",  icone: "calendar" }
    ],
    receita: {
      titulo: "Receita",
      periodos: {
        hoje:   { rotulo: "Hoje",   valor: 23300,  meta: 28000,  variacao: 4.2,  pontos: [12, 14, 13, 16, 18, 17, 19, 22, 21, 23, 24, 23] },
        semana: { rotulo: "Semana", valor: 141000, meta: 160000, variacao: 2.1,  pontos: [18, 21, 19, 24, 26, 25, 28] },
        mes:    { rotulo: "Mês",    valor: 612000, meta: 650000, variacao: -1.3, pontos: [120, 132, 128, 141, 150, 147, 158, 162] }
      },
      marcos: [
        { rotulo: "Seg", valor: 3400 }, { rotulo: "Ter", valor: 5100 }, { rotulo: "Qua", valor: 4600 },
        { rotulo: "Qui", valor: 5200 }, { rotulo: "Sex", valor: 3600 }
      ]
    },
    leads: { titulo: "Novos leads", legenda: "Últimos 7 dias", valor: 1235, variacao: 8.4, barras: [40, 55, 48, 70, 62, 85, 100] },
    aprovacoes: { titulo: "Aprovações", legenda: "3 pendentes", valor: 4800, texto: "Desconto acima do teto · 2 propostas" },
    vendas: {
      titulo: "Vendas (R$ mil)",
      periodos: {
        semana: { rotulo: "Semana", rotulos: ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"], valores: [38, 41, 52, 34, 22, 24, 9], destaque: 2 },
        mes:    { rotulo: "Mês",    rotulos: ["S1", "S2", "S3", "S4"], valores: [141, 162, 155, 154], destaque: 1 },
        ano:    { rotulo: "Ano",    rotulos: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"], valores: [380, 410, 455, 430, 480, 512, 498, 540, 575, 612, 0, 0], destaque: 9 }
      }
    },
    indicadores: [
      { tipo: "numero",   icone: "users",    rotulo: "Clientes",         valor: 2800, variacao: 3.1 },
      { tipo: "pipeline", icone: "target",   rotulo: "Pipeline",         valor: 1220000, variacao: 5.6, moeda: true,
        etapas: [{ rotulo: "Lead", pct: 80 }, { rotulo: "Qualificado", pct: 62 }, { rotulo: "Proposta", pct: 44 }, { rotulo: "Ganho", pct: 18 }] },
      { tipo: "linha",    icone: "activity", rotulo: "Usuários ativos",  valor: 307, variacao: 2.4, pontos: [12, 18, 14, 22, 19, 27, 24, 31, 28, 34] },
      { tipo: "numero",   icone: "ticket",   rotulo: "Chamados abertos", valor: 18, variacao: -12 }
    ],
    call: { titulo: "Call de descoberta · Cliente Exemplo", legenda: "Gravada ontem · 32 min", duracao_s: 1920 }
  },

  funil: {
    colunas: [
      { nome: "Lead",        probabilidade: 10, cor: "#94A3B8", cards: [
        { titulo: "Novo espaço de trabalho", empresa: "Acme Saúde", valor: 6400, data: "18/11", dono: "Ana Souza" },
        { titulo: "API de pagamentos",       empresa: "Borda Pay",  valor: 12800, data: "20/11", dono: "Bruno Lima" },
        { titulo: "Plano inicial",           empresa: "Cais Digital", valor: 2400, data: "22/11", dono: "Carla Dias" } ] },
      { nome: "Qualificado", probabilidade: 30, cor: "#60A5FA", cards: [
        { titulo: "Projeto piloto",          empresa: "Delta Obras", valor: 9200, data: "19/11", dono: "Diego Rocha" },
        { titulo: "Pacote de implantação",   empresa: "Eixo Log",   valor: 7500, data: "25/11", dono: "Ana Souza" } ] },
      { nome: "Proposta",    probabilidade: 55, cor: "#A78BFA", cards: [
        { titulo: "Upgrade de plano",        empresa: "Farol Ensino", valor: 18000, data: "21/11", dono: "Bruno Lima" },
        { titulo: "Módulo de relatórios",    empresa: "Guia Auto",  valor: 9800, data: "26/11", dono: "Carla Dias" },
        { titulo: "Expansão regional",       empresa: "Horto Verde", valor: 24500, data: "28/11", dono: "Diego Rocha" } ] },
      { nome: "Negociação",  probabilidade: 75, cor: "#FBBF24", cards: [
        { titulo: "Contrato anual",          empresa: "Ilha Foods", valor: 36000, data: "17/11", dono: "Ana Souza" },
        { titulo: "SLA de suporte",          empresa: "Jardim Lar", valor: 11200, data: "23/11", dono: "Bruno Lima" } ] },
      { nome: "Ganho",       probabilidade: 100, cor: "#34D399", ganho: true, cards: [
        { titulo: "Renovação anual",         empresa: "Kappa Tech", valor: 42000, data: "08/11", dono: "Carla Dias" },
        { titulo: "Expansão de licenças",    empresa: "Lumen Arq",  valor: 8600, data: "05/11", dono: "Diego Rocha" } ] }
    ]
  },

  clientes: {
    linhas: [
      { nome: "Lina Pereira",   email: "lina@exemplo.com",    empresa: "Acme Saúde",  status: "Ativo",   dono: "Ana Souza",   valor: 54200, ultimo: "Ontem" },
      { nome: "Sara Campos",    email: "sara@exemplo.com",    empresa: "Kappa Tech",  status: "Ativo",   dono: "Carla Dias",  valor: 48100, ultimo: "Ontem" },
      { nome: "Otávio Haddad",  email: "otavio@exemplo.com",   empresa: "Lumen Arq",   status: "Ativo",   dono: "Diego Rocha", valor: 38400, ultimo: "Há 2 dias" },
      { nome: "Amara Oliveira", email: "amara@exemplo.com",   empresa: "Ilha Foods",  status: "Teste",   dono: "Bruno Lima",  valor: 31500, ultimo: "Há 3 dias" },
      { nome: "Júlia Wilson",   email: "julia@exemplo.com", empresa: "Farol Ensino", status: "Ativo",  dono: "Bruno Lima",  valor: 25800, ultimo: "Há 4 dias" },
      { nome: "Dilan Costa",    email: "dilan@exemplo.com",    empresa: "Guia Auto",   status: "Lead",    dono: "Carla Dias",  valor: 0,     ultimo: "Há 5 dias" },
      { nome: "Eva Laurent",    email: "eva@exemplo.com",    empresa: "Horto Verde", status: "Ativo",   dono: "Diego Rocha", valor: 22400, ultimo: "Há 6 dias" },
      { nome: "Elis Lima",      email: "elis@exemplo.com",    empresa: "Jardim Lar",  status: "Teste",   dono: "Ana Souza",   valor: 19700, ultimo: "Há 8 dias" },
      { nome: "Beto Arruda",    email: "beto@exemplo.com",  empresa: "Cais Digital", status: "Perdido", dono: "Carla Dias", valor: 15400, ultimo: "Há 21 dias" }
    ]
  },

  produtos: {
    itens: [
      { nome: "Plano Essencial",   categoria: "Assinatura", preco: 490,   vendas: 182, ativo: true,  cor: "#F472B6", icone: "box" },
      { nome: "Plano Avançado",    categoria: "Assinatura", preco: 1290,  vendas: 96,  ativo: true,  cor: "#FBBF24", icone: "trend" },
      { nome: "Implantação",       categoria: "Serviço",    preco: 4800,  vendas: 31,  ativo: true,  cor: "#34D399", icone: "check" },
      { nome: "Relatórios",        categoria: "Módulo",     preco: 390,   vendas: 74,  ativo: true,  cor: "#60A5FA", icone: "chart" },
      { nome: "Suporte dedicado",  categoria: "Serviço",    preco: 1900,  vendas: 22,  ativo: false, cor: "#FB923C", icone: "phone" },
      { nome: "Integrações",       categoria: "Módulo",     preco: 690,   vendas: 58,  ativo: true,  cor: "#A78BFA", icone: "grid" },
      { nome: "Treinamento",       categoria: "Serviço",    preco: 2400,  vendas: 17,  ativo: true,  cor: "#22D3EE", icone: "users" },
      { nome: "Licença extra",     categoria: "Assinatura", preco: 120,   vendas: 410, ativo: true,  cor: "#F87171", icone: "ticket" }
    ]
  }
};
