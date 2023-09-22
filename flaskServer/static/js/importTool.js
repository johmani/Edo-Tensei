class ImportTool extends CanvasObject{
    constructor(canvas, id, image, pos) {
        super(canvas,pos,new Vector2(image.width,image.height),id);
       
        this.image = image;
    }

    setState(active) {
        this.isActive = active;
    }

    onDraw(mousePos) {
        if (this.isRemoved) return;

        if (this.isSelected) {
            // var html = document.getElementById("textSelect" + this.id);
            // html.innerHTML = this.text;
        }

        this.ctx.drawImage(this.image, this.position.x, this.position.y, this.scale.x, this.scale.y);

        this.drawBox(mousePos);
    }

    drawBox(mousePos) {

        this.ctx.strokeStyle = this.boxColor;
        this.ctx.lineWidth = this.boxLineWidth;

        if (this.isSelected) {
            
            this.ctx.setLineDash([10, 5]);
            this.ctx.strokeRect(this.position.x, this.position.y, this.scale.x, this.scale.y);

            this.delete(mousePos);


            const { x3, y3 } = this.getBox();
            const radius = 10;

            ctx.beginPath();
            ctx.arc(x3, y3, radius, 0, 2 * Math.PI);
            ctx.fillStyle = "#FF0000";
            ctx.fill();
            ctx.closePath();

            const dis = mousePos.subtract(new Vector2(x3, y3)).magnitude();

            if (dis <= radius) {

                ctx.beginPath();
                ctx.arc(x3, y3, radius, 0, 2 * Math.PI);
                ctx.fillStyle = "#4f0c0c5d";
                ctx.fill();
                ctx.closePath();
            }
        }


        if (this.isDraging) {

            const { x1, y1, x2, y2, x3, y3, x4, y4 } = this.getBox();

            var r = 10;

            this.ctx.fillStyle = this.boxColor;
            this.ctx.fillRect(x1 - r / 2, y1 - r / 2, r, r);

            // this.ctx.fillStyle = this.boxColor;
            // this.ctx.fillRect(x2 - r / 2, y2 - r / 2, r, r);

            // this.ctx.fillStyle = this.boxColor;
            // this.ctx.fillRect(x3 - r / 2, y3 - r / 2, r, r);

            this.ctx.fillStyle = this.boxColor;
            this.ctx.fillRect(x4 - r / 2, y4 - r / 2, r, r);
        }
    }
}