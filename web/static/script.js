function isEnter()
{
    const inputbox = document.getElementById("inputbox");
    if (inputbox.value != "") {
        if (event.keyCode == 13)
            SendMessage();
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
            if (event.keyCode == 191)
                inputbox.focus();
        }

        else if (isFocused)
        {
            if (event.keyCode == 27)
                inputbox.blur();
        }
    });
}

function SendMessage()
{
    var data = $('#inputbox').val();
    $.ajax({
        url: '/predict',
        type: 'POST',
        data: { 'input': data },
        success: function (response)
        {
            console.log(response);
        }
    });
    document.getElementById("inputbox").value = "";
}
