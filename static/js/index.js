document.addEventListener("DOMContentLoaded", function() {
    const firstSelectElement = document.getElementById("select1");
    const secondSelectElement = document.getElementById("select2");
    const optionsForSelect2 = {
        0: ["Todos os campos", "Título", "Autor"],
        1: ["Todos os campos", "Título", "Autor", "Publicação", "Palavras-chave"],
        2: ["Todos os campos", "Título", "Autor", "Publicação", "Palavras-chave"],
        3: ["Todos os campos", "Título", "Autor", "Assunto"]
    };

    function updateOptionsForSelect2() {
        const selectedValue = firstSelectElement.value;
        secondSelectElement.innerHTML = "";
        optionsForSelect2[selectedValue].forEach((optionText, index) => {
            const option = document.createElement("option");
            option.value = index;
            option.text = optionText;
            secondSelectElement.appendChild(option);
        });
    }

    firstSelectElement.addEventListener("change", updateOptionsForSelect2);
    firstSelectElement.dispatchEvent(new Event("change"));

    const executeButton = document.querySelector('.home-button');
    let isSubmitting = false;

    executeButton.addEventListener('click', () => {
        if (isSubmitting) {
            return;
        }

        if (isFormAnswered()) {
            executeButton.setAttribute('disabled', 'disabled');
            executeButton.innerHTML = 'Processando...';
            isSubmitting = true;
            document.querySelector('.home-form').submit();
        } else {
            showCustomAlert('Por favor, insira os termos da consulta.');
        }
    });

    function isFormAnswered() {
        const searchTermsInput = document.querySelector('.home-textinput1[name="search_terms"]');
        return searchTermsInput.value !== "";
    }

    function showCustomAlert(message) {

    }
});
