/*global CREATE_TASK, CSRF_TOKEN*/

$(document).ready(function () {
    console.log('executing');

    $('#create-task-form').on('submit', function (e) {
        console.log('js');

        e.preventDefault();  // Prevent form from submitting the default way

        // Gather form data
        var title = $('#create-title').val();
        var description = $('#create-description').val();
        var due_date = $('#create-due-date').val();

        // Log the data you're about to send
        console.log("Data being sent to the backend:");
        console.log({
            title: title,
            description: description,
            due_date: due_date,
            'csrfmiddlewaretoken': CSRF_TOKEN
        });

        // Perform AJAX request to send the form data to the backend
        $.ajax({
            url: CREATE_TASK,  // Replace with the appropriate backend URL
            method: 'POST',
            data: {
                title: title,
                description: description,
                due_date: due_date,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            beforeSend: function(xhr, settings) {
                console.log("AJAX request object:");
                console.log(settings);  // This logs the settings of the AJAX request
            },
            success: function (response) {
                console.log('in here');
                try {
                    // Handle success response
                    console.log('Task created successfully:', response);
                    // Optionally, close the modal
                    $('#exampleModal').modal('hide');
                    // Optionally, refresh or update the task list on the page
                } catch (e) {
                    console.error('Error handling success response:', e);
                }
            },
            error: function (xhr, status, error) {
                // Handle error response
                console.log('in error');
                console.error(`Error: ${status}, ${error}`);
                // Optionally display an error message to the user
                alert('Failed to create task. Please try again.');
            }
        });
    });
});

