function isEnter()
{
    const inputbox = document.getElementById("inputbox");
    inputbox.addEventListener("keyup", function (e)
    {
        if (inputbox.value != "") {
            if (e.key === "Enter");
                // SendMessage();
        }
    });
}

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

// function SendMessage()
// {
//     // JavaScript function to handle form submission
//     document.getElementById("search-bar").onsubmit = function(event)
//     {
//         event.preventDefault(); // Prevent default form submission
//         const query = document.getElementById("inputbox").value;
//         search(query);
//     };

//     function search(query)
//     {
//         console.log(query);
//     }

//     // document.getElementById("inputbox").value = "";
// }
