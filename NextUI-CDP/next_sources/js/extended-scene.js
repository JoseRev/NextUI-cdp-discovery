nx.define('ExtendedScene', nx.graphic.Topology.DefaultScene, {
	methods: {
		clickNode: function(sender, node){
            var right_corner = screen.width-450;
            var node_id = node["_data-id"];
            var name = node["_label"];
            console.log(username)
            var hostname;
            var password;
            var encoded_password;
            var username;
            var connection;
            topologyData["nodes"].forEach( element => {
            	if (element["name"]==name){
                    hostname = element["hostname"];
                    username = element["username"];
                    encoded_password = element["encoded_password"];
                    password = element["password"];
                    connection = element["connection"];
                }
            });
            if (connection.includes("ssh")){
            var URL = "http://" + ip_webssh + "/?hostname="+hostname+"&username="+username+"&password="+encoded_password;
            window.open(URL,"my   window","menubar=1,resizable=1,width=450,height=350,top=0,left="+right_corner);
            }
            else if(connection.includes("telnet")){
            var URL = "http://" +ip_webssh + "/?"+"Telnet="+hostname+"&Usuario="+username+"&Contraseña="+password+"&hostname=10.20.95.201&username=root&password=YzNjMG1yM2QzNQ==     ";
            window.open(URL,"my   window","menubar=1,resizable=1,width=850,height=350,top=0,left="+right_corner);
            }

		}
	}
});
