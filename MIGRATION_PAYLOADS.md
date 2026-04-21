# Documentação de Migração de Payloads (Tsurugi -> Protus)

Este documento registra as modificações e adições feitas para que o motor de geração de payloads e bypasses da Tsurugi funcionasse nativamente dentro da `Protus`.

## O que foi Adicionado

1. **Pasta `payloads/`**
   - Foram adicionadas as listas ricas de injeção originais da Tsurugi (`sqli.txt`, `lfi.txt`, `xss.txt`).
   - Esta pasta funciona como fonte local primária, permitindo o lazy-loading na memória quando requisitado, sem explodir a RAM.

2. **Módulo `core/payloads.py`**
   - Este arquivo foi copiado de `HikariSystem-Tsurugi/core/payloads.py` e customizado para a arquitetura Protus.
   - Fornece funções ativas como `generate_sqli_payloads`, `generate_xss_payloads`, etc. além do mutador embutido pra bypass de WAF.

## O que foi Mexido/Adaptado

1. **Dependências Visuais Removidas (`core/payloads.py`)**
   - Importações inexistentes na Protus (`from core.ui import log_info, log_warning, console`) foram removidas.
   - O uso da biblioteca `rich` e Tabelas Avançadas foi totalmente descartado em favor do `print()` padrão do Python para que o `print_payload_stats()` rodasse bonito porém sem depender de pacotes externos.

2. **Integração no CLI (`core/config.py`)**
   - O interpretador em `base/config.py` foi embutido para aceitar sub-argumentos de `show`.
   - Incluiu-se o parâmetro e validação `if args.item == 'payloads':`. Ao digitar `show payloads` no terminal interativo `pts >>`, o sistema importa temporariamente o payload e exibe as estatísticas pra comprovar o funcionamento.

## Como Testar

Abra o Protus pelo console:
```bash
python protus.py
```
Em seguida, insira o comando adaptado:
```
pts >> show payloads
```

Isso fará o carregamento local, exibindo a tabela com todas as contagens operacionais, e ainda deve testar a engine mostrando um _"Example Generated SQLi Payload"_ extraído e renderizado na hora.
