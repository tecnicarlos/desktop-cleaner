# Como Postar este Projeto no GitHub 🐙

Este guia passo a passo vai te ajudar a colocar o **Faxineiro IA** no GitHub.

## Passo 1: Criar um Repositório no GitHub
1. Acesse [github.com](https://github.com) e faça login.
2. Clique no botão **New** (ou no ícone `+` no canto superior direito -> **New repository**).
3. **Repository name**: Digite `faxineiro-ia` (ou outro nome que preferir).
4. **Description**: (Opcional) "Scripts Python para organização automática de arquivos".
5. **Public/Private**: Escolha se quer que seja público ou privado.
6. **Initialize this repository with**: **NÃO MARQUE NADA** (não adicione README, .gitignore ou License agora, pois já criamos isso localmente).
7. Clique em **Create repository**.

## Passo 2: Preparar o Git no seu Computador
Abra o terminal (Prompt de Comando ou PowerShell) na pasta do projeto: `c:\Users\Usuario\Documents\01 PROGRAMAS\FAXINEIRO IA`.

Execute os seguintes comandos um por um:

1. **Inicializar o Git**:
   ```powershell
   git init
   ```

2. **Adicionar os arquivos**:
   Isso prepara todos os arquivos (exceto os ignorados pelo `.gitignore`) para serem enviados.
   ```powershell
   git add .
   ```

3. **Fazer o primeiro commit**:
   Isso salva a versão atual dos arquivos no histórico do Git.
   ```powershell
   git commit -m "Primeiro commit: Scripts de organização e análise"
   ```

4. **Renomear a branch principal (opcional, mas recomendado)**:
   O padrão moderno é usar `main`.
   ```powershell
   git branch -M main
   ```

## Passo 3: Conectar e Enviar para o GitHub
Volte para a página do repositório que você criou no GitHub. Você verá uma seção chamada **"…or push an existing repository from the command line"**. Copie o comando que começa com `git remote add origin...`.

Deve ser algo parecido com isso (substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub):

1. **Adicionar a origem remota**:
   ```powershell
   git remote add origin https://github.com/SEU_USUARIO/faxineiro-ia.git
   ```

2. **Enviar os arquivos (Push)**:
   ```powershell
   git push -u origin main
   ```

   *Se for a primeira vez, o Git pode pedir para você fazer login no GitHub.*

## Pronto! 🎉
Atualize a página do GitHub e você verá seus arquivos lá.

---

## Dicas Extras
- **Atualizações**: Se você modificar o código no futuro, basta rodar:
  ```powershell
  git add .
  git commit -m "Descrição do que mudou"
  git push
  ```
