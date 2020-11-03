
function onclickEditReport(id) {
    window.location.replace('http://127.0.0.1:8000/report/'+String(id)+'/')
}

function onclickDeleteReport(id) {
    window.location.replace('http://127.0.0.1:8000/report/'+String(id)+'/deletion')
}

function onclickAddReport() {
    window.location.replace('http://127.0.0.1:8000/report/')
}