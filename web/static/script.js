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

function HideTitle()
{
    const results = document.getElementById("results");
    const title = document.getElementById("title");

    if (results.querySelectorAll("li").length > 0)
        title.style.display = "none";

    else
        title.style.display = "block";
}
