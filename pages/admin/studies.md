# Studies

## New Study

<!-- Section to input new study -->
<div class="input-section">
    <input type="text" id="study-name" placeholder="Study Name" />
    <select id="generate-treatment"><option disabled selected>Select a Treatment</option></select>
    <input type="number" id="study-size" placeholder="Study Size" />
    <button id="add-study">Add Study</button>
</div>

<hr>

## Existing Studies

<div class="input-section">
    Search: <input type="text" id="study-name" placeholder="Study Name" />
</div>

<!-- Table for displaying studies -->
<table class="study-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Size</th>
        </tr>
    </thead>
    <tbody id="study-table-body">
        <!-- Rows will be populated dynamically -->
    </tbody>
</table>

<!-- Pagination Controls -->
<div class="pagination">
    <button id="prev-page">Previous</button>
    <span id="page-info">Page 1 of 1</span>
    <button id="next-page">Next</button>
</div>