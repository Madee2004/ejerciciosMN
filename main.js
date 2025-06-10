
function heun(f, t0, y0, h, n) {
  let t = t0;
  let y = y0;
  let result = "t\tHeun y(t)\n";
  let datos = [{ t: t, y: y }];
  result += `${t.toFixed(2)}\t${y.toFixed(6)}\n`;

  for (let i = 1; i < n; i++) {
    let k1 = f(t, y);
    let k2 = f(t + h, y + h * k1);
    y = y + (h / 2) * (k1 + k2);
    t += h;
    result += `${t.toFixed(2)}\t${y.toFixed(6)}\n`;
    datos.push({ t: t, y: y });
  }

  return { texto: result, datos: datos };
}

function rk4(f, t0, y0, h, n) {
  let t = t0;
  let y = y0;
  let result = "t\tRK4 y(t)\n";
  let datos = [{ t: t, y: y }];
  result += `${t.toFixed(2)}\t${y.toFixed(6)}\n`;

  for (let i = 1; i < n; i++) {
    let k1 = f(t, y);
    let k2 = f(t + h / 2, y + (h / 2) * k1);
    let k3 = f(t + h / 2, y + (h / 2) * k2);
    let k4 = f(t + h, y + h * k3);
    y = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4);
    t += h;
    result += `${t.toFixed(2)}\t${y.toFixed(6)}\n`;
    datos.push({ t: t, y: y });
  }

  return { texto: result, datos: datos };
}

let charts = {};

function graficar(heunData, rk4Data, problema) {
  const ctx = document.getElementById("grafico-" + problema).getContext("2d");
  const labels = heunData.map(p => p.t);
  const heunY = heunData.map(p => p.y);
  const rk4Y = rk4Data.map(p => p.y);

  if (charts[problema]) charts[problema].destroy();

  charts[problema] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Heun',
          data: heunY,
          borderColor: 'blue',
          fill: false
        },
        {
          label: 'Runge-Kutta 4',
          data: rk4Y,
          borderColor: 'green',
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { title: { display: true, text: 'Tiempo (t)' } },
        y: { title: { display: true, text: 'y(t)' } }
      }
    }
  });
}

function mostrarTablaComparativa(heunData, rk4Data, problema) {
  let tablaHTML = '<table class="table table-bordered table-striped"><thead><tr><th>t</th><th>Heun</th><th>RK4</th></tr></thead><tbody>';
  for (let i = 0; i < heunData.length; i++) {
    tablaHTML += `<tr><td>${heunData[i].t.toFixed(2)}</td><td>${heunData[i].y.toFixed(6)}</td><td>${rk4Data[i].y.toFixed(6)}</td></tr>`;
  }
  tablaHTML += '</tbody></table>';
  document.getElementById("tabla-" + problema).innerHTML = tablaHTML;
}

function resolverProblema(problema) {
  let f, t0, y0, h, tf, n;

  if (problema === 'tumor') {
    f = (t, y) => (0.8 * y) * (1 - (y / 60) ** 0.25);
    t0 = 0; tf = 30; y0 = 1; h = 0.1;
  } else if (problema === 'caida') {
    f = (t, v) => -9.81 + ((0.05 / 5) * v ** 2);
    t0 = 0; tf = 15; y0 = 0; h = 0.1;
  } else if (problema === 'poblacion') {
    f = (t, N) => 0.000095 * N * (5000 - N);
    t0 = 0; tf = 20; y0 = 100; h = 0.1;
  }

  n = Math.floor((tf - t0) / h) + 1;
  const heunRes = heun(f, t0, y0, h, n);
  const rk4Res = rk4(f, t0, y0, h, n);

  graficar(heunRes.datos, rk4Res.datos, problema);
  mostrarTablaComparativa(heunRes.datos, rk4Res.datos, problema);
}

