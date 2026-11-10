# ECOAR — Laboratório de Oratória Bilíngue

Site público: https://ecoar.grupoeduardabispo.com.br/

Projeto ECOAR, vinculado institucionalmente ao GEB Empresarial — Grupo Eduarda Bispo.

## Publicação
- Código estático em `site/`.
- GitHub Actions publica o conteúdo de `site/` na pasta `public_html/ecoar/` da hospedagem Locaweb a cada atualização na branch `main`.
- Segredos de repositório necessários: `HOST`, `USER`, `PASS`.
- A rotina não exclui arquivos remotos (`mirror --reverse` sem `--delete`) para evitar remoções imprevistas.
- A efetiva publicação depende de DNS, SSL, permissões FTP e execução bem-sucedida do workflow.

## Fonte editorial
A estrutura e os textos iniciais foram adaptados da página ECOAR já existente no GEB Empresarial, respeitando as diretrizes de divulgação do laboratório. Não são anunciadas datas de edições sem confirmação.

## Organização
`site/index.html`: apresentação pública.
`site/robots.txt`: orientação de rastreamento.
`site/sitemap.xml`: endereços locais, sem outros domínios.
`.github/workflows/deploy.yml`: implantação por FTP na Locaweb.
