/* global DELETE_TASK , CSRF_TOKEN */

$(document).ready(function () {
    console.log('Edit Task form JS loaded');

    // Set data from the task when the modal is shown
    $('#editTaskModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var taskId = button.data('task-id'); // Extract info from data-* attributes
        var title = button.data('task-title');
        var description = button.data('task-description');
        var dueDate = button.data('task-due-date');

        // Update the modal's content
        var modal = $(this);
        modal.find('#task_id').val(taskId);
        modal.find('#edit_title').val(title);
        modal.find('#edit_description').val(description);
        modal.find('#edit_due_date').val(dueDate);
    });

    $('#edit-task-form').on('submit', function (e) {
        e.preventDefault();  // Prevent the default form submission

        // Gather form data
        var taskId = $('#task_id').val();
        var title = $('#edit_title').val();
        var description = $('#edit_description').val();
        var due_date = $('#edit_due_date').val();

        // Log the data you're about to send
        console.log("Data being sent to the backend for editing:");
        console.log({
            task_id: taskId,
            title: title,
            description: description,
            due_date: due_date,
            'csrfmiddlewaretoken': CSRF_TOKEN
        });

        // Perform AJAX request to send the form data to the backend
        $.ajax({
            url: EDIT_TASK, // Update this URL to match your endpoint
            method: 'POST',
            data: {
                task_id: taskId,
                title: title,
                description: description,
                due_date: due_date,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            beforeSend: function(xhr, settings) {
                console.log("AJAX request object for editing task:");
                console.log(settings);  // This logs the settings of the AJAX request
            },
            success: function (response) {
                console.log('Edit Task - success:', response);

                // Optionally, close the modal
                $('#editTaskModal').modal('hide');

                // SweetAlert Success
                Swal.fire({
                    icon: 'success',
                    title: 'Task Updated',
                    text: 'The task has been updated successfully.',
                    confirmButtonText: 'OK'
                }).then(function() {
                    // Optionally, reload or update task list on the page
                    location.reload();
                });
            },
            error: function (xhr, status, error) {
                console.error(`Edit Task - Error: ${status}, ${error}`);

                // SweetAlert Error
                Swal.fire({
                    icon: 'error',
                    title: 'Error!',
                    text: 'Failed to update task. Please try again.',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});
