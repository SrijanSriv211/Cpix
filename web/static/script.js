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
    localStorage.setItem("UserHistory")
}

function ChangeTitle()
{
    const results = document.getElementById("results");
    const title = document.getElementById("title");

    if (results.querySelectorAll("li").length > 0)
        title.id = "results-title";

    else
        title.id = "title";
}

function GetHistory()
{
    const results = document.getElementById("results");
    const no_search_history_found = document.getElementById("no-search-history-found");

    if (results.querySelectorAll("li").length > 0)
        no_search_history_found.style.display = "none";
    
    else
        no_search_history_found.style.display = "block";
}
