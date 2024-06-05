function getData() {
    fetch("http://localhost:8000/monitoramento/recentes")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const tableBody = document
          .getElementById("tabelaMonitoramento")
          .getElementsByTagName("tbody")[0];
        tableBody.innerHTML = ""; // Limpa o corpo da tabela
        data.forEach((item) => {
          const row = tableBody.insertRow();
          row.innerHTML = `
                        <td class="alignItensColumn">${item.Id}</td>
                        <td class="alignItensColumn">${item.Temperatura}</td>
                        <td class="alignItensColumn">${item.Umidade}</td>
                        <td class="alignItensColumn">${item.Dispositivo}</td>
                    `;
        });
      })
      .catch((error) => console.error("Erro ao obter dados:", error));
  }
  
  let pesquisaInput = document.getElementById("inputPesquisa");
  
  pesquisaInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      pesquisa = e.target.value;
      console.log(pesquisa);
      getDataByDispositivo();
    }
  });
  
  function getDataByDispositivo() {
    fetch(`http://localhost:8000/monitoramento/${pesquisa}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const tableBody = document
          .getElementById("tabelaMonitoramento")
          .getElementsByTagName("tbody")[0];
        tableBody.innerHTML = "";
        data.forEach((item) => {
          const row = tableBody.insertRow();
          row.innerHTML = `
                        <td class="alignItensColumn">${item.Id}</td>
                        <td class="alignItensColumn">${item.Temperatura}</td>
                        <td class="alignItensColumn">${item.Umidade}</td>
                        <td class="alignItensColumn">${item.Dispositivo}</td>
                    `;
        });
      })
      .catch((error) => console.error("Erro ao obter dados:", error));
  }
  
  pesquisaInput.addEventListener("input", function (e) {
    if (!e.target.value.trim()) {
      window.location.reload();
    }
  });
  
  getData();
  