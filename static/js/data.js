document.addEventListener("DOMContentLoaded", function () {
    const downloadButton = document.getElementById("downloadButton");
    const tokenElement = document.getElementById("token");
    const token = tokenElement.getAttribute("data-token");

    downloadButton.addEventListener("click", function() {
        // Redirect to the /download_data route when the button is clicked
        window.location.href = `/download_data/${token}`;
    });

    // Get references to all elements with the class "itemDatabase"
    const itemDatabases = document.querySelectorAll(".itemDatabase");

    // Function to show the appropriate set of spans based on itemDatabase value
    function showDatabaseSpans() {
        itemDatabases.forEach(function (itemDatabase) {
            const wosSpans = itemDatabase.parentElement.querySelector(".wosSpans");
            const elsSpans = itemDatabase.parentElement.querySelector(".elsSpans");
            const bdtdSpans = itemDatabase.parentElement.querySelector(".bdtdSpans");

            const databaseValue = itemDatabase.value;

            // Hide all sets of spans
            wosSpans.style.display = "none";
            elsSpans.style.display = "none";
            bdtdSpans.style.display = "none";

            // Show the set of spans corresponding to the databaseValue
            if (databaseValue == "WEB OF SCIENCE") {
                wosSpans.style.display = "block";
            } else if (databaseValue == "SCOPUS") {
                elsSpans.style.display = "block";
            } else {
                bdtdSpans.style.display = "block";
            }
        });
    }

    // Call the function initially
    showDatabaseSpans();

    function showDatabaseImg() {
        itemDatabases.forEach(function (itemDatabase) {
            const wosImg = itemDatabase.parentElement.querySelector(".wosImg");
            const elsImg = itemDatabase.parentElement.querySelector(".elsImg");
            const bdtdImg = itemDatabase.parentElement.querySelector(".bdtdImg");

            const databaseValue = itemDatabase.value;

            // Hide all images
            wosImg.style.display = "none";
            elsImg.style.display = "none";
            bdtdImg.style.display = "none";

            // Show the image corresponding to the databaseValue
            if (databaseValue == "WEB OF SCIENCE") {
                wosImg.style.display = "block";
            } else if (databaseValue == "SCOPUS") {
                elsImg.style.display = "block";
            } else {
                bdtdImg.style.display = "block";
            }
        });
    }

    // Call the function initially
    showDatabaseImg();
});
