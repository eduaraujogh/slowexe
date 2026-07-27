# Slowexe — site (memória do projeto)

Site da agência **Slowexe** (HTML/CSS/JS estático, multipágina, **bilíngue PT/EN** via `data-pt`/`data-en`).
Trabalhar nesta pasta; validar JS com `node --check`; manter consistência entre páginas.

## ⭐ Fonte da verdade de design
**SEMPRE seguir `DESIGN_SYSTEM.md`** (nesta pasta) para qualquer página nova ou edição —
cores, tipografia, espaçamento, raios, sombras, movimento e componentes foram extraídos da home.

Inegociáveis:
- Único destaque: salmão `#F07A65` (hover `#E2674F`). Não inventar outras cores de marca.
- Títulos = **Bricolage Grotesque**; corpo/UI = **Inter**. Eyebrow uppercase, tracking `.1em`.
- Seção **escura** `#0A0B0D` (cards `#15171B`, borda `#23262C`, texto sec. `#A0A4AD`).
  Seção **clara** `#fff`/creme `#faf9f7` (borda `#ece9e4`, texto sec. `#6b7078`, labels `#9aa0a8`).
- Raios: pill `999`, botão `8`, tile de ícone `12`, **card de grid `20`**, mídia/destaque `24`.
- **HOVER PADRÃO de card:** sobe `-12px`, gira `-2.5°`, vira branco, sombra `0 36px 80px rgba(240,122,101,.32)`.
  (O flip escuro→branco precisa de fundo escuro atrás.)
- Easing padrão `cubic-bezier(.22,1,.36,1)`; entrada via `[data-reveal]`; CTAs/links usam `.roll`.
- Esteiras: track duplicado por JS, pausa no hover, fade nas bordas.

## Páginas
- `index.html` — home (REFERÊNCIA visual).
- `servicos.html` — hub de todos os serviços.
- `servico-branding.html`, `servico-rebranding.html` — páginas de serviço.
- `projetos.html` (índice) + `projeto.html` (case study).
- `contato.html` — contato + modal de agendamento.

## Workflow
- Editar na pasta `Site Slowexe`; sincronizar cópia em `outputs`.
- Cada item do mega-menu "Serviços" aponta pra `servicos.html`; Branding/Rebranding pras páginas próprias.
