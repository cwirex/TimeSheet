function deleteTask(taskId){
    fetch('/delete-task', {
        method: 'POST',
        body: JSON.stringify({taskId: taskId})
    }).then((response) => {
        window.location.href = "/"
    })
}