/**
 * JavaScript para a página principal do workspace.
 *
 * Gerencia todas as funcionalidades interativas da página principal:
 * - Modal de criação de pasta
 * - Seleção e arraste de itens (drag and drop)
 * - Renomear e deletar itens
 * - Navegação por drag and drop em breadcrumbs
 *
 * Utiliza IIFE para evitar poluição do escopo global e aguarda
 * o carregamento completo do DOM antes de inicializar.
 */
(function () {

    'use strict';

    // Aguarda o carregamento completo do DOM
    document.addEventListener("DOMContentLoaded", function () {
    
        // Seleciona todos os itens clicáveis
        const items = document.querySelectorAll(".selectable-item");
        let selectedItem = null;

        // Referências ao botão e formulário de deletar
        const deleteButton = document.getElementById("delete_selected");
        const deleteForm = document.getElementById("delete_form");

        // Referências ao botão e modal de renomear
        const renameButton = document.getElementById("rename_selected");
        const renameModal = document.getElementById("rename_modal");
        const renameForm = document.getElementById("rename_form");
        const renameInput = document.getElementById("rename_input");
        const renameCancelButton = document.getElementById("rename_cancel");

        /**
         * Atualiza o estado do botão de remover baseado na seleção
         */
        function updateDeleteButton() {
            if (!deleteButton) return;
            
            if (selectedItem) {
                deleteButton.disabled = false;
            } else {
                deleteButton.disabled = true;
            }
        }

        /**
         * Atualiza o estado do botão de renomear baseado na seleção
         * Habilita se o item selecionado for uma pasta ou arquivo
         */
        function updateRenameButton() {
            if (!renameButton) return;
            
            if (selectedItem) {
                // Tenta múltiplas formas de obter o tipo do item
                let itemKind = null;
                
                // Primeiro tenta getAttribute (mais confiável)
                const attrKind = selectedItem.getAttribute("data-kind");
                if (attrKind) {
                    itemKind = attrKind.trim();
                }
                
                // Se não encontrou, tenta dataset
                if (!itemKind && selectedItem.dataset && selectedItem.dataset.kind) {
                    itemKind = String(selectedItem.dataset.kind).trim();
                }
                
                // Se ainda não encontrou, tenta acessar diretamente
                if (!itemKind && selectedItem.hasAttribute && selectedItem.hasAttribute("data-kind")) {
                    itemKind = selectedItem.getAttribute("data-kind")?.trim();
                }
                
                if (itemKind === "folder" || itemKind === "file") {
                    renameButton.disabled = false;
                } else {
                    renameButton.disabled = true;
                }
            } else {
                renameButton.disabled = true;
            }
        }

        /**
         * Remove seleção de todos os itens
         */
        function clearSelection() {
            items.forEach(item => {
                item.classList.remove("ring-2", "ring-blue-500");
            });
            selectedItem = null;
            updateDeleteButton();
            updateRenameButton();
        }

        /**
         * Seleciona visualmente um item
         */
        function selectItem(item) {
            clearSelection();
            item.classList.add("ring-2", "ring-blue-500");
            selectedItem = item;
            updateDeleteButton();
            updateRenameButton();
        }

        // Variável para rastrear se um drag está em andamento
        let isDragging = false;

        // Aplica eventos a cada item
        items.forEach(item => {

            // Clique simples → seleciona
            item.addEventListener("click", function (event) {
                // Não previne o comportamento padrão se um drag acabou de ocorrer
                if (isDragging) {
                    isDragging = false;
                    return;
                }
                event.preventDefault();
                selectItem(item);
            });

            // Duplo clique → navega
            item.addEventListener("dblclick", function () {
                if (isDragging) return;
                
                const url = item.dataset.url;
                const target = item.dataset.target || "_self";

                if (!url) return;

                if (target === "_blank") {
                    window.open(url, "_blank");
                } else {
                    window.location.href = url;
                }
            });

        }); // items.forEach

        // Clique fora → limpa seleção
        document.addEventListener("click", function (event) {
            const clickedItem = event.target.closest(".selectable-item");
            // Não limpa seleção se clicar em botões ou formulários
            const clickedButton = event.target.closest("button");
            const clickedForm = event.target.closest("form");
            const preserveSelection = event.target.closest("[data-preserve-selection]");
            
            if (!clickedItem && !clickedButton && !clickedForm && !preserveSelection) {
                clearSelection();
            }
        });

        // Limpa seleção ao pressionar ESC
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                clearSelection();
            }
        });


        // ============================================================
        // VALIDAÇÃO DO FORMULÁRIO DE CRIAÇÃO DE PASTA
        // ============================================================

        /**
         * Obtém a lista de nomes de pastas existentes no diretório
         * atual.
         * 
         * Busca todos os elementos com data-kind="folder" e extrai
         * seus nomes para validação de duplicação.
         * 
         * @returns {Array<string>} Array com os nomes das pastas
         *                          existentes (em minúsculas)
         */
        function getExistingFolderNames() {
            const folderItems = document.querySelectorAll(
                '[data-kind="folder"]'
            );
            const folderNames = [];
            
            folderItems.forEach(function (item) {
                // O nome da pasta está no segundo span dentro do item
                // Estrutura: <span><span>📁</span><span>Nome</span></span>
                // Busca todos os spans aninhados
                const allSpans = item.querySelectorAll("span span");
                
                if (allSpans.length >= 2) {
                    // Pega o último span que contém o nome da pasta
                    const nameSpan = allSpans[allSpans.length - 1];
                    const folderName = nameSpan.textContent.trim();
                    
                    // Normaliza o nome para comparação (minúsculas)
                    if (folderName) {
                        const normalized = folderName.toLowerCase();
                        folderNames.push(normalized);
                    }
                }
            });
            
            return folderNames;
        }

        /**
         * Obtém a lista de nomes de arquivos existentes no diretório atual.
         * 
         * Busca todos os elementos com data-kind="file" e extrai
         * seus nomes para validação de duplicação.
         * 
         * @returns {Array<string>} Array com os nomes dos arquivos
         *                          existentes (em minúsculas)
         */
        function getExistingFileNames() {
            const fileItems = document.querySelectorAll(
                '[data-kind="file"]'
            );
            const fileNames = [];
            
            fileItems.forEach(function (item) {
                // O nome do arquivo está no segundo span dentro do item
                // Estrutura: <span><span>📄</span><span>Nome</span></span>
                // Busca todos os spans aninhados
                const allSpans = item.querySelectorAll("span span");
                
                if (allSpans.length >= 2) {
                    // Pega o último span que contém o nome do arquivo
                    const nameSpan = allSpans[allSpans.length - 1];
                    const fileName = nameSpan.textContent.trim();
                    
                    // Normaliza o nome para comparação (minúsculas)
                    if (fileName) {
                        const normalized = fileName.toLowerCase();
                        fileNames.push(normalized);
                    }
                }
            });
            
            return fileNames;
        }

        /**
         * Valida se o nome da pasta já existe no diretório atual.
         * 
         * @param {string} folderName - Nome da pasta a ser validado
         * @param {string} excludeName - Nome a ser excluído da validação (opcional)
         * @returns {boolean} true se o nome já existe, false caso
         *                   contrário
         */
        function folderNameExists(folderName, excludeName = null) {
            if (!folderName || !folderName.trim()) {
                return false;
            }
            
            const existingNames = getExistingFolderNames();
            const normalizedName = folderName.trim().toLowerCase();
            
            // Se há um nome para excluir (ex: nome atual da pasta sendo renomeada),
            // remove-o da lista antes de verificar
            if (excludeName) {
                const normalizedExclude = excludeName.trim().toLowerCase();
                const index = existingNames.indexOf(normalizedExclude);
                if (index > -1) {
                    existingNames.splice(index, 1);
                }
            }
            
            return existingNames.includes(normalizedName);
        }

        /**
         * Valida se o nome do arquivo já existe no diretório atual.
         * 
         * @param {string} fileName - Nome do arquivo a ser validado
         * @param {string} excludeName - Nome a ser excluído da validação (opcional)
         * @returns {boolean} true se o nome já existe, false caso
         *                   contrário
         */
        function fileNameExists(fileName, excludeName = null) {
            if (!fileName || !fileName.trim()) {
                return false;
            }
            
            const existingNames = getExistingFileNames();
            const normalizedName = fileName.trim().toLowerCase();
            
            // Se há um nome para excluir (ex: nome atual do arquivo sendo renomeado),
            // remove-o da lista antes de verificar
            if (excludeName) {
                const normalizedExclude = excludeName.trim().toLowerCase();
                const index = existingNames.indexOf(normalizedExclude);
                if (index > -1) {
                    existingNames.splice(index, 1);
                }
            }
            
            return existingNames.includes(normalizedName);
        }

        /**
         * Exibe a mensagem de erro no modal.
         * 
         * @param {HTMLElement} errorElement - Elemento que exibe o
         *                                    erro
         * @param {string} message - Mensagem de erro a ser exibida
         */
        function showErrorMessage(errorElement, message) {
            if (!errorElement) return;
            
            errorElement.textContent = message;
            errorElement.classList.remove("hidden");
        }

        /**
         * Remove a mensagem de erro do modal.
         * 
         * @param {HTMLElement} errorElement - Elemento que exibe o
         *                                    erro
         */
        function hideErrorMessage(errorElement) {
            if (!errorElement) return;
            
            errorElement.textContent = "";
            errorElement.classList.add("hidden");
        }

        // Referência ao modal de criação de pasta
        const createFolderModal = document.getElementById(
            "create_folder_modal"
        );
        
        /**
         * Função para inicializar a validação do formulário de pasta
         */
        function initializeFolderValidation() {
            if (!createFolderModal) return;
            
            const folderNameInput = createFolderModal.querySelector(
                "#folder_name"
            );
            const errorMessage = createFolderModal.querySelector(
                "#server-error"
            );
            const createFolderForm = createFolderModal.querySelector(
                "form"
            );
            
            if (!folderNameInput || !errorMessage) return;
            
            // Remove listeners anteriores se existirem (usando clone)
            // para evitar duplicação
            const hasInputListener = folderNameInput.hasAttribute(
                "data-validation-attached"
            );
            
            if (!hasInputListener) {
                // Validação em tempo real enquanto o usuário digita
                folderNameInput.addEventListener("input", function () {
                    const folderName = this.value.trim();
                    
                    // Se o campo estiver vazio, remove o erro
                    if (!folderName) {
                        hideErrorMessage(errorMessage);
                        return;
                    }
                    
                    // Verifica se o nome já existe
                    if (folderNameExists(folderName)) {
                        showErrorMessage(
                            errorMessage,
                            "Já existe uma pasta com esse nome " +
                            "nesse diretório."
                        );
                    } else {
                        hideErrorMessage(errorMessage);
                    }
                });
                
                folderNameInput.setAttribute(
                    "data-validation-attached",
                    "true"
                );
            }
            
            // Previne submissão do formulário se houver erro
            if (createFolderForm && 
                !createFolderForm.hasAttribute("data-submit-listener")) {
                createFolderForm.addEventListener("submit", function (
                    event
                ) {
                    const folderName = folderNameInput.value.trim();
                    
                    // Se o campo estiver vazio, permite validação
                    // HTML5 padrão
                    if (!folderName) {
                        return;
                    }
                    
                    // Se o nome já existe, previne a submissão
                    if (folderNameExists(folderName)) {
                        event.preventDefault();
                        showErrorMessage(
                            errorMessage,
                            "Já existe uma pasta com esse nome " +
                            "nesse diretório."
                        );
                        // Foca no campo para facilitar correção
                        folderNameInput.focus();
                        folderNameInput.select();
                    }
                });
                
                createFolderForm.setAttribute(
                    "data-submit-listener",
                    "true"
                );
            }
        }


        // ============================================================
        // SISTEMA DE COMANDOS PARA MODAIS
        // ============================================================

        /**
         * Sistema de delegação de eventos para comandos customizados.
         * 
         * Este sistema permite que elementos HTML com atributos
         * "command" e "commandfor" executem ações específicas,
         * como abrir/fechar modais.
         * 
         * Exemplo de uso no HTML:
         * <button command="show-modal" 
         *         commandfor="create_folder_modal">
         *     Nova Pasta
         * </button>
         */

        // Usa delegação de eventos para capturar cliques em
        // elementos com atributo "command"
        document.addEventListener("click", function (event) {
            // Verifica se o elemento clicado (ou seu pai) tem
            // o atributo "command"
            const commandElement = event.target.closest(
                '[command]'
            );
            
            // Se não encontrou, ignora o evento
            if (!commandElement) return;
            
            // Obtém o tipo de comando (ex: "show-modal", "close")
            const command = commandElement.getAttribute("command");
            
            // Obtém o alvo do comando (ex: "create_folder_modal")
            const commandFor = commandElement.getAttribute(
                "commandfor"
            );
            
            // Se não há comando ou alvo, ignora
            if (!command || !commandFor) return;
            
            // ========================================================
            // COMANDO: show-modal
            // ========================================================
            // Abre um modal e foca no campo de input
            if (command === "show-modal") {
                // Busca o elemento <dialog> pelo ID especificado
                const modal = document.getElementById(commandFor);
                
                // Se o modal não existe, não faz nada
                if (!modal) return;
                
                // Limpa o campo e mensagem de erro ao abrir o modal
                if (commandFor === "create_folder_modal") {
                    const inputField = modal.querySelector(
                        "#folder_name"
                    );
                    const errorMessage = modal.querySelector(
                        "#server-error"
                    );
                    
                    if (inputField) {
                        inputField.value = "";
                        // Dispara evento input para garantir validação
                        inputField.dispatchEvent(new Event("input", {
                            bubbles: true
                        }));
                    }
                    if (errorMessage) {
                        errorMessage.textContent = "";
                        errorMessage.classList.add("hidden");
                    }
                    
                    // Garante que a validação está inicializada
                    setTimeout(initializeFolderValidation, 50);
                }
                
                // Abre o modal usando a API nativa do HTML5
                modal.showModal();
                
                // Busca o campo de input dentro do modal
                // Usa o ID "folder_name" que está no HTML
                const inputField = modal.querySelector(
                    "#folder_name"
                );
                
                // Se o campo existe, foca nele
                // O setTimeout garante que o foco aconteça após
                // o modal estar totalmente renderizado
                if (inputField) {
                    setTimeout(function () {
                        inputField.focus();
                        // Seleciona todo o texto (se houver)
                        // para facilitar substituição
                        inputField.select();
                    }, 100);
                }
            }
            
            // ========================================================
            // COMANDO: close
            // ========================================================
            // Fecha um modal
            if (command === "close") {
                // Busca o elemento <dialog> pelo ID especificado
                const modal = document.getElementById(commandFor);
                
                // Se o modal não existe, não faz nada
                if (!modal) return;
                
                // Limpa o campo e mensagem de erro ao cancelar
                if (commandFor === "create_folder_modal") {
                    const inputField = modal.querySelector(
                        "#folder_name"
                    );
                    const errorMessage = modal.querySelector(
                        "#server-error"
                    );
                    
                    if (inputField) {
                        inputField.value = "";
                    }
                    if (errorMessage) {
                        errorMessage.textContent = "";
                        errorMessage.classList.add("hidden");
                    }
                }
                
                // Fecha o modal usando a API nativa do HTML5
                modal.close();
            }
        });

        // Inicializa a validação quando o DOM estiver pronto
        if (createFolderModal) {
            // Aguarda um pouco para garantir que o DOM está completo
            setTimeout(function () {
                initializeFolderValidation();
                
                // Se o modal abre automaticamente (erro do servidor),
                // garante que a validação esteja ativa
                if (createFolderModal.hasAttribute("data-auto-open")) {
                    // Abre o modal automaticamente
                    createFolderModal.showModal();
                    
                    // Aguarda o modal abrir completamente
                    setTimeout(function () {
                        initializeFolderValidation();
                    }, 300);
                }
            }, 100);
        }


        const uploadButton = document.getElementById("upload_button");
        const uploadMenu = document.getElementById("upload_menu");

        // Mostrar dropdown ao clicar
        uploadButton.addEventListener("click", function (event) {
            event.stopPropagation();
            uploadMenu.classList.toggle("hidden");
        });

        // Fechar dropdown ao pressionar ESC
        document.addEventListener("keydown", function(event) {
            if (event.key === "Escape" && !uploadMenu.classList.contains("hidden")) {
                uploadMenu.classList.add("hidden");
            }
        });

        // Fechar dropdown ao clicar fora
        document.addEventListener("click", function(event) {
            // Verifica se o clique foi fora do botão e do menu
            const isClickInside = uploadButton.contains(event.target) || 
                                uploadMenu.contains(event.target);
            
            if (!isClickInside && !uploadMenu.classList.contains("hidden")) {
                uploadMenu.classList.add("hidden");
            }
        });


        // ============================================================
        // UPLOAD DE PASTA
        // ============================================================

        /**
         * Processa o upload de uma pasta inteira.
         * 
         * Quando o usuário seleciona uma pasta usando o input com
         * webkitdirectory, extrai os caminhos relativos dos arquivos
         * e preenche os campos necessários antes de submeter o formulário.
         */
        const folderInput = document.getElementById("folder_input");
        const uploadFolderForm = document.getElementById("upload_folder_form");
        const filePathsInput = document.getElementById("file_paths_json");
        const detectedFolderNameInput = document.getElementById("detected_folder_name");

        if (folderInput && uploadFolderForm && filePathsInput && detectedFolderNameInput) {
            folderInput.addEventListener("change", function(event) {
                const files = event.target.files;
                
                if (!files || files.length === 0) {
                    return;
                }

                // Fecha o dropdown de upload
                if (uploadMenu) {
                    uploadMenu.classList.add("hidden");
                }

                // Extrai os caminhos relativos dos arquivos
                const filePaths = [];
                let folderName = null;

                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    // webkitRelativePath contém o caminho relativo da pasta selecionada
                    const relativePath = file.webkitRelativePath || file.name;
                    filePaths.push(relativePath);

                    // Extrai o nome da pasta raiz (primeiro diretório do caminho)
                    if (!folderName && relativePath.includes("/")) {
                        const pathParts = relativePath.split("/");
                        if (pathParts.length > 0 && pathParts[0].trim()) {
                            folderName = pathParts[0].trim();
                        }
                    }
                }

                // Se não conseguiu detectar o nome da pasta, usa um nome padrão
                if (!folderName) {
                    folderName = "Pasta Upload";
                }

                // Preenche os campos ocultos do formulário
                filePathsInput.value = JSON.stringify(filePaths);
                detectedFolderNameInput.value = folderName;

                // Submete o formulário
                uploadFolderForm.submit();
            });
        }


        // ====================================================================
        // BOTÃO DE DELETAR ITEM
        // ====================================================================

        if (deleteButton && deleteForm) {
            deleteButton.addEventListener("click", (event) => {
                event.preventDefault();
                if (!selectedItem) return;

                const kind = selectedItem.dataset.kind;
                const id = selectedItem.dataset.id;
                if (!kind || !id) return;

                // Define a URL de ação baseada no tipo de item
                let action = "";
                if (kind === "folder") {
                    action = `/delete-folder/${id}/`;
                } else if (kind === "file") {
                    action = `/delete-file/${id}/`;
                }

                // Submete o formulário com a ação correta
                if (action) {
                    deleteForm.action = action;
                    deleteForm.submit();
                }
            });
        }

        // Inicializa o estado dos botões ao carregar a página
        updateDeleteButton();
        updateRenameButton();


        // ====================================================================
        // BOTÃO DE RENOMEAR ITEM SELECIONADO (PASTA/ARQUIVO)
        // ====================================================================

        /**
         * Obtém o nome atual do item selecionado
         * Extrai o nome do segundo span dentro do item
         */
        function getSelectedItemName() {
            if (!selectedItem) return "";
            
            // Estrutura: <span><span>📁</span><span>Nome</span></span>
            const allSpans = selectedItem.querySelectorAll("span span");
            
            if (allSpans.length >= 2) {
                // Pega o último span que contém o nome
                const nameSpan = allSpans[allSpans.length - 1];
                return nameSpan.textContent.trim();
            }
            
            return "";
        }

        if (renameButton && renameModal && renameForm && renameInput) {
            // Referência ao elemento de erro do modal de renomear
            const renameErrorElement = document.getElementById("rename-error");
            
            // Variáveis para armazenar o nome atual e tipo do item sendo renomeado
            let currentItemName = "";
            let currentItemKind = "";

            /**
             * Inicializa a validação do formulário de renomear
             */
            function initializeRenameValidation() {
                if (!renameInput || !renameErrorElement) return;

                // Remove listeners anteriores se existirem
                const hasInputListener = renameInput.hasAttribute(
                    "data-validation-attached"
                );

                if (!hasInputListener) {
                    // Validação em tempo real enquanto o usuário digita
                    renameInput.addEventListener("input", function () {
                        const newName = this.value.trim();

                        // Se o campo estiver vazio, remove o erro
                        if (!newName) {
                            hideErrorMessage(renameErrorElement);
                            return;
                        }

                        // Se o nome for igual ao atual, não há erro
                        if (newName.toLowerCase() === currentItemName.toLowerCase()) {
                            hideErrorMessage(renameErrorElement);
                            return;
                        }

                        // Verifica se o nome já existe baseado no tipo do item
                        let nameExists = false;
                        let errorMessage = "";

                        if (currentItemKind === "folder") {
                            nameExists = folderNameExists(newName, currentItemName);
                            errorMessage = "Já existe uma pasta com esse nome " +
                                         "nesse diretório.";
                        } else if (currentItemKind === "file") {
                            nameExists = fileNameExists(newName, currentItemName);
                            errorMessage = "Já existe um arquivo com esse nome " +
                                         "nesse diretório.";
                        }

                        if (nameExists) {
                            showErrorMessage(renameErrorElement, errorMessage);
                        } else {
                            hideErrorMessage(renameErrorElement);
                        }
                    });

                    renameInput.setAttribute(
                        "data-validation-attached",
                        "true"
                    );
                }

                // Previne submissão do formulário se houver erro
                if (renameForm && 
                    !renameForm.hasAttribute("data-submit-listener")) {
                    renameForm.addEventListener("submit", function (event) {
                        const newName = renameInput.value.trim();

                        // Se o campo estiver vazio, permite validação HTML5 padrão
                        if (!newName) {
                            return;
                        }

                        // Se o nome for igual ao atual, permite submissão
                        if (newName.toLowerCase() === currentItemName.toLowerCase()) {
                            return;
                        }

                        // Verifica se o nome já existe baseado no tipo do item
                        let nameExists = false;
                        let errorMessage = "";

                        if (currentItemKind === "folder") {
                            nameExists = folderNameExists(newName, currentItemName);
                            errorMessage = "Já existe uma pasta com esse nome " +
                                         "nesse diretório.";
                        } else if (currentItemKind === "file") {
                            nameExists = fileNameExists(newName, currentItemName);
                            errorMessage = "Já existe um arquivo com esse nome " +
                                         "nesse diretório.";
                        }

                        // Se o nome já existe, previne a submissão
                        if (nameExists) {
                            event.preventDefault();
                            showErrorMessage(renameErrorElement, errorMessage);
                            // Foca no campo para facilitar correção
                            renameInput.focus();
                            renameInput.select();
                        }
                    });

                    renameForm.setAttribute(
                        "data-submit-listener",
                        "true"
                    );
                }
            }

            // Abre o modal de renomear quando clicar no botão
            renameButton.addEventListener("click", (event) => {
                event.preventDefault();
                if (!selectedItem) return;

                const kind = selectedItem.getAttribute("data-kind") || selectedItem.dataset?.kind;
                const id = selectedItem.getAttribute("data-id") || selectedItem.dataset?.id;
                
                // Permite renomear pastas e arquivos
                if ((kind !== "folder" && kind !== "file") || !id) return;

                // Preenche o campo com o nome atual
                currentItemName = getSelectedItemName();
                currentItemKind = kind;
                renameInput.value = currentItemName;
                
                // Atualiza o título do modal baseado no tipo
                const renameTitle = document.getElementById("rename-title");
                if (renameTitle) {
                    if (kind === "folder") {
                        renameTitle.textContent = "Renomear pasta";
                    } else if (kind === "file") {
                        renameTitle.textContent = "Renomear arquivo";
                    }
                }
                
                // Limpa mensagem de erro ao abrir o modal
                if (renameErrorElement) {
                    hideErrorMessage(renameErrorElement);
                }
                
                // Define a action do formulário baseado no tipo
                if (kind === "folder") {
                    renameForm.action = `/rename-folder/${id}/`;
                } else if (kind === "file") {
                    renameForm.action = `/rename-file/${id}/`;
                }
                
                // Inicializa a validação
                initializeRenameValidation();
                
                // Abre o modal
                renameModal.showModal();
                
                // Foca no campo de input após o modal abrir
                setTimeout(() => {
                    renameInput.focus();
                    renameInput.select();
                }, 100);
            });

            // Fecha o modal ao clicar em cancelar
            if (renameCancelButton) {
                renameCancelButton.addEventListener("click", () => {
                    renameModal.close();
                    renameInput.value = "";
                    currentItemName = "";
                    currentItemKind = "";
                    if (renameErrorElement) {
                        hideErrorMessage(renameErrorElement);
                    }
                });
            }

            // Fecha o modal ao clicar fora (backdrop)
            renameModal.addEventListener("click", (event) => {
                // Se o clique foi no backdrop (não no conteúdo do modal)
                if (event.target === renameModal) {
                    renameModal.close();
                    renameInput.value = "";
                    currentItemName = "";
                    currentItemKind = "";
                    if (renameErrorElement) {
                        hideErrorMessage(renameErrorElement);
                    }
                }
            });

            // Fecha o modal ao pressionar ESC
            renameModal.addEventListener("keydown", (event) => {
                if (event.key === "Escape") {
                    renameModal.close();
                    renameInput.value = "";
                    currentItemName = "";
                    currentItemKind = "";
                    if (renameErrorElement) {
                        hideErrorMessage(renameErrorElement);
                    }
                }
            });
        }

        // ====================================================================
        // DRAG AND DROP - MOVER ARQUIVOS E PASTAS
        // ====================================================================

        /**
         * Obtém o endpoint para mover itens
         */
        function getMoveEndpoint() {
            const configElement = document.querySelector('[data-workspace-config]');
            if (configElement) {
                return configElement.getAttribute('data-move-endpoint') || '/move-item/';
            }
            return '/move-item/';
        }

        /**
         * Obtém o CSRF token do Django
         */
        function getCsrfToken() {
            // Tenta obter do input hidden primeiro
            const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfInput) {
                return csrfInput.value;
            }
            
            // Tenta obter do cookie
            const name = 'csrftoken';
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        /**
         * Move um item (arquivo ou pasta) para uma pasta de destino
         */
        function moveItem(itemType, itemId, targetFolderId) {
            const endpoint = getMoveEndpoint();
            const formData = new FormData();
            formData.append('item_type', itemType);
            formData.append('item_id', itemId);
            if (targetFolderId) {
                formData.append('target_folder', targetFolderId);
            }

            // Obtém o CSRF token
            const csrfToken = getCsrfToken();
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken);
            }

            return fetch(endpoint, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                return data;
            });
        }

        /**
         * Remove todas as classes de highlight de drag
         */
        function clearDragHighlights() {
            // Remove highlight de pastas
            document.querySelectorAll('.selectable-item[data-kind="folder"]').forEach(item => {
                item.classList.remove('drag-over');
            });
            // Remove highlight de breadcrumbs
            document.querySelectorAll('.breadcrumb-drop').forEach(item => {
                item.classList.remove('drag-over');
            });
        }

        /**
         * Inicializa o sistema de drag and drop
         */
        function initializeDragAndDrop() {
            const draggableItems = document.querySelectorAll('.selectable-item[draggable="true"]');
            const dropTargets = document.querySelectorAll('.selectable-item[data-kind="folder"]');
            const breadcrumbTargets = document.querySelectorAll('.breadcrumb-drop');

            // Configura os itens arrastáveis
            draggableItems.forEach(item => {
                item.addEventListener('dragstart', function(e) {
                    const itemKind = item.getAttribute('data-kind');
                    const itemId = item.getAttribute('data-id');
                    
                    if (!itemKind || !itemId) {
                        e.preventDefault();
                        return;
                    }

                    // Marca que um drag está em andamento
                    isDragging = true;

                    // Armazena os dados do item sendo arrastado
                    e.dataTransfer.setData('text/plain', JSON.stringify({
                        kind: itemKind,
                        id: itemId
                    }));
                    
                    // Adiciona classe visual ao item sendo arrastado
                    item.classList.add('dragging');
                    
                    // Define o efeito de arrastar
                    e.dataTransfer.effectAllowed = 'move';
                });

                item.addEventListener('dragend', function(e) {
                    // Remove classe visual
                    item.classList.remove('dragging');
                    // Limpa highlights
                    clearDragHighlights();
                    // Reseta a flag após um pequeno delay para evitar conflito com click
                    setTimeout(() => {
                        isDragging = false;
                    }, 100);
                });
            });

            // Configura as pastas como destinos de drop
            dropTargets.forEach(target => {
                target.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Verifica se o item sendo arrastado não é a própria pasta
                    const draggedData = e.dataTransfer.getData('text/plain');
                    if (!draggedData) return;
                    
                    try {
                        const dragged = JSON.parse(draggedData);
                        const targetId = target.getAttribute('data-id');
                        
                        // Não permite arrastar uma pasta para ela mesma
                        if (dragged.kind === 'folder' && dragged.id === targetId) {
                            e.dataTransfer.dropEffect = 'none';
                            return;
                        }
                        
                        e.dataTransfer.dropEffect = 'move';
                        target.classList.add('drag-over');
                    } catch (err) {
                        // Ignora erros de parsing
                    }
                });

                target.addEventListener('dragleave', function(e) {
                    // Remove highlight apenas se realmente saiu do elemento
                    if (!target.contains(e.relatedTarget)) {
                        target.classList.remove('drag-over');
                    }
                });

                target.addEventListener('drop', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    target.classList.remove('drag-over');
                    
                    const draggedData = e.dataTransfer.getData('text/plain');
                    if (!draggedData) return;
                    
                    try {
                        const dragged = JSON.parse(draggedData);
                        const targetId = target.getAttribute('data-id');
                        
                        // Não permite arrastar uma pasta para ela mesma
                        if (dragged.kind === 'folder' && dragged.id === targetId) {
                            return;
                        }
                        
                        // Move o item
                        moveItem(dragged.kind, dragged.id, targetId)
                            .then(() => {
                                // Recarrega a página para atualizar a visualização
                                window.location.reload();
                            })
                            .catch(error => {
                                alert('Erro ao mover item: ' + error.message);
                            });
                    } catch (err) {
                        console.error('Erro ao processar drop:', err);
                    }
                });
            });

            // Configura os breadcrumbs como destinos de drop
            breadcrumbTargets.forEach(target => {
                target.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const draggedData = e.dataTransfer.getData('text/plain');
                    if (!draggedData) return;
                    
                    try {
                        const dragged = JSON.parse(draggedData);
                        const targetFolderId = target.getAttribute('data-folder-id');
                        
                        // Não permite arrastar uma pasta para ela mesma ou seus descendentes
                        // (isso será validado no backend, mas fazemos uma verificação básica aqui)
                        if (dragged.kind === 'folder' && dragged.id === targetFolderId) {
                            e.dataTransfer.dropEffect = 'none';
                            return;
                        }
                        
                        e.dataTransfer.dropEffect = 'move';
                        target.classList.add('drag-over');
                    } catch (err) {
                        // Ignora erros de parsing
                    }
                });

                target.addEventListener('dragleave', function(e) {
                    // Remove highlight apenas se realmente saiu do elemento
                    if (!target.contains(e.relatedTarget)) {
                        target.classList.remove('drag-over');
                    }
                });

                target.addEventListener('drop', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    target.classList.remove('drag-over');
                    
                    const draggedData = e.dataTransfer.getData('text/plain');
                    if (!draggedData) return;
                    
                    try {
                        const dragged = JSON.parse(draggedData);
                        const targetFolderId = target.getAttribute('data-folder-id');
                        
                        // Não permite arrastar uma pasta para ela mesma
                        if (dragged.kind === 'folder' && dragged.id === targetFolderId) {
                            return;
                        }
                        
                        // Move o item (targetFolderId pode ser vazio para raiz)
                        const folderId = targetFolderId && targetFolderId.trim() !== '' ? targetFolderId : null;
                        
                        moveItem(dragged.kind, dragged.id, folderId)
                            .then(() => {
                                // Recarrega a página para atualizar a visualização
                                window.location.reload();
                            })
                            .catch(error => {
                                alert('Erro ao mover item: ' + error.message);
                            });
                    } catch (err) {
                        console.error('Erro ao processar drop:', err);
                    }
                });
            });
        }

        // Inicializa o drag and drop
        initializeDragAndDrop();

    }); // DOMContentLoaded
})(); // IIFE
