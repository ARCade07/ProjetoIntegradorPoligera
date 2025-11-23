const role = document.cookie.split("; ").find(linha => linha.startsWith("role="))?.split("=")[1];
if (role === "admin") {
    //document.getElementById("btn_estatistica").style.display = "block";
}
