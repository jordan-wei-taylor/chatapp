<div class="admin-container" id="admin-container" style="display:none">
    <h1>Statistics / Dashboard</h1>
    <center>
    <p>Total No. of Users</p>
    <p>No. active within a week</p>
    <p>No completed module 0-7</p>
    </center>
    <h1>Users</h1>
    <div class="table-container">
        <table id="usersTable">
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
            <tbody id="usersTableRows">
                <!-- Data will be inserted here -->
            </tbody>
        </table>
    </div>
    <div class="pagination">
        <button id="prevPage" disabled>Previous</button>
        <span id="pageInfo"></span>
        <button id="nextPage">Next</button>
    </div>

    <div class="generate">
        <h1>Generate New Users</h1>
        <center>
        <form id="generate-users">
            <label for="textInput">Number of Users:</label>
            <input type="text" id="generate-number" name="textInput">
            <br><br>
            <label for="generate-treatment">Select a Treatment</label>
            <select name="Treatment" id= "generate-treatment">
                <option value=""></option>
            </select>
            <br><br>
            <label for="generate-treatment">Select an Option</label>
            <select name="Option" id="generate-option"></select>
            <br><br>
            <button type="button" id="generate-button">Submit</button>
        </form>
        </center>
    </div>
    
    <h1>Undo Recent Generation</h1>
    <h1>Deactivate User</h1>
    <h1>Reactivate User</h1>
    <br>
</div>