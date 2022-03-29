var SERVER_IP = "localhost"
var SERVER_PORT = 7091

function onOperationSelected(){
  var operationSelect = document.getElementById("operationSelect").value
  var divServiceNameSelect = document.getElementById("divServiceNameSelect");
  var divJsonTextArea = document.getElementById("divJsonTextArea");
  var divServiceNameInput = document.getElementById("divServiceNameInput");
  var searchButton = document.getElementById("searchButton");
  var jsonTextArea = document.getElementById("jsonTextArea");
  var serviceNameInput = document.getElementById("serviceNameInput");
  var servicePathTitleLabel = document.getElementById("servicePathTitleLabel");
  var servicePathLabel = document.getElementById('servicePathLabel');
  var servicePathLabelSpan = document.getElementById("servicePathLabelSpan");
  var copyImage = document.getElementById("copyImage");
  if (operationSelect === "OPR_SELECT") {
    divServiceNameSelect.style.display = "inline-block";
    divJsonTextArea.style.display = "inline-block";
    divServiceNameInput.style.display = "none";
    copyImage.style.display = "inline-block";
    searchButton.innerText = "Select";
    searchButton.style.backgroundColor = "#74ac1e";
    jsonTextArea.value = "";
    fillServiceNames()
  } else if (operationSelect === "OPR_UPDATE"){
    divServiceNameSelect.style.display = "inline-block";
    divJsonTextArea.style.display = "inline-block";
    divServiceNameInput.style.display = "none";
    copyImage.style.display = "none";
    searchButton.innerText = "Update";
    searchButton.style.backgroundColor = "#74ac1e";
    jsonTextArea.value = ""
    fillServiceNames();
    getJSONForUpdate();
  } else if (operationSelect === "OPR_INSERT"){
    divServiceNameSelect.style.display = "none";
    divJsonTextArea.style.display = "inline-block";
    divServiceNameInput.style.display = "inline-block";
    copyImage.style.display = "none";
    searchButton.innerText = "Add";
    searchButton.style.backgroundColor = "#74ac1e";
    jsonTextArea.value = "";
    serviceNameInput.value = "";
    servicePathTitleLabel.innerText = "Paste JSON Text below";
    servicePathLabel.innerText = "";
  } else if (operationSelect === "OPR_DELETE") {
    fillServiceNames();
    divServiceNameSelect.style.display = "inline-block";
    divJsonTextArea.style.display = "none";
    divServiceNameInput.style.display = "none";
    copyImage.style.display = "none";
    searchButton.innerText = "Delete";
    searchButton.style.backgroundColor = "#FF0000";
    jsonTextArea.value = "";
    servicePathTitleLabel.innerText = "";
    servicePathLabel.innerText = "";
  }
}

function onServiceNameSelected(){
    var operationSelect = document.getElementById("operationSelect").value
    if (operationSelect === "OPR_UPDATE"){
        getJSONForUpdate();
    }
    updateServicePathLabel();
}

function fillServiceNames() {
    var request = createRequest("POST", "http://".concat(SERVER_IP).concat(":").concat(SERVER_PORT).concat("/serviceNames"));
    if (!request) {
        console.log("Cannot make request!");
        return;
    }

    request.onload = function () {
        if (request.status === 200) {
            var jsonResponse = JSON.parse(request.responseText);
            var serviceNameSelect = document.getElementById("serviceNameSelect");

            while (serviceNameSelect.options.length > 0) {
                serviceNameSelect.remove(0);
            }
            for (var i = 0; i < jsonResponse.length; i++){
                var option = document.createElement("option");
                option.text = jsonResponse[i].serviceNameSelect;
                serviceNameSelect.add(option);
            }
            updateServicePathLabel();
        }
    }
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send("");
}

function updateServicePathLabel(){
    var servicePathTitleLabel = document.getElementById("servicePathTitleLabel");
    var servicePathLabel = document.getElementById('servicePathLabel');
    var serviceNameSelect = document.getElementById("serviceNameSelect");
    if (serviceNameSelect.options.length > 0){
        var serviceNameSelectedValue = serviceNameSelect.options[serviceNameSelect.selectedIndex].value;
        servicePathTitleLabel.innerText = "Service Path (Click on Path to Copy): ";
        servicePathLabel.innerText = "http://".concat(SERVER_IP).concat(":").concat(SERVER_PORT).concat("/").concat(serviceNameSelectedValue);
    }else {
        servicePathTitleLabel.innerText = "Service Path: ";
        servicePathLabel.innerText = "";
    }
}

