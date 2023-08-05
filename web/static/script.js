function isEnter()
{
    const inputbox = document.getElementById("inputbox");
    if (inputbox.value != "") {
        if (keyCode == 13);
            // SendMessage();
    }
}

function Focus_on_inputbox()
{
    const inputbox = document.getElementById("inputbox");
    document.addEventListener("keyup", function (e)
    {
        let isFocused = (document.activeElement === inputbox);
        if (!isFocused)
        {
            if (e.keyCode == 191)
                inputbox.focus();
        }

        else if (isFocused)
        {
            if (e.keyCode == 27)
                inputbox.blur();
        }
    });
}

function CloseSearchPanel()
{
    // code here.
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
