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

        /**
         * Remove seleção de todos os itens
         */
        function clearSelection() {
            items.forEach(item => {
                item.classList.remove("ring-2", "ring-blue-500");
            });
            selectedItem = null;
        }

        /**
         * Seleciona visualmente um item
         */
        function selectItem(item) {
            clearSelection();
            item.classList.add("ring-2", "ring-blue-500");
            selectedItem = item;
        }

        // Aplica eventos a cada item
        items.forEach(item => {

            // Clique simples → seleciona
            item.addEventListener("click", function (event) {
                event.preventDefault();
                selectItem(item);
            });

            // Duplo clique → navega
            item.addEventListener("dblclick", function () {
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
            if (!clickedItem) {
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
                
                // Fecha o modal usando a API nativa do HTML5
                modal.close();
            }
        });

    }); // DOMContentLoaded
})(); // IIFE
