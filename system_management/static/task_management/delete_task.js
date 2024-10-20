/* global CSRF_TOKEN */

// Function to get CSRF token from the meta tag
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Set task_id when opening the modal
$('.delete-task').on('click', function() {
    var taskId = $(this).data('task-id'); 
    console.log('Setting task_id:', taskId);
    $('#delete_task_id').val(taskId); 
    console.log('delete_task_id:', taskId);
    $('#deleteTaskModal').modal('show');  // Show the delete confirmation modal
});

// Handle the delete task form submission
$('#delete-task-form').on('submit', function (e) {
    e.preventDefault();  // Prevent the default form submission

    // Gather the task ID from the form
    var task_id = $('#delete_task_id').val(); 
    console.log('taskId before submission:', task_id);  // Log it

    if (!task_id) {
        console.error('Task ID is missing');
        Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: 'Task ID is missing. Please provide a valid task ID.',
            confirmButtonText: 'OK'
        });
        return;  // Exit if task ID is not set
    }

    // Get CSRF token from the form
    var csrf_token = getCSRFToken();
    console.log('CSRF_TOKEN:', csrf_token);  // Log CSRF token

    if (!csrf_token) {
        console.error('CSRF token is missing');
        Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: 'CSRF token is missing. Please try again.',
            confirmButtonText: 'OK'
        });
        return;
    }

    // Perform AJAX request to delete the task
    $.ajax({
        url: DELETE_TASK,  // Ensure this URL matches your delete endpoint
        method: 'POST',  // Use POST for the form submission
        headers: {
            'X-CSRFToken': csrf_token,  // Include CSRF token for security
            'Content-Type': 'application/json'  // Set content type to JSON
        },
        data: JSON.stringify({ task_id: task_id }),  // Send task_id in the request body as JSON

        success: function (response) {
            console.log('Delete Task - success:', response);

            // SweetAlert Success
            Swal.fire({
                icon: 'success',
                title: 'Deleted!',
                text: 'The task has been deleted successfully.',
                confirmButtonText: 'OK'
            }).then(function() {
                // Optionally, reload or update task list on the page
                location.reload();  // Reload the page to reflect changes
            });
        },
        error: function (xhr, status, error) {
            console.error(`Delete Task - Error: ${status}, ${error}`);

            // SweetAlert Error
            Swal.fire({
                icon: 'error',
                title: 'Error!',
                text: 'Failed to delete task. Please try again.',
                confirmButtonText: 'OK'
            });
        }
    });
});