function getJSONForUpdate(){
    var request = createRequest("POST", "http://".concat(SERVER_IP).concat(":").concat(SERVER_PORT).concat("/OPR_SELECT"));
    if (!request) {
        console.log("Cannot make request!");
        return;
    }
    var requestObject
    var serviceNameSelect = document.getElementById("serviceNameSelect").value;
        if (serviceNameSelect){
            requestObject = { serviceNameSelect: serviceNameSelect };
        }

    if (requestObject){
        var jsonRequest = JSON.stringify(requestObject);
        request.onload = function () {
            if (request.status == 200) {
                var jsonTextArea = document.getElementById("jsonTextArea");
                jsonTextArea.value = request.responseText;
            }
        }
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(jsonRequest);
    }
}

function onRequest() {
    var operationSelect = document.getElementById("operationSelect").value
    var request = createRequest("POST", "http://".concat(SERVER_IP).concat(":").concat(SERVER_PORT).concat("/").concat(operationSelect));
    if (!request) {
        console.log("Cannot make request!");
        return;
    }
    var requestObject
    if (operationSelect === "OPR_SELECT") {
        var serviceNameSelect = document.getElementById("serviceNameSelect").value
        if (serviceNameSelect){
            requestObject = { serviceNameSelect: serviceNameSelect };
        }else {
            alert("There is nothing to select.")
        }
    } else if (operationSelect === "OPR_UPDATE") {
        var serviceNameSelect = document.getElementById("serviceNameSelect").value
        var jsonTextArea = document.getElementById("jsonTextArea").value;
        if (serviceNameSelect){
            if (jsonTextArea){
                requestObject = { serviceNameSelect: serviceNameSelect,
                                   jsonTextArea: jsonTextArea };
            }else {
                alert("Enter JSON Text");
            }
        }else {
            alert("There is nothing to update.");
        }
    } else if (operationSelect === "OPR_INSERT"){
      var serviceNameInput = document.getElementById("serviceNameInput").value;
      var jsonTextArea = document.getElementById("jsonTextArea").value;
      if (serviceNameInput){
          if (jsonTextArea){
            requestObject = {serviceNameInput: serviceNameInput,
                            jsonTextArea: jsonTextArea};
          }else {
            alert("Enter JSON Text")
          }
      } else {
        alert("Enter Service Name")
      }
    } else if (operationSelect === "OPR_DELETE") {
      var serviceNameSelect = document.getElementById("serviceNameSelect").value;
      if (serviceNameSelect){
          var confirmText = "You are deleting ".concat(serviceNameSelect);
          var confirmDelete = confirm(confirmText);
          if (confirmDelete){
            requestObject = { serviceNameSelect: serviceNameSelect };
          }
      }else {
        alert("There is nothing to delete.")
      }
    }

    if (requestObject){
        var jsonRequest = JSON.stringify(requestObject);
        request.onload = function () {
            if (request.status == 200) {
                if (operationSelect === "OPR_SELECT"){
                    var jsonTextArea = document.getElementById("jsonTextArea");
                    jsonTextArea.value = request.responseText;
                } else if(operationSelect === "OPR_UPDATE") {
                    alert(request.responseText);
                } else if(operationSelect === "OPR_INSERT") {
                    var jsonTextArea = document.getElementById("jsonTextArea");
                    var serviceNameInput = document.getElementById("serviceNameInput");
                    jsonTextArea.value = "";
                    serviceNameInput.value = "";
                    alert(request.responseText);
                } else if (operationSelect === "OPR_DELETE"){
                    fillServiceNames();
                    alert(request.responseText);
                }
            } else if (request.status == 404){
                alert(request.responseText)
            }
        }
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(jsonRequest);
    }
}

function onCopyImageClick(){
    var jsonTextArea = document.getElementById("jsonTextArea").value;
    if (jsonTextArea){
        copyTextToClipboard(jsonTextArea)
    } else {
        alert("There is nothing to select");
    }
}

function copyServicePath(){
    var servicePath = document.getElementById("servicePathLabel").innerText;
    copyTextToClipboard(servicePath)
}

function copyTextToClipboard(textToCopy) {
  navigator.permissions.query({ name: "clipboard-write" }).then((result) => {
      if (result.state == "granted") {
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert("Copied to Clipboard");
        });
      } else {
        alert("Clipboard permission is NOT granted.");
      }
    });
}

function createRequest(method, url) {
    var request = new XMLHttpRequest();
    if ("withCredentials" in request) {
        request.open(method, url, false);
    } else if (typeof XDomainRequest != "undefined") {
        request = new XDomainRequest();
        request.open(method, url);
    } else {
        console.log("CORS not supported");
        alert("CORS not supported");
        request = null;
    }
    return request;
}