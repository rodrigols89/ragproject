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
(function() {
    'use strict';

    // Aguarda o carregamento completo do DOM
    document.addEventListener("DOMContentLoaded", function () {

        // ====================================================================
        // CONFIGURAÇÃO GLOBAL E TOKENS
        // ====================================================================

        // Obtém configurações do elemento HTML via data attributes
        const configElement = document.querySelector(
            '[data-workspace-config]'
        );
        const moveEndpoint = configElement?.dataset.moveEndpoint || '';

        // Obtém o token CSRF do formulário de deletar
        // Necessário para requisições POST seguras
        const deleteForm = document.getElementById("delete_form");
        const csrfToken = (
            deleteForm?.querySelector(
                "input[name='csrfmiddlewaretoken']"
            )?.value || ''
        );

        // ====================================================================
        // MODAL DE CRIAR PASTA
        // ====================================================================

        const modal = document.querySelector("#create_folder_modal");
        
        // Se não houver modal, não inicializa o restante
        if (!modal) return;

        // Elementos do modal
        const input = modal.querySelector("#nome_pasta");
        const serverError = document.getElementById("server-error");
        const openCreateBtn = document.querySelector(
            'button[command="show-modal"]' +
            '[commandfor="create_folder_modal"]'
        );
        const cancelButtons = modal.querySelectorAll(
            "button[command='close']"
        );

        /**
         * Limpa os campos do modal e esconde erros do servidor.
         */
        function clearModalFields() {
            if (input) input.value = "";
            if (serverError) {
                serverError.textContent = "";
                serverError.classList.add("hidden");
            }
        }

        /**
         * Foca e seleciona o input de nome da pasta.
         * Usa timeout para garantir que o foco ocorra após o modal abrir.
         */
        function focusCreateInput() {
            if (input) {
                setTimeout(() => {
                    input.focus();
                    input.select();
                }, 0);
            }
        }

        // Event listeners para botões de cancelar
        if (cancelButtons.length > 0) {
            cancelButtons.forEach(btn => {
                btn.addEventListener("click", function () {
                    clearModalFields();
                    modal.close();
                    // Redireciona se estiver na página de criar pasta
                    if (
                        window.location.pathname.startsWith(
                            "/create-folder"
                        )
                    ) {
                        window.location.href = "/workspace";
                    }
                });
            });
        }

        // Fecha o modal ao pressionar ESC
        modal.addEventListener("cancel", function () {
            clearModalFields();
            modal.close();
            if (
                window.location.pathname.startsWith("/create-folder")
            ) {
                window.location.href = "/workspace";
            }
        });

        // Abre o modal ao clicar no botão de criar
        if (openCreateBtn) {
            openCreateBtn.addEventListener("click", (event) => {
                event.preventDefault();
                modal.showModal();
                focusCreateInput();
            });
        }

        // Abre o modal automaticamente se configurado
        const autoOpenModal = document.querySelector(
            '#create_folder_modal[data-auto-open="true"]'
        );
        if (autoOpenModal) {
            modal.showModal();
            focusCreateInput();
        }

        // ====================================================================
        // SELEÇÃO E ARRASTE DE ITENS (DRAG AND DROP)
        // ====================================================================

        const selectableItems = document.querySelectorAll(
            ".selectable-item"
        );
        let selectedItem = null;
        let draggedItem = null;

        const deleteButton = document.getElementById("delete_selected");
        const renameButton = document.getElementById("rename_selected");

        /**
         * Limpa a seleção atual, removendo estilos e desabilitando botões.
         */
        function clearSelection() {
            selectableItems.forEach(el => {
                el.classList.remove("ring-2", "ring-blue-500");
            });
            selectedItem = null;
            if (deleteButton) deleteButton.disabled = true;
            if (renameButton) renameButton.disabled = true;
        }

        /**
         * Seleciona um item, removendo a seleção anterior.
         *
         * @param {HTMLElement} item - Elemento a ser selecionado
         */
        function selectItem(item) {
            selectableItems.forEach(el => {
                el.classList.remove("ring-2", "ring-blue-500");
            });
            item.classList.add("ring-2", "ring-blue-500");
            selectedItem = item;
            if (deleteButton) deleteButton.disabled = false;
            if (renameButton) renameButton.disabled = false;
        }

        /**
         * Move o item selecionado para uma pasta de destino.
         *
         * @param {string} targetFolderId - ID da pasta de destino
         */
        function moveSelectedToFolder(targetFolderId) {
            if (!selectedItem || !moveEndpoint || !csrfToken) return;

            // Prepara os dados da requisição
            const payload = new URLSearchParams({
                item_type: selectedItem.dataset.kind,
                item_id: selectedItem.dataset.id,
                target_folder: targetFolderId || "",
            });

            // Envia requisição para mover o item
            fetch(moveEndpoint, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
                body: payload,
            })
                .then(async response => {
                    const data = await response.json().catch(() => ({}));
                    if (!response.ok) {
                        const message = (
                            data.error ||
                            "Não foi possível mover o item."
                        );
                        alert(message);
                        return;
                    }
                    // Recarrega a página após mover com sucesso
                    window.location.reload();
                })
                .catch(() => {
                    alert("Erro inesperado ao mover item.");
                });
        }

        // Event listeners para cada item selecionável
        selectableItems.forEach(item => {
            // Seleciona item ao clicar
            item.addEventListener("click", (event) => {
                event.preventDefault();
                selectItem(item);
            });

            // Navega ao dar duplo clique
            item.addEventListener("dblclick", () => {
                const url = item.dataset.url;
                const target = item.dataset.target || "_self";
                if (!url) return;

                if (target === "_blank") {
                    window.open(url, "_blank");
                } else {
                    window.location.href = url;
                }
            });

            // Inicia o arraste
            item.addEventListener("dragstart", (event) => {
                draggedItem = item;
                event.dataTransfer.effectAllowed = "move";
                // Seleciona o item se ainda não estiver selecionado
                if (selectedItem !== item) {
                    selectItem(item);
                }
            });

            // Finaliza o arraste
            item.addEventListener("dragend", () => {
                draggedItem = null;
                // Remove destaque de todas as áreas de drop
                document.querySelectorAll(".drop-highlight").forEach(
                    el => {
                        el.classList.remove(
                            "ring-2",
                            "ring-green-500"
                        );
                    }
                );
            });

            // Se o item for uma pasta, permite receber outros itens
            if (item.dataset.kind === "folder") {
                // Destaca a pasta ao passar o mouse durante o arraste
                item.addEventListener("dragover", (event) => {
                    if (draggedItem && draggedItem !== item) {
                        event.preventDefault();
                        item.classList.add(
                            "ring-2",
                            "ring-green-500",
                            "drop-highlight"
                        );
                    }
                });

                // Remove destaque ao sair da pasta
                item.addEventListener("dragleave", () => {
                    item.classList.remove(
                        "ring-2",
                        "ring-green-500",
                        "drop-highlight"
                    );
                });

                // Move o item ao soltar na pasta
                item.addEventListener("drop", (event) => {
                    event.preventDefault();
                    item.classList.remove(
                        "ring-2",
                        "ring-green-500",
                        "drop-highlight"
                    );
                    if (!draggedItem || draggedItem === item) return;
                    moveSelectedToFolder(item.dataset.id);
                });
            }
        });

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

        // ====================================================================
        // BOTÃO DE RENOMEAR ITEM
        // ====================================================================

        const renameModal = document.getElementById("rename_modal");
        const renameForm = document.getElementById("rename_form");
        const renameInput = document.getElementById("rename_input");
        const renameCancel = document.getElementById("rename_cancel");

        // Abre o modal de renomear
        if (renameButton && renameModal && renameInput) {
            renameButton.addEventListener("click", (event) => {
                event.preventDefault();
                if (!selectedItem) return;
                
                // Obtém o nome atual do item (segundo span)
                const currentName = (
                    selectedItem.querySelector("span:nth-child(2)")
                        ?.textContent?.trim() || ""
                );
                renameInput.value = currentName;
                renameModal.showModal();
                renameInput.focus();
            });
        }

        // Fecha o modal de renomear
        if (renameCancel && renameModal) {
            renameCancel.addEventListener("click", () => {
                renameModal.close();
            });
        }

        // Submete o formulário de renomear
        if (renameForm) {
            renameForm.addEventListener("submit", (event) => {
                if (!selectedItem) {
                    event.preventDefault();
                    return;
                }
                
                const kind = selectedItem.dataset.kind;
                const id = selectedItem.dataset.id;
                if (!kind || !id) {
                    event.preventDefault();
                    return;
                }
                
                // Define a URL de ação baseada no tipo de item
                if (kind === "folder") {
                    renameForm.action = `/rename-folder/${id}/`;
                } else if (kind === "file") {
                    renameForm.action = `/rename-file/${id}/`;
                } else {
                    event.preventDefault();
                }
            });
        }

        // ====================================================================
        // EVENT LISTENERS GLOBAIS (TECLADO E CLIQUE)
        // ====================================================================

        // Limpa seleção ao pressionar ESC
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                clearSelection();
            }
        });

        // Limpa seleção ao clicar fora dos itens
        // Usa capture phase para garantir que funcione
        document.addEventListener("click", (event) => {
            const clickedItem = event.target.closest(
                ".selectable-item"
            );
            const preserve = event.target.closest(
                "[data-preserve-selection='true']"
            );
            if (!clickedItem && !preserve) {
                clearSelection();
            }
        }, true);

        // ====================================================================
        // BREADCRUMBS COM DRAG AND DROP
        // ====================================================================

        // Permite mover itens arrastando para os breadcrumbs
        const breadcrumbDrops = document.querySelectorAll(
            ".breadcrumb-drop"
        );

        breadcrumbDrops.forEach(crumb => {
            // Destaca o breadcrumb ao passar o mouse durante o arraste
            crumb.addEventListener("dragover", (event) => {
                if (!draggedItem) return;
                event.preventDefault();
                crumb.classList.add(
                    "ring-2",
                    "ring-green-500",
                    "drop-highlight"
                );
            });

            // Remove destaque ao sair do breadcrumb
            crumb.addEventListener("dragleave", () => {
                crumb.classList.remove(
                    "ring-2",
                    "ring-green-500",
                    "drop-highlight"
                );
            });

            // Move o item ao soltar no breadcrumb
            crumb.addEventListener("drop", (event) => {
                event.preventDefault();
                crumb.classList.remove(
                    "ring-2",
                    "ring-green-500",
                    "drop-highlight"
                );
                if (!draggedItem) return;
                moveSelectedToFolder(
                    crumb.dataset.folderId || null
                );
            });
        });
    });
})();
