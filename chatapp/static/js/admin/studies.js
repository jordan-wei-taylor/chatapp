import { addStudy, getStudies, getTreatments } from "/static/js/events.js"

async function populateTreatments(){
    const treatments = await getTreatments()
    const dropdown = document.getElementById("studyDropdown");

    console.log(treatments)
    treatments.forEach(treatment => {
        const newTreatment = document.createElement("option");
        newTreatment.value = treatment;
        newTreatment.textContent = treatment;
        dropdown.appendChild(newTreatment);
    });
}

window.onload = async function() {
    await populateTreatments()
    await getStudyRecords()
}   

// new study
const Name = document.getElementById('study-name')
const Size = document.getElementById('study-size')

document.getElementById("newStudyForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent form from submitting normally
    await addEntryToTable();
});

async function addEntryToTable() {
    // Get form values
    const studyName = document.getElementById("studyName").value;
    const treatment = document.getElementById("studyDropdown").value;
    const treatmentSize = document.getElementById("treatmentSize").value;
    const controlSize = document.getElementById("controlSize").value;

    // Generate a unique code (for example, a random alphanumeric string)
    const code = generateRandomCode();

    // Get the table body element
    const tableBody = document.getElementById("studiesTableBody");

    // // Create a new row
    // const newRow = tableBody.insertRow();

    // // Add cells and insert form values
    // const codeCell = newRow.insertCell(0);
    // const nameCell = newRow.insertCell(1);
    // const treatmentCell = newRow.insertCell(2);
    // const treatmentSizeCell = newRow.insertCell(3);
    // const controlSizeCell = newRow.insertCell(4);
    // const populationSizecCell = newRow.insertCell(5);

    // codeCell.textContent = code;
    // nameCell.textContent = studyName;
    // treatmentCell.textContent = treatment;
    // treatmentSizeCell.textContent = treatmentSize;
    // controlSizeCell.textContent = controlSize;
    // populationSizecCell.textContent = 0

    addStudy([code, studyName, treatment, treatmentSize, controlSize])

    // Clear the form after submission
    document.getElementById("newStudyForm").reset();

    await getStudyRecords()

    return false; // Prevent default form submission
}

async function getStudyRecords() {
    const records = await getStudies()
    const tableBody = document.getElementById("studiesTableBody");
    tableBody.innerHTML = ""
    records.forEach(record => {
        var newRow = tableBody.insertRow()

        var codeCell = newRow.insertCell(0)
        var codeLink = document.createElement('a')
        codeLink.href = `study/${record[0]}`
        codeLink.textContent = record[0]
        codeCell.appendChild(codeLink)
        
        for (let i = 1; i < 6; i++) {
            newRow.insertCell(i).textContent = record[i]
        }
    })

}

function generateRandomCode() {
    // Generate a random letter for the first character
    const firstCharacter = String.fromCharCode(Math.floor(Math.random() * 26) + 65); // A-Z

    // Generate the remaining 9 characters as alphanumeric
    const remainingCharacters = Math.random().toString(36).substring(2, 12).toUpperCase();

    // Combine the first character with the remaining characters
    return firstCharacter + remainingCharacters; // Ensures first character is a letter
}

function filterTable() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const table = document.getElementById("studiesTableBody");
    const rows = table.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const codeCell = rows[i].getElementsByTagName("td")[0];
        const nameCell = rows[i].getElementsByTagName("td")[1];
        const code = codeCell.textContent || codeCell.innerText;
        const name = nameCell.textContent || nameCell.innerText;

        if (code.toLowerCase().indexOf(input) > -1 || name.toLowerCase().indexOf(input) > -1) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
}

document.getElementById("searchInput").addEventListener("input", filterTable);
// study table
