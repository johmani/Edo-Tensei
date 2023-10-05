const popup = document.getElementById('popup');
const downLoad = document.getElementById('downLoad');
const cancelButton = document.getElementById('cancelButton');
const processing_container = document.getElementById('processing-container');


var sessionNumber = undefined;

function getTime() {
    var currentDate = new Date();

    var year = currentDate.getFullYear();
    var month = currentDate.getMonth() + 1;
    var day = currentDate.getDate();
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var seconds = currentDate.getSeconds();
    var ms = currentDate.getMilliseconds();

    time = `${year}-${month}-${day}-${hours}-${minutes}-${seconds}-${ms}`

    return time
}


function generate() {
    cancelButton.classList.add('active');
    axios({
        method: "POST",
        url: url + "/pragmata_girl",
        data: { "sessionNumber": sessionNumber },
    })
        .then(function (response) {
            console.log(response.data.message);
            processing_container.classList.remove('active');
            downLoad.classList.add('active');
        })
        .catch(function (error) {
            console.log(error.message);
        });
}

applyButton.addEventListener("click", () => {

    sessionNumber = getTime()

    popup.classList.add('active');
    processing_container.classList.add('active');
    downLoad.classList.remove('active');
    cancelButton.classList.remove('active');

    sendImage = c.getImage();

    axios({
        method: "POST",
        url: url + "/submit_pragmata_girl",
        data: { "image": sendImage, "sessionNumber": sessionNumber },
    })
    .then(function (response) {
        console.log(response.data.message);
        generate()
    })
    .catch(function (error) {
        console.log(error);
    });
});

downLoad.addEventListener("click", () => {
    var a = document.createElement('a');
    a.href = "/download_pragmata_girl?sessionNumber=" + sessionNumber;
    a.setAttribute('download', '');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
});

cancelButton.addEventListener('click', function () {

    popup.classList.remove('active');

    axios({
        method: "POST",
        url: url + "/cancel_process",
        data: { "sessionNumber": sessionNumber }
    })
        .then(function (response) {
            console.log(response.data.message);
        })
        .catch(function (error) {
            console.log(error);
        });

});