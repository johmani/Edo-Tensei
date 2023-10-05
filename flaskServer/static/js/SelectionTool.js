class SelectionTool {
    constructor(canvas,func) {

        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');

        this.isActive = false;
        this.isDrawing = false;

        this.startPoint = undefined;
        this.endPoint = new Vector2(0,0);

        this.boxColor = "black";
        this.boxLineWidth = 2;

        this.func = func;
    }

    isVaildArea(e){
        
        var pos = canvasFunctions.position(e,this.canvas);
       
        for (const text of items) {
            if (text.isInBox({ x: pos.x, y: pos.y })) {
               if(!text.isRemoved){
                // inputText.focus();
                return true;
               }
            }
        }
        return false;
    }

    setState(active) {
        this.isActive = active;
    }

    onMouseDown(e) {
        if (this.isVaildArea(e)) return;
        if (!this.isActive) return;

        this.startPoint = canvasFunctions.position(e,this.canvas);
        this.endPoint = canvasFunctions.position(e,this.canvas);
        this.isDrawing = true;
    }

    onMousMove(e) {
        if (this.isVaildArea(e)) return;
        this.endPoint = canvasFunctions.position(e,this.canvas);
    }

    onMousUp(e) {
        if (this.isVaildArea(e)) return;
        if (!this.isActive) return;

        this.isDrawing = false
        this.endPoint = canvasFunctions.position(e,this.canvas);

        // call when selection end
        this.func();
    }

    onMousOut(e) {
        this.isDrawing = false
    }

    onDrawGizmos(){
        if (!this.isDrawing) return;
 
        this.ctx.strokeStyle = this.boxColor;
        this.ctx.lineWidth = this.boxLineWidth;
        this.ctx.setLineDash([10, 5]); // [dashLength, gapLength]
        this.ctx.strokeRect(this.startPoint.x, this.startPoint.y, this.endPoint.x - this.startPoint.x, this.endPoint.y - this.startPoint.y);
    }
}