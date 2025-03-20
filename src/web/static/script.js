function Focus_on_inputbox()
{
    var inputbox = document.getElementById("inputbox");
    document.addEventListener("keyup", function (e)
    {
        let isFocused = (document.activeElement === inputbox);
        if (!isFocused)
        {
            if (e.key === "/")
                inputbox.focus();
        }

        else if (isFocused)
        {
            if (e.key === "Escape")
                inputbox.blur();
        }
    });
}

function SendMessage()
{
    // JavaScript function to handle form submission
    const query = document.getElementById("inputbox").value;

    // Create an AJAX request
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/");
    xhr.setRequestHeader("Content-Type", "application/json");

    // Send the data to the Flask route
    const data = JSON.stringify({
        "query": query
    });
    xhr.send(data);
}

function DeleteHistory()
{
    const clear_history_form = document.getElementById("clear-history-form");

    clear_history_form.addEventListener("submit", function (e)
    {
        e.preventDefault();

        // Create an AJAX request
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/history");
        xhr.setRequestHeader("Content-Type", "application/json");

        // Send the data to the Flask route
        xhr.send();

        // Reload the page to reflect the changes
        location.reload();
    });
}

function ToggleOverview(element)
{
    var hr = element.querySelector("hr");
    hr.style.display = (hr.style.display === "none") ? "block" : "none";

    var p = element.querySelector("div");
    p.style.display = (p.style.display === "none") ? "block" : "none";
}

function PutQueryInSearch(element)
{
    document.getElementById("inputbox").value = element.innerHTML;
}

function AdjustGridColumns() {
    const results_container = document.getElementById("results");
    const result_blocks = document.querySelectorAll(".result-block");

    if (!result_blocks.length) return; // Avoid errors if no results exist

    let total_length = 0;

    // Calculate total length of all titles
    result_blocks.forEach(block => {
        const title = block.textContent.trim();
        total_length += title.length;
    });

    // Calculate average length
    const avg_length = total_length / result_blocks.length;

    // Set columns dynamically based on average title length
    let columns = 5; // Default

    if (avg_length > 50) {
        columns = 2; // Fewer columns for long titles
    } else if (avg_length > 30) {
        columns = 3;
    } else if (avg_length > 20) {
        columns = 4;
    }

    // Apply new column count
    results_container.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
}

// Run function when the page loads or results update
window.addEventListener("load", AdjustGridColumns);
