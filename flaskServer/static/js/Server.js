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
// downLoad.classList.add('active');
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



// downLoad.addEventListener("click", () => {

//     axios({
//         method: "GET",
//         url: url+"/download_pragmata_girl",
//         data: {"file_name":"ss"}
//     })
//         .then(function (response) {

//             window.location.href = "/download_pragmata_girl";
//             // axios({
//             //     method: "GET",
//             //     url: url+"/delete_cookie",
//             //     data: {"file_name":"ss"}
//             // })
//             //     .then(function (response) {
//             //         console.log(response.data);
//             //     })
//             //     .catch(function (error) {
//             //         console.log(error.message);
//             //     });
  
//         })
//         .catch(function (error) {
//             console.log(error.message);
//         });
// });

applyButton.addEventListener("click", () => {

    progress.classList.add('active');
    processNumber.classList.add('active');

    sendImage = canvas.toDataURL("image/png", 1.0);
    const file_name = "momo.mp4"

    axios({
        method: "POST",
        url: url+"/pragmata_girl",
        data: { "image": sendImage ,"file_name":file_name},
    })
        .then(function (response) {
            console.log(response.data);

            if (response.data == "DONE") {
                processNumber.classList.remove('active');
                downLoad.classList.add('active');
            }
           
            // const eventSource = new EventSource('/pragmata_girl_state');
            // eventSource.onmessage = function (event) {
            //     const message = event.data;
            //     updateState(message)

            //     if (message == "100") {
            //         processNumber.classList.remove('active');
            //         downLoad.classList.add('active');
            //         eventSource.close();
            //     }
            // };
            // eventSource.onerror = function (error) {
            //     console.error('EventSource failed:', error);
            //     eventSource.close();
            // };
        })
        .catch(function (error) {
            console.log(error.message);
        });
});









