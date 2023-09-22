class canvasFunctions {
    static position(event, canvas) {
        var x = event.offsetX * canvas.width / canvas.clientWidth | 0;
        var y = event.offsetY * canvas.height / canvas.clientHeight | 0;
        return new Vector2(x, y);
    }
}
