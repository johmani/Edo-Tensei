class Vector2 {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }

    add(v) {
        return new Vector2(this.x + v.x, this.y + v.y);
    }

    subtract(v) {
        return new Vector2(this.x - v.x, this.y - v.y);
    }

    multiply(s) {
        return new Vector2(this.x * s, this.y * s);
    }

    divide(s) {
        if (s !== 0) {
            return new Vector2(this.x / s, this.y / s);
        } else {
            console.error("Division by zero.");
            return new Vector2();
        }
    }

    dot(v) {
        return this.x * v.x + this.y * v.y;
    }

    magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    normalize() {
        const mag = this.magnitude();
        if (mag !== 0) {
            return this.divide(mag);
        } else {
            console.error("Normalization of a zero-length vector.");
            return new Vector2();
        }
    }

    toString() {
        return `(${this.x},${this.y})`;
    }
}