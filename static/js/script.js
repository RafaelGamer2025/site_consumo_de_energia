const ctx =
document.getElementById("grafico");

const chart =
new Chart(ctx, {

    type:"line",

    data:{

        labels:[],

        datasets:[{

            label:"Watts",

            data:[],

            borderColor:"#00ffee",

            borderWidth:3
        }]
    }
});

function adicionarAparelho(){

    const div =
    document.createElement("div");

    div.classList.add("item");

    div.innerHTML = `

    <input class="nome"
    placeholder="Nome do aparelho">

    <input class="watts"
    placeholder="Watts">

    <input class="horas"
    placeholder="Horas">

    <input class="quantidade"
    placeholder="Quantidade">

    `;

    document
    .getElementById("aparelhos")
    .appendChild(div);
}

async function monitor(){

    const r =
    await fetch("/monitor");

    const d =
    await r.json();

    document.getElementById(
    "cpu").innerHTML =
    "CPU " + d.cpu + "%";

    document.getElementById(
    "ram").innerHTML =
    "RAM " + d.ram + "%";

    document.getElementById(
    "watts").innerHTML =
    d.watts + "W";

    chart.data.labels.push(
    new Date().toLocaleTimeString());

    chart.data.datasets[0]
    .data.push(d.watts);

    if(chart.data.labels.length > 10){

        chart.data.labels.shift();

        chart.data.datasets[0]
        .data.shift();
    }

    chart.update();
}

setInterval(monitor,2000);

async function calcular(){

    const watts =
    document.getElementById(
    "wattsInput").value;

    const horas =
    document.getElementById(
    "horasInput").value;

    const dias =
    document.getElementById(
    "diasInput").value;

    const tarifa =
    document.getElementById(
    "tarifaInput").value;

    const quantidade =
    document.getElementById(
    "quantidadeInput").value;

    const nome =
    document.getElementById(
    "nomeInput").value;

    const casa =
    document.getElementById(
    "casaInput").value;

    const r =
    await fetch("/calcular",{

        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },

        body:JSON.stringify({

            nome,
            watts,
            horas,
            dias,
            tarifa,
            quantidade,
            casa
        })
    });

    const d =
    await r.json();

    document.getElementById(
    "resultado").innerHTML =

    `
    <h2>${d.nome}</h2>

    <h2>${d.kwh} kWh</h2>

    <h2>R$ ${d.preco}</h2>

    <h3>Casa ${d.casa}m²</h3>
    `;

    document.getElementById(
    "ideias").innerHTML =

    d.ideias.map(i =>
    `<p>${i}</p>`).join("");
}