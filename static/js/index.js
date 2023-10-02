document.addEventListener("DOMContentLoaded", function() {
    // Get references to the select elements and define options based on the first select
    const select1 = document.getElementById("select1");
    const select2 = document.getElementById("select2");
    const opcoesSelect2 = {
        0: ["Todos os campos", "Título", "Autor"],
        1: ["Todos os campos", "Título", "Autor", "Publicação", "Palavras-chave"],
        2: ["Todos os campos", "Título", "Autor", "Publicação", "Palavras-chave"],
        3: ["Todos os campos", "Título", "Autor", "Assunto"]
    };

    // Function to update options in the second select based on the first select
    function atualizarOpcoesSelect2() {
        const selectedValue = select1.value;
        select2.innerHTML = "";
        opcoesSelect2[selectedValue].forEach((opcao, index) => {
        const option = document.createElement("option");
        option.value = index;
        option.text = opcao;
        select2.appendChild(option);
    });
    }

    // Add a change event listener to the first select
    select1.addEventListener("change", atualizarOpcoesSelect2);
    // Trigger the 'change' event on page load to set initial options
    select1.dispatchEvent(new Event("change"));

    // Get a reference to the execute button
    const executeButton = document.querySelector('.home-button');

     // Flag to track if the form is being submitted
    let isSubmitting = false;

    // Add a click event listener to the execute button
    executeButton.addEventListener('click', () => {
        // Check if the form is already being submitted
        if (isSubmitting) {
            return;
        }

        // Check if the form is fully answered
        if (isFormAnswered()) {
            // Disable the button
            executeButton.setAttribute('disabled', 'disabled');
            executeButton.innerHTML = 'Processando...';

            // Set the form submission flag to true
            isSubmitting = true;

            // Submit the form
            document.querySelector('.home-form').submit();
        } else {
            // If the form is not fully answered, prevent the button click
            alert('Por favor, insira os termos da consulta.');
        }
    });

    // Function to check if the form is answered
    function isFormAnswered() {
        const searchTermsInput = document.querySelector('.home-textinput1[name="search_terms"]');

        if (
            searchTermsInput.value !== "" // Search terms are filled out
        ) {
            return true;
        } else {
            return false;
        }
}
});
