class DrawingApp {
    constructor(canvas, colorPicker, pencil_size_slider) {
        this.isActive = false;
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.colorPicker = colorPicker;
        this.pencil_size_slider = pencil_size_slider;
        this.isDrawing = false;
        this.Vector2 = undefined;
        this.clonedCanvas = canvas.cloneNode();
        this.clonedCtx = this.clonedCanvas.getContext("2d");
    }

    setState(active) {
        this.isActive = active;
    }

    onMouseDown(e) {
        if (!this.isActive) return;
        this.Vector2 = canvasFunctions.position(e,this.canvas)
        this.clonedCtx.beginPath();
        this.clonedCtx.moveTo(this.Vector2.x, this.Vector2.y);
        this.isDrawing = true;
    }

    onDraw() {
        this.ctx.drawImage(this.clonedCanvas, 0, 0, this.canvas.width, this.canvas.height, 0, 0, this.canvas.width, this.canvas.height);
    }

    onMouseMove(e) {
        if (!this.isActive) return;
        if (!this.isDrawing) return;

        var pos = canvasFunctions.position(e,this.canvas)

        this.clonedCtx.setLineDash([]);
        this.clonedCtx.lineTo(pos.x, pos.y);
        this.clonedCtx.strokeStyle = this.colorPicker.value;
        this.clonedCtx.lineWidth = this.pencil_size_slider.value;
        this.clonedCtx.lineJoin = 'round';
        this.clonedCtx.lineCap = 'round';
        this.clonedCtx.stroke();
    }

    onMouseUp(e) {
        this.isDrawing = false;
    }

    onMouseOut(e) {
        this.isDrawing = false;
    }
}

