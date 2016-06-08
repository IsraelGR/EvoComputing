'use strict';

var img = document.getElementById("scream");
var c = document.getElementById("myCanvas");
var c2 = document.getElementById("canvasChild");

var ctx = c.getContext("2d");
var ctx2 = c2.getContext("2d");

ctx.drawImage(img, 0, 0);

ctx2.fillStyle = "black";
ctx2.fillRect(0,0, img.width,img.height);

var randPosX = 0;
var randPosY = 0;
var randRadius = 0;

var pixelData = [0,0,0,0];
var pixelData2 = [0,0,0,0];
var pixelDataPert = [0,0,0,0];

var pertR;
var pertG;
var pertB;
var pertAlpha;

var aptitudChild;
var aptitudPert;

function evoImage(){
//while (true) {

  randPosX = Math.floor((Math.random() * img.width) + 1);
  randPosY = Math.floor((Math.random() * img.height) + 1);
  randRadius = Math.floor((Math.random() * 10) + 1);
  //alert(randPosX+","+randPosY);

  pixelData = ctx.getImageData(randPosX, randPosY, 1, 1).data;
  pixelData2 = ctx2.getImageData(randPosX, randPosY, 1, 1).data;
  // getImageData(positionX,positionY,) pixelData{ R, G, B, alpha};

  pertR = Math.floor((Math.random() * 511) - 255);
  pertG = Math.floor((Math.random() * 511) - 255);
  pertB = Math.floor((Math.random() * 511) - 255);
  pertAlpha = Math.random();

  pixelDataPert[0] = pixelData2[0] + pertR;
  pixelDataPert[1] = pixelData2[1] + pertG;
  pixelDataPert[2] = pixelData2[2] + pertB;
  pixelDataPert[3] = pixelData2[3] + pertAlpha;

  //+ Math.pow((pixelData[3]-pixelData2[3]), 2)
  //+ Math.pow((pixelData[3]-pixelDataPert[3]), 2)
  aptitudChild = Math.sqrt( Math.pow((pixelData[0]-pixelData2[0]), 2)  +   Math.pow((pixelData[1]-pixelData2[1]), 2)  +   Math.pow((pixelData[2]-pixelData2[2]), 2) + Math.pow((pixelData[3]-pixelData2[3]), 2));
  aptitudPert = Math.sqrt( Math.pow((pixelData[0]-pixelDataPert[0]), 2)  +   Math.pow((pixelData[1]-pixelDataPert[1]), 2)  +   Math.pow((pixelData[2]-pixelDataPert[2]), 2) + Math.pow((pixelData[3]-pixelDataPert[3]), 2));

  //console.log("aptitudChild: "+aptitudChild);
  //console.log("aptitudPert: "+aptitudPert);

  //,pixelDataPert[3]
  if(aptitudPert <= aptitudChild){
    draw(randPosX,randPosY,randRadius,pixelDataPert[0],pixelDataPert[1],pixelDataPert[2],pixelDataPert[3]);
  }

  setTimeout((function(){
    evoImage();
  }).bind(this),0);

}

$('canvas').mousemove(function() {
  var pixelData = ctx.getImageData(event.offsetX, event.offsetY, 1, 1).data;
  var pixelData = ctx.getImageData(event.offsetX, event.offsetY, 1, 1).data;

  $('#output').html('rgba: ' + pixelData[0] + ',' + pixelData[1] + ',' + pixelData[2] + ',' + pixelData[3]);
  $('#position').html('rgba: ' + pixelData2[0] + ',' + pixelData2[1] + ',' + pixelData2[2] + ',' + pixelData2[3]);
});

function draw(posX, posY, radius, r, g, b,alpha) {
  //ctx2.beginPath();
  //ctx2.arc(posX,posY,radius,0,2*Math.PI);

  ctx2.fillStyle = "rgba("+r+","+g+","+b+","+alpha+")";
  ctx2.fillRect(posX,posY, radius,radius);
  //ctx2.fill();
}

window.onload = evoImage;
