Number.prototype.map = function (in_min, in_max, out_min, out_max) {
  return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
function echo() {
		console.log("echo");
	}
function init() {
	var canvas = document.getElementById("myCanvas");
	var ctx = canvas.getContext("2d");
	var rect = canvas.getBoundingClientRect();
	var mdown = false;
	var pos;
	canvas.addEventListener("mousedown", inputStart, false);
	canvas.addEventListener("mouseup", inputEnd, false);
	canvas.addEventListener("mouseout", function(e) {
		mdown = false;
	}, false);
	canvas.addEventListener('mousemove', inputMove, false);
	canvas.addEventListener("touchstart", inputStart, false);
	canvas.addEventListener("touchend", inputEnd, false);
	canvas.addEventListener("touchmove", inputMove, false);

	function inputStart() {
		mdown = true;
	}
	function inputEnd() {
	inputMove({ clientX: Math.round(rect.width/2+rect.left), clientY: Math.round(rect.height/2+rect.top)});
		mdown = false;
	}
	function inputMove(e) {
	document.getElementById("console").innerHTML = "inputMove()";

		if(mdown) {
			if(e.touches && e.touches.length > 0) {
				pos = getMousePos(e.touches[0]);
			} else {
				pos = getMousePos(e);
			}
			centerPos(pos);
	//mapCenterPos(pos);
			toLeftRight(pos);
			printPos(pos);
			drawHandle(pos);
	event.preventDefault();
		}
	}
	function getMousePos(evt) {	
		var pos = {
		  x: Math.round(evt.clientX) - Math.round(rect.left),
		  y: Math.round(evt.clientY) - Math.round(rect.top)
		};
		pos.ox = pos.x;
		pos.oy = pos.y;
		return pos;
	}
	function centerPos(pos) {
		pos.cx = pos.x-rect.width/2;
		pos.cy = rect.height/2-pos.y;
	}
	function toLeftRight(pos) {
		pos.left = Math.min(pos.cy+pos.cx, 254);
		pos.right = Math.min(pos.cy-pos.cx, 254);
		return pos;
	}
	function mapCenterPos(pos) {
		pos.cx = Math.round(pos.cx.map(0, rect.width/2, 0, 254));
		pos.cy = 254 - Math.round(pos.cy.map(0, rect.height/2, 0, 254));
	}
	function printPos(pos) {
		document.getElementById("xy").innerHTML = "x:"+pos.x + "  y:" + pos.y;
		document.getElementById("cxcy").innerHTML = "cx:"+pos.cx + "  cy:" + pos.cy;
		document.getElementById("lr").innerHTML = "l:"+pos.left + "  r:" + pos.right;
	}
	function drawHandle(pos) {
		ctx.clearRect(0, 0, rect.width, rect.height);
		var s = 10;
		ctx.fillRect(pos.ox-s/2, pos.oy-s/2, s, s);
		
		ctx.beginPath();
		ctx.moveTo(rect.width/2, rect.height/2);
		ctx.lineTo(pos.ox, pos.oy);
		ctx.stroke();
	}

}