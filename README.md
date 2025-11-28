# Desktop Cleaner

O **Desktop Cleaner** é um conjunto de scripts em Python projetado para organizar automaticamente seus arquivos e analisar a "saúde" da organização das suas pastas.

## Funcionalidades

### 1. Organizador Automático (`cleaner.py`)
Organiza arquivos das pastas **Desktop**, **Downloads** e **Videos** para as pastas padrão do sistema:
- 🖼️ **Imagens** -> `Pictures`
- 🎥 **Vídeos** -> `Videos`
- 📄 **Documentos e outros** -> `Documents`
- 🎵 **Música** -> `Music`

**Recursos:**
- Ignora arquivos de sistema e temporários.
- Gera um histórico para permitir desfazer as ações.

### 2. Analisador de Pastas (`analyser.py`)
Gera um relatório detalhado sobre o estado das suas pastas, incluindo:
- 📊 Nota de organização (0 a 100).
- 🔍 Identificação de arquivos "soltos" e bagunça.
- 📉 Análise de profundidade de pastas (hierarquia).
- 🏷️ Detecção de padrões de nomes (ex: nomes genéricos de câmera).
- 💡 Dicas personalizadas para melhorar a organização.

### 3. Desfazer (`cleaner.py --undo`)
Se algo não sair como esperado, você pode reverter a última organização com um único comando.

## Como Usar

### Pré-requisitos
- Python 3.x instalado.

### Instalação
1. Clone este repositório ou baixe os arquivos.
2. Não é necessário instalar bibliotecas externas (usa apenas bibliotecas padrão do Python).

### Executando a Limpeza
Para organizar seus arquivos:
```bash
python cleaner.py
```

### Desfazendo a Limpeza
Para desfazer a última ação:
```bash
python cleaner.py --undo
```

### Gerando Relatório
Para ver a análise das suas pastas:
```bash
python analyser.py
```

## Estrutura do Projeto
- `cleaner.py`: Script principal de organização.
- `analyser.py`: Script de análise e pontuação.
- `cleanup_history.json`: Arquivo gerado automaticamente para armazenar histórico (não deve ser editado manualmente).

## Notas
- O script move arquivos. Embora seguro, recomenda-se ter backup de dados importantes antes de rodar scripts de automação de arquivos.
- O arquivo `cleanup_history.json` é local e contém caminhos dos seus arquivos, por isso é ignorado no git.
