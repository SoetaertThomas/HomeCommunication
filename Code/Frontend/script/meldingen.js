const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region ***  Callback-Visualisation - show___ ***
const showHistoriekMeldingen = function (jsonObject) {
  //console.log(jsonObject);
  html = '';
  table_header = `<tr class="c-row js-header">
          <td class="c-cell c-cell--label">tijd</td>
          <td class="c-cell c-cell--label">afdrukken</td>
          <td class="c-cell c-cell--label">bericht</td>
        </tr>`

  for (const volgnummer of jsonObject) {
    // if(volgnummer.status_melding == '1'){
    //   status_melding = "Stil"
    // }
    // else if(volgnummer.status_melding == '2'){
    //   status_melding = "Trillen"
    // }
    // else if (volgnummer.status_melding == '3'){
    //   status_melding = "Luid"
    // }
    html += `<tr class="c-row">
				<td class="c-cell">${volgnummer.tijd_melding.substring(4,22)}</td>
        <td class="c-cell">${volgnummer.reactie_tijd} sec</td>
        <td class="c-cell">${volgnummer.bericht}</td>
        </tr>`
  }

  const table = document.querySelector(`.js-table`);
  table.innerHTML = table_header + html;
}
////#endregion

//#region ***  Data Access - get___ ***
const getHistoriekMeldingen = function () {
  handleData(`http://${lanIP}/api/v1/meldingen`, showHistoriekMeldingen);
};
//#endregion

const listenToUI = function () {

};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

  socket.on("B2F_update_historiekmelding", function () {
    getHistoriekMeldingen();
  });

};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
  getHistoriekMeldingen();
});
