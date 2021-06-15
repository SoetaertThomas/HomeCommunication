const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region ***  Callback-Visualisation - show___ ***
const showBureauActiviteit = function(jsonObject){
  //console.log(jsonObject.datum_meting)
  // datum_meting
  dag = jsonObject.datum_meting.substring(0,3)
  if (dag == "Mon"){
    dag = "Maandag"
  }
  else if(dag == "Tue"){
    dag = "Dinsdag"
  }
  else if(dag == "Wed"){
    dag = "Woensdag"
  }
  else if(dag == "Thu"){
    dag = "Donderdag"
  }
  else if(dag == "Fri"){
    dag = "Vrijdag"
  }
  else if(dag == "Sat"){
    dag = "Zaterdag"
  }
  else if(dag == "Sun"){
    dag = "Zondag"
  }
  document.querySelector('.js-bureau').innerHTML = dag + ", " + jsonObject.datum_meting.substring(17,22);
}

const showLuchtkwaliteit = function(jsonObject){
  luchtkwaliteit_span = ''
  //console.log(jsonObject[0].meetresultaat)
  
  
  if (jsonObject[0].meetresultaat < 800){
  luchtkwaliteit_span = "goed"
  }
  else if (jsonObject[0].meetresultaat < 1200 && jsonObject[0].meetresultaat > 800){
    luchtkwaliteit_span = "matig"
  }
  else if (jsonObject[0].meetresultaat > 1200){
    luchtkwaliteit_span = "slecht"
  }
  
  
  document.querySelector('.js-luchtkwaliteit').innerHTML = luchtkwaliteit_span;
}

const showOngelezenMelding = function(jsonObject){
  //console.log(jsonObject.tijd_afdrukken_melding );
  html = `<p class="o-layout__item">${jsonObject.bericht}</p>
                            <p class="o-layout__item">${jsonObject.tijd_melding.substring(17,22)}</p>`
  if (jsonObject.tijd_afdrukken_melding == null){
    document.querySelector('.js-ongelezen-melding').innerHTML = html;
  }
  else{
    document.querySelector('.js-ongelezen-melding').innerHTML = `<p class="o-layout__item">Geen ongelezen melding</p>
                            <p class="o-layout__item">--:--</p>`;
  }
}

const showKamer = function(jsonObject){
  //console.log(jsonObject)
  const naamcompententen = document.querySelectorAll('.js-naam');
  for(const naam of naamcompententen){
    naam.innerHTML = jsonObject.voornaam;
  }
};
////#endregion

//#region ***  Data Access - get___ ***
const getBureauActiviteit = function(){
  handleData(`http://${lanIP}/api/v1/bureau_activiteit`, showBureauActiviteit);
}

const getHistoriekLuchtkwaliteit = function () {
  handleData(`http://${lanIP}/api/v1/luchtkwaliteit`, showLuchtkwaliteit);
};

const getOngelezenMelding = function(){
  handleData(`http://${lanIP}/api/v1/melding`, showOngelezenMelding)
}

const getKamer = function(){
  handleData(`http://${lanIP}/api/v1/kamer`, showKamer)
}
//#endregion

const listenToUI = function () {

};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });
  socket.on("B2F_update_bureauactiviteit", function () {
    getBureauActiviteit();
  });
  socket.on("B2F_update_luchtkwaliteit", function () {
    getHistoriekLuchtkwaliteit();
  });
  socket.on("B2F_ongelezen_melding", function () {
    getOngelezenMelding();
    console.log('ongelezen');
  });
  socket.on("B2F_change_name", function () {
    getKamer();
    console.log("update kamer naam")
  });


};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
  getBureauActiviteit();
  getHistoriekLuchtkwaliteit();
  getOngelezenMelding();
  getKamer();
});
