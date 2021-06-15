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

const showStatusMelding = function(jsonObject){
  //console.log(jsonObject);
  meetresultaat = jsonObject.meetresultaat;
  if (meetresultaat == 1){
    status_melding = "stil"
  }
  else if(meetresultaat == 2){
    status_melding = "trillen"
  }
  else if(meetresultaat == 3){
    status_melding = "luid"
  }
  //console.log(meetresultaat)
  const options = document.querySelectorAll('.js-option-melding');
  for(const option of options){
    //console.log(option.getAttribute("value"))
    if (option.getAttribute("value") == status_melding){
      option.setAttribute("selected", 'selected');
      //console.log("hallo")
    }else{
      option.removeAttribute("selected");
    }
  }
  listenToChangeStatusMelding();
}

const callbackAddBericht = function(){
  console.log("bericht verzonden");
  socket.emit('F2B_getBericht');
  window.location = "index.html";
}
//#region ***  Data Access - get___ ***
const getBureauActiviteit = function(){
  handleData(`http://${lanIP}/api/v1/bureau_activiteit`, showBureauActiviteit);
}

const getStatusMelding = function(){
  handleData(`http://${lanIP}/api/v1/status_melding`, showStatusMelding);
}
//#endregion

const listenToClickAddBericht = function () {  
  const button = document.querySelector('.js-verstuur');
  button.addEventListener("click", function () {
    console.log("melding maken");
    console.log(status);
    status_melding = document.querySelector(".js-select-status").value;
    if (status_melding == "stil"){
      status = 1;
    }
    else if(status_melding == "trillen"){
      status = 2;
    }
    else if(status_melding == "luid"){
      status = 3;
    }
    const jsonObject = {
      bericht: document.querySelector(".js-bericht").value,
      status_bericht: status
    };
    console.log(jsonObject);
    handleData(`http://${lanIP}/api/v1/melding`, callbackAddBericht, null, "POST", JSON.stringify(jsonObject));
  });
};

const listenToChangeStatusMelding = function(){
  select_list = document.querySelector('.js-select-status');
  select_list.addEventListener('change', function(){
    const options = document.querySelectorAll('.js-option-melding');
    for(const option of options){
      if (option.getAttribute("value") == select_list.value){
      option.setAttribute("selected", 'selected');
      //console.log("hallo")
    }else{
      option.removeAttribute("selected");
    }
    }
    console.log(select_list.value);
  });
}

const listenToUI = function () {

};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });
  socket.on("B2F_update_bureauactiviteit", function () {
    getBureauActiviteit();
  });
  socket.on("B2F_update_status_melding", function () {
    getStatusMelding();
  });
};

const listenToTxtArea = function(){
  const txtarea = document.querySelector('.js-bericht');
  const checkbox = document.querySelector('.js-checkbox');
  txtarea.addEventListener('change', function(){
    if(txtarea.value != ''){
      
      checkbox.setAttribute("style", "display:none");
    }
    else{
      checkbox.remove("style");
    }
  })
}

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
  listenToClickAddBericht();
  getBureauActiviteit();
  getStatusMelding();
  listenToTxtArea();

});
