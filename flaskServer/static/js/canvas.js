var ctx = canvas.getContext("2d");
const sourceImage = new Image();
sourceImage.src = "static/images/rec.png";

canvas.width = 1460;
canvas.height = 780;


sourceImage.onload = function () {
  ctx.drawImage(sourceImage, 0, 0, 1460, 780);
};

var scetchTool = new DrawingApp(canvas, colorPicker, pencil_size_slider);

var select = new SelectionTool(canvas, createText);
select.setState(false);

var items = [];


var fileInput = document.getElementById('fileInput');


importButton.addEventListener('click', function () {
  fileInput.click();
});


fileInput.addEventListener('change', function (event) {
  var file = event.target.files[0];

  if (file) {
    var reader = new FileReader();

    reader.onload = function (e) {
      var img = new Image();
      img.src = e.target.result;

      img.onload = function () {
        var importTool = new ImportTool(canvas, items.length, img, new Vector2(0, 0));
        importTool.setState(true);
        items = items.concat(importTool);


        const itemSelect = "textSelect" + importTool.id;
        const deletIcon = "deletIcon" + importTool.id;

        const htmlString = `
                <div class="textItem">
                  <a href="#" class="textSelect" id="${itemSelect}" onclick="selectText(${importTool.id})">${file.name}</a>
                  <a href="#" class="trash-icon" id="${deletIcon}" onclick="removeText(${importTool.id})"><i class="bx bx-trash icon"></i></a>
                </div>
              `;

        textContainer.innerHTML += htmlString;
      };
    };

    reader.readAsDataURL(file);
  }
});





function selectText(id) {
  items.forEach((text) => {
    text.isSelected = false;
  });

  items[id].isSelected = true;
  items[id].isAssigned = false;
  inputText.focus();
}

function removeText(id) {
  document.getElementById("deletIcon" + id).parentNode.remove();
  items[id].isRemoved = true;
  items[id].isSelected = false;
}

function createText() {

  var textPosX = Math.min(select.startPoint.x, select.endPoint.x);
  var textPosY = Math.min(select.startPoint.y, select.endPoint.y);
  var pos = new Vector2(textPosX, textPosY)

  var textSize = Math.abs(select.startPoint.y - select.endPoint.y);
  if (textSize < 30) return
  var myText = new TextTool(
    canvas,
    items.length,
    inputText,
    textColorPicker1,
    textColorPicker2,
    checkBoxGradient,
    text_size_slider,
    fontSelector,
    "TEXT",
    textSize,
    'Comic Sans MS',
    textColorPicker1.value,
    textColorPicker2.value,
    true,
    pos
  );


  myText.position = new Vector2(textPosX, textPosY)

  text_size_value.innerHTML = myText.size;

  myText.setState(true);
  items = items.concat(myText);
  // inputText.focus();


  const textSelect = "textSelect" + myText.id;
  const deletIcon = "deletIcon" + myText.id;
  const TEXT = myText.text;

  const htmlString = `
    <div class="textItem">
      <a href="#" class="textSelect" id="${textSelect}" onclick="selectText(${myText.id})">${TEXT}</a>
      <a href="#" class="trash-icon" id="${deletIcon}" onclick="removeText(${myText.id})"><i class="bx bx-trash icon"></i></a>
    </div>
  `;

  textContainer.innerHTML += htmlString;
}


class Canvas {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');

    this.canvas.addEventListener('pointerdown', this.onMouseDown.bind(this));
    this.canvas.addEventListener('pointermove', this.onMouseMove.bind(this));
    this.canvas.addEventListener('pointerup', this.onMouseUp.bind(this));
    this.canvas.addEventListener('pointerout', this.onMouseOut.bind(this));

    this.animationRequestId = null;

    this.mousePos = new Vector2(0, 0);
  }

  onStart() {

    {

    }
    this.onUpdate();
  }
  getImage(t){
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.drawImage(sourceImage, 0, 0, this.canvas.width, this.canvas.height);

    items.forEach((item) => {
      item.isDrawGizmos = false;
      item.onDraw(this.mousePos);
    });

    scetchTool.onDraw();
    const image = canvas.toDataURL("image/png", 1.0);
    items.forEach((item) => {
      item.isDrawGizmos = true;
    });

    return image;
  }

  onUpdate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.ctx.drawImage(sourceImage, 0, 0, this.canvas.width, this.canvas.height);

    {
      items.forEach((item) => {
        item.onDraw();
      });

      scetchTool.onDraw();
      select.onDrawGizmos();

      items.forEach((item) => {
        item.onDrawGizmos(this.mousePos);
      });
    }

    this.animationRequestId = requestAnimationFrame(this.onUpdate.bind(this));
  }

  onMouseDown(e) {

    select.onMouseDown(e);
    scetchTool.onMouseDown(e);

    items.forEach((item) => {
      item.onMouseDown(e);
    });

  }

  onMouseMove(e) {
    this.mousePos = canvasFunctions.position(e, this.canvas);

    select.onMousMove(e);
    items.forEach((item) => {
      item.drag(e);
    });
    scetchTool.onMouseMove(e);
  }

  onMouseUp(e) {
    select.onMousUp(e);
    items.forEach((item) => {
      item.onMousUp(e);
    });

    scetchTool.onMouseUp(e);

    var t = false;
    items.forEach((item) => {
      if (item.isSelected == true && item instanceof TextTool) {
        textProperties.classList.add('active');
        t = true;
      }
    });
    if (!t) {
      textProperties.classList.remove('active');
    }
  }

  onMouseOut(e) {
    select.onMousOut(e);
    items.forEach((item) => {
      item.onMousOut(e);
    });
    scetchTool.onMouseOut(e)
  }

  stopAnimation() {
    if (this.animationRequestId) {
      cancelAnimationFrame(this.animationRequestId);
    }
  }
}


c = new Canvas(canvas);
c.onStart();

