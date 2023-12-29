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

function ChangeTitle()
{
    const results = document.getElementById("results");
    const title = document.getElementById("title");
    const time_taken = document.getElementById("time-taken");

    if (results.querySelectorAll("li").length > 0)
    {
        title.id = "results-title";
        time_taken.style.display = "block";
    }

    else
    {
        title.id = "title";
        time_taken.style.display = "none";
    }
}

function CheckForHistory()
{
    const results = document.getElementById("results");
    const no_search_history_found = document.getElementById("no-search-history-found");
    const clear_history_form = document.getElementById("clear-history-form");

    if (results.querySelectorAll("li").length > 0)
    {
        no_search_history_found.style.display = "none";
        clear_history_form.style.display = "block";
    }
    
    else
    {
        no_search_history_found.style.display = "block";
        clear_history_form.style.display = "none";
    }
}

function ToggleResultBlock(element)
{
    var result_desc = element.querySelector("#result-desc");
    if (result_desc.innerText.trim() != "")
        result_desc.style.display = (result_desc.style.display === "none") ? "block" : "none";
}
