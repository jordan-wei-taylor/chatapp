import { fetchRecords } from "/static/js/events.js";

let currentPage = 1;
const limit = 10;

// populate table when page loads
window.onload = () => { fetchRecords(currentPage, limit) }

// previous page update
document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchRecords(currentPage, limit)
    }
});

// next page update
document.getElementById('nextPage').addEventListener('click', () => {
    currentPage++;
    fetchRecords(currentPage, limit);
});