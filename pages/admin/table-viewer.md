# Table Viewer

<div class='table-container'>
    <table id="table">
        <thead>
            <tr>
                <th>User</th>
                <th>Treatment</th>
                <th>Option</th>
                <th>Completed</th>
                <th style="width:150px">Generated</th>
                <th style="width:150px">Last Active</th>
            </tr>
        </thead>
        <tbody id="table-rows">
            <!-- Data will be inserted here -->
        </tbody>
    </table>
<div class="pagination">
    <button id="prevPage" disabled>Previous</button>
    <span id="pageInfo"></span>
    <button id="nextPage">Next</button>
</div>
</div>

## To Do:

+ improve format via CSS
+ allow user to query the data
    + filter on treatment / option / completed
    + filter last active datetimes between {start} and {end}