const canvas = document.getElementById("rain");

const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;

canvas.height = window.innerHeight;

const letras = "アイウエオ0123456789";

const fonte = 16;

const colunas =
canvas.width / fonte;

const gotas = [];

for(let i=0;i<colunas;i++){

gotas[i]=1;
}

function desenhar(){

ctx.fillStyle =
"rgba(0,0,0,0.05)";

ctx.fillRect(
0,
0,
canvas.width,
canvas.height);

ctx.fillStyle =
"#00ffee";

ctx.font =
fonte + "px monospace";

for(let i=0;i<gotas.length;i++){

const texto =
letras[
Math.floor(
Math.random()*letras.length)];

ctx.fillText(
texto,
i*fonte,
gotas[i]*fonte);

if(
gotas[i]*fonte >
canvas.height
&& Math.random()>0.975
){

gotas[i]=0;
}

gotas[i]++;
}
}

setInterval(desenhar,33);