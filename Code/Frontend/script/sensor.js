const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region ***  Callback-Visualisation - show___ ***
const showHistoriekDevices = function (jsonObject) {
  //console.log(jsonObject);
  html = '';
  table_header = `<tr class="c-row o-layout__item o-layout--gutter js-header">
          <td class="c-cell c-cell--label u-1-of-2">datum meting</td>
          <td class="c-cell c-cell--label u-1-of-2">meetresultaat</td>
        </tr>`
  for (const volgnummer of jsonObject) {
    if(volgnummer.meeteenheid){
      meeteenheid = volgnummer.meeteenheid;
    }
    else{
      meeteenheid = '';
    }
    html += `<tr class="c-row o-layout--gutter o-layout__item">
				<td class="c-cell u-1-of-2">${volgnummer.datum_meting.substring(4,22)}</td>
        <td class="c-cell u-1-of-2">${volgnummer.meetresultaat+ " " + meeteenheid}</td>
        </tr>`
  }

  const table = document.querySelector(`.js-table`);
  table.innerHTML = table_header + html;
}

const showHistoriekLuchtkwaliteit = function(jsonObject) {
    //console.log(jsonObject);
    let converted_labels = [];
    let converted_data = [];
    //console.log(jsonObject[0].meetresultaat)
    if (jsonObject[0].meetresultaat < 800){
          color = '#29CC94'
        }
        else if (jsonObject[0].meetresultaat < 1200 && jsonObject[0].meetresultaat > 800){
          color = '#CCB329'
        }
        else if (jsonObject[0].meetresultaat > 1200){
          color = '#CC4F29'
        }
    for(const data of jsonObject) {
        console.log(data.meetresultaat)
        // Dit wat op de x-as komt
        converted_labels.push(data.datum_meting);
        // Dit is wat op de y-as komt
        converted_data.push(data.meetresultaat)
        
    };
    drawChart1(converted_labels, converted_data, color);
};
////#endregion

//#region ***  Data Access - get___ ***
const getHistoriekDevices = function () {
  handleData(`http://${lanIP}/api/v1/devices`, showHistoriekDevices);
};

const getHistoriekLuchtkwaliteit = function () {
  handleData(`http://${lanIP}/api/v1/luchtkwaliteit`, showHistoriekLuchtkwaliteit);
};
//#endregion

const listenToUI = function () {

};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });
  socket.on("B2F_update_historieksensor", function () {
    getHistoriekDevices();
    getHistoriekLuchtkwaliteit();
    console.log("geupdate");
  });



};



const drawChart1 = function (labels, data, color) {
  var options = {
        series: [{
        name: 'PPM',
        data: data
      }],
        chart: {
        height: 350,
        type: 'area'
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth'
      },
      xaxis: {
        type: 'datetime',
        categories: labels
      },
      fill: {
        colors: [color]
      },
    };
  var chart = new ApexCharts(document.querySelector('.js-luchtkwaliteit'), options);

  chart.render();
}


document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
  getHistoriekDevices();
  getHistoriekLuchtkwaliteit();
});
