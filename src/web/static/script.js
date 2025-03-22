hide_title = false;

function CheckForKeyboardShortcuts()
{
    document.addEventListener("keyup", function (e)
    {
        // focus on search box if `/`
        const inputbox = document.getElementById("inputbox");
        let isFocused = (document.activeElement === inputbox);
        if (!isFocused && e.key === "/")
            inputbox.focus();

        else if (isFocused && e.key === "Escape")
            inputbox.blur();
    });

    document.addEventListener("keydown", function (e)
    {
        // expand or collapse sidebar with "Alt + `"
        if (e.altKey && e.key === "`")
        {
            const sidebar = document.getElementById("sidebar");
            sidebar.style.display = (sidebar.style.display === "none") ? "block" : "none";
        }
    });
}

function ToggleOverview(element)
{
    var hr = element.querySelector("hr");
    hr.style.display = (hr.style.display === "none") ? "block" : "none";
    element.style.width = (hr.style.display === "none") ? "max-content" : "";
    element.style.height = (hr.style.display === "none") ? "max-content" : "800px";
    element.setAttribute("id", (hr.style.display === "none") ? "overview" : "overview-expanded");

    var p = element.querySelector("div");
    document.getElementById("results").style.display = (p.style.display === "none") ? "none" : "grid";
    document.getElementById("time-taken").style.display = (p.style.display === "none") ? "none" : "block";
    p.style.display = (p.style.display === "none") ? "block" : "none";

    var t = document.getElementById("title");
    t.style.display = (!hide_title && t.style.display === "none") ? "block" : "none";
}

function ToggleResults()
{
    var r = document.getElementById("results");
    r.style.display = (r.style.display === "none") ? "grid" : "none";
}

function PutQueryInSearch(element)
{
    document.getElementById("inputbox").value = element.innerHTML;
    document.getElementById("inputbox").focus();
}

function AdjustGridColumns()
{
    const results_container = document.getElementById("results");
    const result_blocks = document.querySelectorAll(".result-block");

    if (!result_blocks.length)
        return; // avoid errors if no results exist

    let total_length = 0;

    // calculate total length of all titles
    result_blocks.forEach(block => {
        const title = block.textContent.trim();
        total_length += title.length;
    });

    // calculate average length
    const avg_length = total_length / result_blocks.length;

    // set columns dynamically based on average title length
    let columns = 5; // default

    if (avg_length > 80)
        columns = 2; // fewer columns for long titles
    
    else if (avg_length > 70)
        columns = 3;
    
    else if (avg_length > 50)
        columns = 4;

    // apply new column count
    results_container.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
}

// function to perform search
function PerformSearch()
{
    const inputbox = document.getElementById("inputbox");
    const query = inputbox.value.trim();
    if (!query)
        return;

    // send to backend and get response
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("title").style.display = "none";
        hide_title = true;
        inputbox.value = "";
        UpdateResults(data);

        // update history only if it exists in the response
        if (data.history && Array.isArray(data.history))
        {
            const history_container = document.getElementById("history");
            history_container.innerHTML = '';
            
            data.history.forEach(item => {
                const p = document.createElement('p');
                p.textContent = item;
                p.onclick = function() { PutQueryInSearch(this); };
                history_container.appendChild(p);
            });
        }

        else
            console.error('History data is missing or not an array:', data);
    })
    .catch(error => { console.error('Error:', error); });
    return query;
}

// function to update search results
function UpdateResults(data)
{
    // update time taken
    document.getElementById("time-taken").textContent = data.time_taken;

    // update results
    const results_container = document.getElementById("results");
    results_container.innerHTML = '';

    data.results.forEach(result => {
        const a = document.createElement('a');
        a.className = 'result-block';
        a.href = result.URL;
        a.target = '_blank';
        a.textContent = result.Title;
        results_container.appendChild(a);
    });

    // adjust grid columns based on results
    AdjustGridColumns();
}

function DeleteHistory()
{
    // clear history in the backend by sending a special query
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: "<|del-history|>" }),
    })
    .then(response => response.json())
    .then(data => {
        // clear history in the UI
        document.getElementById("history").innerHTML = '';
        console.log('History cleared successfully');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function GetOverview(input)
{
    // send message to get AI overview
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: "<|overview|>" + input }),
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector("#overview div").innerHTML = marked.parse(data.overview);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
