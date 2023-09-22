class TextTool extends CanvasObject {
  constructor(canvas, id, inputText, textColorPicker1, textColorPicker2, checkBoxGradient, text_size_slider, fontSelector, text, size, font, color1, color2, isGradient, pos) {
    super(canvas, pos, new Vector2(100, 100), id)

    this.isAssigned = false;

    this.text = text || "TEXT"
    this.size = size || "72";
    this.font = font || "Arial";
    this.color1 = color1 || "red";
    this.color2 = color2 || "red";
    this.isGradient = isGradient;


    this.inputText = inputText;
    this.inputText.value = this.text;
    this.textColorPicker1 = textColorPicker1;
    this.textColorPicker2 = textColorPicker2;
    this.text_size_slider = text_size_slider;
    this.fontSelector = fontSelector;
    this.checkBoxGradient = checkBoxGradient;

    this.textMetrics_ = undefined;

    this.textPos = pos;
  }

  setState(active) {
    this.isActive = active;
  }

  setText(text) {
    this.text = text;
  }

  textMetrics() {
    this.updateData();
    return this.ctx.measureText(this.text);
  }

  onDraw(mousePos) {
    if (this.isRemoved) return;

    if (this.isSelected) {
      if (!this.isAssigned) {

        this.isAssigned = true;
        this.inputText.value = this.text;
        this.text_size_slider.value = this.size;
        this.textColorPicker1.value = this.color1;
        this.textColorPicker2.value = this.color2;
        this.fontSelector.value = this.font;
        this.checkBoxGradient.checked = this.isGradient;
      }

      this.text = this.inputText.value;
      this.size = this.text_size_slider.value;
      this.color1 = this.textColorPicker1.value;
      this.color2 = this.textColorPicker2.value;
      this.font = this.fontSelector.value;
      this.isGradient = this.checkBoxGradient.checked;

      this.scale.x = this.textMetrics().width + (this.scale.x * 0.03);
      this.scale.y = this.size * 1;

      this.textPos.x = this.position.x
      this.textPos.y = this.position.y + this.scale.y - (this.scale.y * 0.15);

      if (this.isGradient) {
        this.textColorPicker2.style.display = "block";
      }
      else {
        this.textColorPicker2.style.display = "none";
      }

      var html = document.getElementById("textSelect" + this.id);
      html.innerHTML = this.text;
    }

    const { x1, y1, x3, y3} = this.getBox();
    const gradient = this.ctx.createLinearGradient(x1, y1, x3, y3);
    gradient.addColorStop(0, this.color1);
    gradient.addColorStop(1, this.color2);

    this.ctx.font = `${this.size}px ${this.font}`;
    this.ctx.fillStyle = this.isGradient ? gradient : this.color1;

    this.ctx.fillText(this.text, this.textPos.x, this.textPos.y);
    this.drawBox(mousePos);
  }

  updateData() {
    this.ctx.font = `${this.size}px ${this.font}`;
    this.ctx.fillStyle = "#00000000";
    this.ctx.fillText(this.text, this.position.x, this.position.y);
  }
}