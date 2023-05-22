
// telnet webssh

// Borrar equipo del Inventario
del_inventory = function() {
    var esqDer = screen.width-550;
    var center = 250;
    window.open("http://" + ip + "/delInventory","delInventario","menubar=1,resizable=1,width=550,height=200,top=350,"+"left="+esqDer);
}

// Borrar equipo de Topologia JavaScript
node_del = function() {
    var esqDer = screen.width-550;
    var center = 250;
    window.open("http://" + ip + "/delNode","node_del","menubar=1,resizable=1,width=550,height=200,top=350,"+"left="+esqDer);
}

// Abir nueva ventana para agregar al inventario
add_inventory = function() {
    var esqDer = screen.width-550;
    var center = 250;
    window.open("http://" + ip + "/addInventory","addInventorio","menubar=1,resizable=1,width=550,height=420,top=250,"+"left="+esqDer);
    // window.location.reload(true);
}

// Abir nueva ventana para agregar un nodo
node_add = function() {
    //nodeSet_add()
    var esqDer = screen.width-550;
    var center = 250;
    window.open("http://" + ip + "/addNode","node_add","menubar=1,resizable=1,width=550,height=620,top=250,"+"left="+esqDer);

}

// Mostrar la informacion de topology.js
topology_js = function() {
    var esqDer = screen.width-550;
    var center = 250;
    window.open("http://" + ip + "/topology_js","topology_js","menubar=1,resizable=1,width=550,height=1450,top=-30,left=0");
}

// Abir nueva ventana para leer y mostrar inventory/hosts.yaml
inventory_hosts_yaml = function() {
    var esqDer = screen.width-550;
    var center = 250;
    window.open("http://" + ip + "/inventory_hosts_yaml","inventory_hosts_yaml","menubar=1,resizable=1,width=550,height=1450,top=-30,left=0");
}

// Invertir interfaces API
invertir_interfaces = function() {
    console.log("u");
    fetch("http://"+ip+"/invertir-interfaces");
    window.location.reload(true);
}

// Modo Aleatorio
modo_aleatorio = function() {
    fetch("http://"+ip+"/modo-aleatorio");
    window.location.reload(true);
}

// Modo Aleatorio
cdp = function() {
    fetch("http://"+ip+"/cdp");
    window.location.reload(true);
}

// Mostrar/ocultar intarfaces
    mostrar_ocultar_interfaces = function() {
    console.log("funcion mostrar ocultar interfaces");
    fetch("http://" + ip + "/show-interfaces");
    window.location.reload(true);
    console.log("cambio de interfaces exitoso, ip: " + ip)
}

// Recarga la pagina, eliminando los temporales
    actualizar = function() {
    console.info('reload page');
    window.location.reload(true);
}
