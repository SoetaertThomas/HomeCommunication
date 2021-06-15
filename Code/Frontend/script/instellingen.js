const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region ***  Callback-Visualisation - show___ ***
const showKamer = function(jsonObject){
    //console.log(jsonObject);
    document.querySelector('.js-room-naam').innerHTML = jsonObject.voornaam;
}
//#region ***  Data Access - get___ ***
const getKamer = function(){
  handleData(`http://${lanIP}/api/v1/kamer`, showKamer)
}
//#endregion

const listenToClickWijzig = function () {  
  const btn = document.querySelector('.js-wijzig');
  btn.addEventListener('click', function(){
      console.log('verander voornaam');
      voornaam = document.querySelector('.js-textarea').value;
      socket.emit('F2B_change_name', {'voornaam': voornaam});
      window.location = "index.html";
  })
};

const listenToUI = function () {

};

constListenToAfsluiten = function(){
  const btn = document.querySelector('.js-afsluiten');
  btn.addEventListener('click', function(){
    console.log('print');
    socket.emit('F2B_afsluiten');
  });
  
}

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

};

document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    listenToUI();
    listenToSocket();
    listenToClickWijzig();
    getKamer();
    constListenToAfsluiten();
});
