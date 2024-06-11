let dispositivo = [];
let totalRegistros = [];

function getData() {
  fetch("http://localhost:5000/monitoramento/grafico1")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      data.forEach((item) => {
        dispositivo.push(item.dispositivo);
        totalRegistros.push(item.TotalRegistros);
      });
      checkCharts();
    })
    .catch((error) => console.error("Erro ao obter dados:", error));
}

function checkCharts() {
  const radioButtons = document.querySelectorAll(
    'input[type="radio"][name="chart-type"]'
  );

  radioButtons.forEach((radioButton) => {
    radioButton.addEventListener("change", () => {
      displayChart(radioButton.value);
    });
  });
}

function displayChart(chartType) {
  document.querySelector(".charts").style.display = "block";

  switch (chartType) {
    case "pie":
      document.getElementById("chart_div").style.display = "block";
      document.getElementById("barchart_div").style.display = "none";
      document.getElementById("areachart_div").style.display = "none";
      drawChart("corechart", "pie");
      break;
    case "bar":
      document.getElementById("barchart_div").style.display = "block";
      document.getElementById("chart_div").style.display = "none";
      document.getElementById("areachart_div").style.display = "none";
      drawChart("bar", "bar");
      break;
    case "area":
      document.getElementById("areachart_div").style.display = "block";
      document.getElementById("chart_div").style.display = "none";
      document.getElementById("barchart_div").style.display = "none";
      drawChart("corechart", "area");
      break;
    default:
      console.log("No radio button is checked");
  }
}

function drawChart(package, chartType) {
  google.charts.load("current", { packages: [package] });
  google.charts.setOnLoadCallback(function () {
    let data = new google.visualization.DataTable();
    data.addColumn("string", "Dispositivo");
    data.addColumn("number", "Total de Registros");

    for (let i = 0; i < dispositivo.length; i++) {
      data.addRow([dispositivo[i], totalRegistros[i]]);
    }

    let options;
    let chart;

    if (chartType === "pie") {
      options = {
        title: "Registros de Dispositivos",
      };

      chart = new google.visualization.PieChart(
        document.getElementById("chart_div")
      );
    } else if (chartType === "bar") {
      options = {
        chart: {
          title: "Registros de Dispositivos",
        },
        bars: "horizontal",
      };

      chart = new google.charts.Bar(document.getElementById("barchart_div"));
    } else if (chartType === "area") {
      options = {
        title: "Registros de Dispositivos",
      };

      chart = new google.visualization.AreaChart(
        document.getElementById("areachart_div")
      );
    }

    chart.draw(data, options);
  });
}

getData();
