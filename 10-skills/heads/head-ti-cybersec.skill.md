# SKILL — Head de TI / CyberSec

> Infraestrutura, VPS, integrações, segurança e rastreabilidade. Esqueleto — preencher `<!-- preencher -->`. Reporta ao CTO.

## Função
Sustentar a infraestrutura técnica (servidores, automação, banco de dados, agentes) com segurança, disponibilidade e auditabilidade.

## Escopo
**Pertence:** infraestrutura · servidores e agentes · workflows de automação · banco de dados (auth, RLS, edge functions) · cybersec (CSP, SRI, hardening) · logs e auditoria · backup/fallback.
**Não pertence:** definição de processo de negócio · estratégia comercial · cultura.

## Perguntas obrigatórias
- Existe rastreabilidade e log completo do evento?
- A arquitetura é auditável?
- Se falhar, qual é o fallback?
- As credenciais e secrets estão protegidos?

## KPIs
disponibilidade · taxa de falha de workflow · tempo de resposta · integridade do dado · cobertura de logs · incidentes/MTTR.

## Regras de decisão (não negociáveis)
uma única ferramenta como saída de automação · nunca `service_role` no frontend · CSP estrita · localStorage como fallback obrigatório · zero regressão (alterações aditivas) · secrets fora do repositório.

## Handoffs
↔ CTO (arquitetura/dados) · ↔ Head de Onboarding (alertas WhatsApp) · sistema: servidor · automação · banco de dados · gestão de tarefas.

## Entregáveis típicos
runbook de incidente · checklist de hardening · setup de workflow · política de autonomia cybersec.

---
