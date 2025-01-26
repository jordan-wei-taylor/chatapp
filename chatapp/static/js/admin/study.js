import { getStudy, updateStudy } from "/static/js/events.js"

const code = window.location.href.substring(window.location.href.lastIndexOf('/') + 1)

async function populateTable() {
    const tableBody = document.querySelector("#userTable tbody");
    const data = await getStudy(code)
    data.forEach((row, index) => {
        var line = document.createElement("tr");
        // Create editable cells for each field
        line.innerHTML = `
            <tr>
                <td contenteditable="true">${row[0]}</td>
                <td contenteditable="true">${row[1]}</td>
                <td contenteditable="true">${row[2]}</td>
                <td contenteditable="true">${row[3]}</td>
            </tr>
        `;
        tableBody.appendChild(line);
    });
}

function updateTable() {
    const rows = document.querySelectorAll("#userTable tbody tr");
    let data = [];
    
    rows.forEach(row => {
        const name = row.cells[0].textContent.trim(); // First column
        const email = row.cells[1].textContent.trim(); // Second column
        const gender = row.cells[2].textContent.trim(); // Third column
        const dob = row.cells[3].textContent.trim(); // Fourth column

        data.push([name, email, gender, dob ]);
    });
    updateStudy(code, data)
    alert(`Updated table ${code}`)
}

window.onload = async function() {
    await populateTable()
}   

// document.addEventListener("DOMContentLoaded", populateTable);

document.getElementById("updateButton").addEventListener('click', updateTable)