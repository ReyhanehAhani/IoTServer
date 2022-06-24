/* globals Chart:false, feather:false */

const activateExportButton = (myChart) => {
  const pdf = document.getElementById('export-pdf');
  const image = document.getElementById('export-image');

  pdf.disabled = false;
  image.disabled = false;

  pdf.chart = myChart;
  image.chart = myChart;
}

const exportPDF = () => {
  const options = {
    orientation: 'landscape',
    unit: "mm",
    format: "a4",
    putOnlyUsedFonts: true,
    floatPrecision: "smart",
  };

  var doc = new jspdf.jsPDF(options);
  doc.text("Chart export", 10, 10);
  doc.addImage(event.target.chart.toBase64Image(), 'png', 10, 10, 210, 100);
  doc.save('chart.pdf');
}

const exportImage = () => {
  const anchor = document.createElement('a');
  anchor.download = 'chart.png';
  anchor.href = event.target.chart.toBase64Image();
  anchor.click();
}

const loadChart = () => {
  const pdf = document.getElementById('export-pdf');
  const image = document.getElementById('export-image');

  pdf.disabled = true;
  image.disabled = true;
  
  if(window.chart) {
    window.chart.destroy();
  }


  var labels = [];

  var ir_values = [];
  var light_values = [];
  var moisture_values = [];
  var temperature_values = [];

  fetch(`/api/fetch_recent_record?limit=${window.chartLimit}`)
    .then(res => res.json())
    .then(res => {
      var rows = res['data'];

      for (var i = 0; i < rows.length; i++) {
        labels.push(rows[i]['created']);
        ir_values.push(rows[i]['ir']);
        light_values.push(rows[i]['light']);
        moisture_values.push(rows[i]['moisture']);
        temperature_values.push(rows[i]['temperature']);
      }
      const data = {
        labels: labels,
        datasets: [
          {
            data: light_values,
            label: 'Light',
            borderColor: '#B0B97A',
          },
          {
            data: moisture_values,
            label: 'Moisture',
            borderColor: '#F49586',
          },
          {
            data: temperature_values,
            label: 'Temperature',
            borderColor: '#F7E188',
          }
        ]
      };

      const config = {
        type: 'line',
        data: data,
        options: {
          bezierCurve: false,
          animation: {
            onComplete: () => {
              activateExportButton(myChart)
            }
          },
          elements: {
            line: {
              backgroundColor: 'transparent',
              tension: 0
            }
          }
        }
      };
      const ctx = document.getElementById('myChart')

      const myChart = new Chart(
        ctx,
        config
      );
      window.chart = myChart;
      myChart.update();
    })
}

const setupChart = () => {
  loadChart();
  setInterval(loadChart, 1000 * 60 * 15);
}

const showMessage = (message, type) => {
  var errorContainer = document.getElementById('messageContainer');

  var errorElement = `
      <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
  `;

  errorContainer.innerHTML = errorElement;
}

const getUsernameAndPassword = () => {
  var username = document.getElementById('username');
  var password = document.getElementById('password');

  if (!username.value || !password.value) {
    return { 'result': 'error', 'reason': 'Empty username or password' }
  }

  return {
    'result': 'success',
    'username': username.value,
    'password': password.value
  }
}

const changeUsername = () => {
  var info = getUsernameAndPassword();

  if (info['result'] != 'success') {
    showMessage(info['reason'], 'danger');
    return false;
  }

  var data = `username=${info['username']}&password=${info['password']}`;

  fetch('/auth/change_username', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: data,
  })
    .then(res => {
      if (!res.ok) {
        throw res
      }
      return res
    })
    .then(res => {
      if (info['remember']) {
        saveUsername(info['username']);
      }
      showMessage(`Username successfully changed, redirecting...`, 'success');
      setTimeout(() => {
        window.location.replace('/auth/logout');
      }, 1000)
    })
    .catch(error => error.json().then(json => showMessage(json['reason'], 'danger')))


  return false;
}


const loadTable = (limit) => {
  const table = document.getElementById('table-body');
  table.innerHTML = '';

  const exportBtn = document.getElementById('export-csv');
  exportBtn.disabled = true;

  var url = `/api/fetch_recent_record?limit=${limit}`;

  fetch(url)
    .then(res => res.json())
    .then(json => {
      const row = json['data'];
      for (var i = 0; i < row.length; i++) {
        const rowHTML = `
        <tr>
          <th scope="row">${row[i]['id']}</th>
          <td>${row[i]['device_id']}</td>
          <td>${row[i]['created']}</td>
          <td>${row[i]['light']}</td>
          <td>${row[i]['moisture']}</td>
          <td>${row[i]['temperature']}</td>
        </tr>
      `;
        table.innerHTML += rowHTML;
      }

      exportBtn.disabled = false;
    })
}

const exportCSV = (name) => {
  var csv_data = [];

  var rows = document.getElementsByTagName('tr');
  for (var i = 0; i < rows.length; i++) {
    var cols = rows[i].querySelectorAll('td,th');
    var csv_row = [];

    for (var j = 0; j < cols.length; j++) {
      csv_row.push(cols[j].innerHTML);
    }

    csv_data.push(csv_row.join(","));
  }

  csv_data = csv_data.join('\n');
  CSVFile = new Blob([csv_data], { type: "text/csv" });

  var anchor = document.createElement('a');
  anchor.download = name;
  anchor.href = window.URL.createObjectURL(CSVFile);
  anchor.click();
}