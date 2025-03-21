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

function ToggleOverview(element)
{
    var hr = element.querySelector("hr");
    hr.style.display = (hr.style.display === "none") ? "block" : "none";

    var p = element.querySelector("div");
    document.getElementById("results").style.display = (p.style.display === "none") ? "none" : "grid";
    p.style.display = (p.style.display === "none") ? "block" : "none";
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
        return; // Avoid errors if no results exist

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

    if (avg_length > 80)
        columns = 2; // Fewer columns for long titles
    
    else if (avg_length > 70)
        columns = 3;
    
    else if (avg_length > 50)
        columns = 4;

    // Apply new column count
    results_container.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
}

// Function to perform search
function PerformSearch()
{
    const inputbox = document.getElementById("inputbox");
    const query = inputbox.value.trim();
    if (!query)
        return;

    // Send to backend and get response
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
        UpdateResults(data);

        // Update history only if it exists in the response
        if (data.history && Array.isArray(data.history))
        {
            const historyContainer = document.getElementById("history");
            historyContainer.innerHTML = '';
            
            data.history.forEach(item => {
                const p = document.createElement('p');
                p.textContent = item;
                p.onclick = function() { PutQueryInSearch(this); };
                historyContainer.appendChild(p);
            });
        }

        else
            console.error('History data is missing or not an array:', data);
    })
    .catch(error => { console.error('Error:', error); });
    return query;
}

// Function to update search results
function UpdateResults(data)
{
    // Update time taken
    document.getElementById("time-taken").textContent = data.time_taken;

    // Update results
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = '';

    data.results.forEach(result => {
        const a = document.createElement('a');
        a.className = 'result-block';
        a.href = result.URL;
        a.target = '_blank';
        a.textContent = result.Title;
        resultsContainer.appendChild(a);
    });

    // Adjust grid columns based on results
    AdjustGridColumns();
}

function DeleteHistory()
{
    // Clear history in the backend by sending a special query
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: "<|del-history|>" }),
    })
    .then(response => response.json())
    .then(data => {
        // Clear history in the UI
        document.getElementById("history").innerHTML = '';
        console.log('History cleared successfully');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function GetOverview(input)
{
    // Send message to get AI overview
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: "<|overview|>" + input }),
    })
    .then(response => response.json())
    .then(data => {
        // Update overview
        const overviewDiv = document.querySelector("#overview div");
        overviewDiv.textContent = data.overview;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
