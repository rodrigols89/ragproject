/**
 * Workspace Home Page JavaScript
 * Gerencia funcionalidades da página principal do workspace:
 * - Modal de criação de pasta
 * - Seleção e arraste de itens
 * - Renomear e deletar itens
 * - Navegação por drag and drop
 */

(function() {
    'use strict';

    document.addEventListener("DOMContentLoaded", function () {

        // Configuração global - valores vindos do HTML via data attributes
        const configElement = document.querySelector('[data-workspace-config]');
        const moveEndpoint = configElement?.dataset.moveEndpoint || '';
        
        // Pega CSRF token do formulário
        const deleteForm = document.getElementById("delete_form");
        const csrfToken = deleteForm?.querySelector("input[name='csrfmiddlewaretoken']")?.value || '';

        // ========================================
        // MODAL DE CRIAR PASTA
        // ========================================
        const modal = document.querySelector("#create_folder_modal");
        if (!modal) return; // Se não houver modal, não inicializa

        const input = modal.querySelector("#nome_pasta");
        const serverError = document.getElementById("server-error");
        const openCreateBtn = document.querySelector('button[command="show-modal"][commandfor="create_folder_modal"]');
        const cancelButtons = modal.querySelectorAll("button[command='close']");

        function clearModalFields() {
            if (input) input.value = "";
            if (serverError) {
                serverError.textContent = "";
                serverError.classList.add("hidden");
            }
        }

        function focusCreateInput() {
            // timeout garante foco após showModal
            if (input) {
                setTimeout(() => {
                    input.focus();
                    input.select();
                }, 0);
            }
        }

        // Event listeners do modal de criar pasta
        if (cancelButtons.length > 0) {
            cancelButtons.forEach(btn => {
                btn.addEventListener("click", function () {
                    clearModalFields();
                    modal.close();
                    if (window.location.pathname.startsWith("/create-folder")) {
                        window.location.href = "/workspace";
                    }
                });
            });
        }

        modal.addEventListener("cancel", function () {
            clearModalFields();
            modal.close();
            if (window.location.pathname.startsWith("/create-folder")) {
                window.location.href = "/workspace";
            }
        });

        if (openCreateBtn) {
            openCreateBtn.addEventListener("click", (event) => {
                event.preventDefault();
                modal.showModal();
                focusCreateInput();
            });
        }

        // Auto-focus quando o modal é aberto automaticamente
        const autoOpenModal = document.querySelector('#create_folder_modal[data-auto-open="true"]');
        if (autoOpenModal) {
            modal.showModal();
            focusCreateInput();
        }

        // ========================================
        // SELEÇÃO E ARRASTE DE ITENS
        // ========================================
        const selectableItems = document.querySelectorAll(".selectable-item");
        let selectedItem = null;
        let draggedItem = null;

        const deleteButton = document.getElementById("delete_selected");
        const renameButton = document.getElementById("rename_selected");

        function clearSelection() {
            selectableItems.forEach(el => el.classList.remove("ring-2", "ring-blue-500"));
            selectedItem = null;
            if (deleteButton) deleteButton.disabled = true;
            if (renameButton) renameButton.disabled = true;
        }

        function selectItem(item) {
            selectableItems.forEach(el => el.classList.remove("ring-2", "ring-blue-500"));
            item.classList.add("ring-2", "ring-blue-500");
            selectedItem = item;
            if (deleteButton) deleteButton.disabled = false;
            if (renameButton) renameButton.disabled = false;
        }

        function moveSelectedToFolder(targetFolderId) {
            if (!selectedItem || !moveEndpoint || !csrfToken) return;
            
            const payload = new URLSearchParams({
                item_type: selectedItem.dataset.kind,
                item_id: selectedItem.dataset.id,
                target_folder: targetFolderId || "",
            });

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
                        const message = data.error || "Não foi possível mover o item.";
                        alert(message);
                        return;
                    }
                    window.location.reload();
                })
                .catch(() => alert("Erro inesperado ao mover item."));
        }

        // Event listeners dos itens selecionáveis
        selectableItems.forEach(item => {
            item.addEventListener("click", (event) => {
                event.preventDefault();
                selectItem(item);
            });

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

            item.addEventListener("dragstart", (event) => {
                draggedItem = item;
                event.dataTransfer.effectAllowed = "move";
                if (selectedItem !== item) {
                    selectItem(item);
                }
            });

            item.addEventListener("dragend", () => {
                draggedItem = null;
                document.querySelectorAll(".drop-highlight").forEach(el => 
                    el.classList.remove("ring-2", "ring-green-500")
                );
            });

            if (item.dataset.kind === "folder") {
                item.addEventListener("dragover", (event) => {
                    if (draggedItem && draggedItem !== item) {
                        event.preventDefault();
                        item.classList.add("ring-2", "ring-green-500", "drop-highlight");
                    }
                });

                item.addEventListener("dragleave", () => {
                    item.classList.remove("ring-2", "ring-green-500", "drop-highlight");
                });

                item.addEventListener("drop", (event) => {
                    event.preventDefault();
                    item.classList.remove("ring-2", "ring-green-500", "drop-highlight");
                    if (!draggedItem || draggedItem === item) return;
                    moveSelectedToFolder(item.dataset.id);
                });
            }
        });

        // ========================================
        // BOTÃO DE DELETAR
        // ========================================
        if (deleteButton && deleteForm) {
            deleteButton.addEventListener("click", (event) => {
                event.preventDefault();
                if (!selectedItem) return;

                const kind = selectedItem.dataset.kind;
                const id = selectedItem.dataset.id;
                if (!kind || !id) return;

                let action = "";
                if (kind === "folder") {
                    action = `/delete-folder/${id}/`;
                } else if (kind === "file") {
                    action = `/delete-file/${id}/`;
                }

                if (action) {
                    deleteForm.action = action;
                    deleteForm.submit();
                }
            });
        }

        // ========================================
        // BOTÃO DE RENOMEAR
        // ========================================
        const renameModal = document.getElementById("rename_modal");
        const renameForm = document.getElementById("rename_form");
        const renameInput = document.getElementById("rename_input");
        const renameCancel = document.getElementById("rename_cancel");

        if (renameButton && renameModal && renameInput) {
            renameButton.addEventListener("click", (event) => {
                event.preventDefault();
                if (!selectedItem) return;
                const currentName = selectedItem.querySelector("span:nth-child(2)")?.textContent?.trim() || "";
                renameInput.value = currentName;
                renameModal.showModal();
                renameInput.focus();
            });
        }

        if (renameCancel && renameModal) {
            renameCancel.addEventListener("click", () => {
                renameModal.close();
            });
        }

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
                if (kind === "folder") {
                    renameForm.action = `/rename-folder/${id}/`;
                } else if (kind === "file") {
                    renameForm.action = `/rename-file/${id}/`;
                } else {
                    event.preventDefault();
                }
            });
        }

        // ========================================
        // EVENT LISTENERS GLOBAIS (TECLADO E CLIQUE)
        // ========================================
        // Esc limpa a seleção
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                clearSelection();
            }
        });

        // Clique fora de itens limpa seleção
        document.addEventListener("click", (event) => {
            const clickedItem = event.target.closest(".selectable-item");
            const preserve = event.target.closest("[data-preserve-selection='true']");
            if (!clickedItem && !preserve) {
                clearSelection();
            }
        }, true);

        // ========================================
        // BREADCRUMBS COM DRAG AND DROP
        // ========================================
        const breadcrumbDrops = document.querySelectorAll(".breadcrumb-drop");

        breadcrumbDrops.forEach(crumb => {
            crumb.addEventListener("dragover", (event) => {
                if (!draggedItem) return;
                event.preventDefault();
                crumb.classList.add("ring-2", "ring-green-500", "drop-highlight");
            });

            crumb.addEventListener("dragleave", () => {
                crumb.classList.remove("ring-2", "ring-green-500", "drop-highlight");
            });

            crumb.addEventListener("drop", (event) => {
                event.preventDefault();
                crumb.classList.remove("ring-2", "ring-green-500", "drop-highlight");
                if (!draggedItem) return;
                moveSelectedToFolder(crumb.dataset.folderId || null);
            });
        });
    });
})();
