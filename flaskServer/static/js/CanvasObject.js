class CanvasObject {
    constructor(canvas, position, scale, id) {

        this.id = id;

        this.isActive = false;
        this.isDraging = false;
        this.isDrawGizmos = true;
        this.cursorState = false;
        this.isSelected = true;
        this.isRemoved = false;
        this.isCliced = false;

        this.lastPoint = undefined;

        this.position = position || new Vector2(0, 0);
        this.scale = scale || new Vector2(100, 100);;

        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');

        this.boxColor = "black";
        this.boxLineWidth = 2;

        this.toolRadius = getComputedStyle(document.documentElement).getPropertyValue('--tool-radius');

        this.tempScale = new Vector2(scale.x, scale.y);
        this.isOnResize = false;
    }

    getBox() {
        var rectangle = {
            x1: this.position.x,
            y1: this.position.y,

            x2: this.position.x + this.scale.x,
            y2: this.position.y,

            x3: this.position.x + this.scale.x,
            y3: this.position.y + this.scale.y,

            x4: this.position.x,
            y4: this.position.y + this.scale.y,
        };
        return rectangle;
    }

    isInBox(point, margin = 0) {

        const { x1, y1, x2, y2, x3, y3, x4, y4 } = this.getBox();
        const { x, y } = point;

        const minX = Math.min(x1 - margin, x2 + margin, x3 + margin, x4 - margin);
        const maxX = Math.max(x1 - margin, x2 + margin, x3 + margin, x4 - margin);
        const minY = Math.min(y1 - margin, y2 - margin, y3 + margin, y4 + margin);
        const maxY = Math.max(y1 - margin, y2 - margin, y3 + margin, y4 + margin);

        if (x >= minX && x <= maxX && y >= minY && y <= maxY) {
            return true;
        } else {
            return false;
        }
    }


    drag(e) {
        if (this.isRemoved) return;
        if (!this.isActive) return;

        var pos = canvasFunctions.position(e, this.canvas);

        if (this.isSelected && this instanceof ImportTool) {
            this.reSize(pos);
        }

        if (this.isInBox(pos)) {

            if (!this.cursorState) {
                document.body.style.cursor = "move";
                this.cursorState = true;
            }

            if (this.isDraging) {

                var v = pos.subtract(this.lastPoint);
                this.position = this.position.add(v)

                this.lastPoint = pos;
            }

        }
        else {
            if (this.cursorState) {
                this.cursorState = false;
                document.body.style.cursor = "auto";
            }
        }
    }

    delete(mousePos) {

        const { x2, y2 } = this.getBox();
        const radius = this.toolRadius;

        // delete button
        {
            ctx.beginPath();
            ctx.arc(x2, y2, radius, 0, 2 * Math.PI);
            ctx.fillStyle = "#FFFFFF";
            ctx.fill();
            ctx.closePath();

            ctx.beginPath();
            ctx.arc(x2, y2, radius, 0, 2 * Math.PI);
            this.ctx.setLineDash([]);
            ctx.lineWidth = 1;
            ctx.fillStyle = "#000000";
            ctx.stroke();
            ctx.closePath();

            ctx.beginPath();
            ctx.moveTo(x2 - radius / 3, y2);
            ctx.lineTo(x2 + radius / 3, y2);
            ctx.lineWidth = radius / 4;
            ctx.strokeStyle = "red";
            ctx.stroke();
            ctx.closePath();
        }

        const dis = mousePos.subtract(new Vector2(x2, y2)).magnitude();
        if (dis <= radius) {

            // hover effect
            {
                ctx.beginPath();
                ctx.arc(x2, y2, radius, 0, 2 * Math.PI);
                ctx.fillStyle = "#4f0c0c5d";
                ctx.fill();
                ctx.closePath();
            }

            if (this.isCliced) {
                this.isRemoved = true;
                this.isSelected = false;
                document.getElementById("deletIcon" + this.id).parentNode.remove();
                document.body.style.cursor = 'auto';
            }
        }
    }

    reSize(mousePos) {

        const { x3, y3 } = this.getBox();
        const radius = 10;

        if (!this.isCliced) {
            this.tempScale = new Vector2(this.scale.x, this.scale.y);
        }

        const dis = mousePos.subtract(new Vector2(x3, y3)).magnitude();

        if (dis <= radius) {
            this.isOnResize = true;
        }

        if (this.isCliced && this.isOnResize) {
            var v = mousePos.subtract(this.lastPoint);
            this.scale = this.tempScale.add(v)
        }
    }

    onDrawGizmos(mousePos) {
        if (this.isRemoved) return;
        if (!this.isDrawGizmos) return;

        this.ctx.strokeStyle = this.boxColor;
        this.ctx.lineWidth = this.boxLineWidth;

        if (this.isSelected) {

            this.ctx.setLineDash([10, 5]);
            this.ctx.strokeRect(this.position.x, this.position.y, this.scale.x, this.scale.y);

            this.delete(mousePos);
        }


        if (this.isDraging) {

            const { x1, y1, x2, y2, x3, y3, x4, y4 } = this.getBox();

            var r = 10;

            this.ctx.fillStyle = this.boxColor;
            this.ctx.fillRect(x1 - r / 2, y1 - r / 2, r, r);

            // this.ctx.fillStyle = this.boxColor;
            // this.ctx.fillRect(x2 - r / 2, y2 - r / 2, r, r);

            this.ctx.fillStyle = this.boxColor;
            this.ctx.fillRect(x3 - r / 2, y3 - r / 2, r, r);

            this.ctx.fillStyle = this.boxColor;
            this.ctx.fillRect(x4 - r / 2, y4 - r / 2, r, r);
        }
    }

    onMouseDown(e) {
        if (this.isRemoved) return;
        this.isCliced = true;
        var pos = canvasFunctions.position(e, this.canvas);

        if (this.isInBox(pos, 15)) {
            this.isSelected = true;
            this.isAssigned = false;
        }
        else {
            this.isSelected = false;
        }

        if (!this.isActive) return;
        this.lastPoint = canvasFunctions.position(e, this.canvas);
        if (this.isInBox(pos)) {
            this.isDraging = true;
        };
    }

    onMousUp(e) {
        if (this.isRemoved) return;
        this.isDraging = false
        this.isCliced = false;
        this.isOnResize = false;
    }

    onMousOut(e) {
        if (this.isRemoved) return;
        this.isDraging = false
    }
}