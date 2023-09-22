const progress = document.getElementById('progress');
const downLoad = document.getElementById('downLoad');
const processNumber = document.getElementById('processNumber');
const process = document.getElementById('process');
const cancelButton = document.getElementById('cancelButton');

cancelButton.addEventListener('click', function () {
    processNumber.classList.add('active');
    downLoad.classList.remove('active');
    progress.classList.remove('active');
});

function updateState(i) {
    var max = 578;
    var min = 0;

    i = i > 100 ? 100 : i < 0 ? 0 : i;

    var p = i / 100;
    var r = (1 - p) * min + p * max;
    var inv = max - r;

    processNumber.innerHTML = i + "%";
    process.style.strokeDashoffset = inv;
}



applyButton.addEventListener("click", () => {

    progress.classList.add('active');
    processNumber.classList.add('active');

    sendImage = canvas.toDataURL("image/png", 1.0);

    axios({
        method: "POST",
        url: "http://154.41.228.96:5000/pragmata_girl",
        data: { "image": sendImage },
    })
        .then(function (response) {
            // console.log(response.data);
            const eventSource = new EventSource('/pragmata_girl_state');
            eventSource.onmessage = function (event) {
                const message = event.data;
                updateState(message)

                if (message == "100") {
                    processNumber.classList.remove('active');
                    downLoad.classList.add('active');
                    eventSource.close();
                }
            };
            eventSource.onerror = function (error) {
                console.error('EventSource failed:', error);
                eventSource.close();
            };
        })
        .catch(function (error) {
            console.log(error.message);
        });
});









