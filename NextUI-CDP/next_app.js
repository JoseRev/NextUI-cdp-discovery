
(function (nx) {
    /**
     * NeXt UI base application
     */

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    var topo = new nx.graphic.Topology({
        // View dimensions
        width: 1700,
        height: 800,
        // Dataprocessor is responsible for spreading
        // the Nodes across the view.
        // 'force' dataprocessor spreads the Nodes so
        // they would be as distant from each other
        // as possible. Follow social distancing and stay healthy.
        // 'quick' dataprocessor picks random positions
        // for the Nodes.

                                                    dataProcessor: 'force', //COMENTADO SIGNIFICA QUE LA TOPOLOGIA TOMA EN CUENTA LAS POSICIONES X,Y DECLARADAS EN LOS NODOS
        // Node and Link identity key attribute name
        identityKey: 'id',
        // Node settings
        nodeConfig: {
            label: 'model.name',
            iconType:'model.icon',
            color: function(model) {
                if (model._data.is_new === 'yes') {
                    return '#148D09'
                }
            },
        },
        // Node Set settings (for future use)
        nodeSetConfig: {
            label: 'model.name',
        //  iconType: 'model.iconType'
            iconType: 'model.icon'
        },

        // Tooltip content settings
        tooltipManagerConfig: {
            nodeTooltipContentClass: 'CustomNodeTooltip'
        },
        // Link settings
        linkConfig: {
            // Display Links as curves in case of 
            // multiple links between Node Pairs.
            // Set to 'parallel' to use parallel links.
            linkType: 'curve',
            sourcelabel: 'model.srcIfName', //#MODIFICADO PARA ELIMININAR INTERFACES
            targetlabel: 'model.tgtIfName', //#MODIFICADO PARA ELIMININAR INTERFACES
            style: { 'width': '10'},
            // color: 'blue'   //Cambiar color
        },

        // Display Node icon. Displays a dot if set to 'false'.
        showIcon: true,
        linkInstanceClass: 'CustomLinkClass'
    });

    var Shell = nx.define(nx.ui.Application, {
        methods: {
            start: function () {

                topo.on("topologyGenerated", function(topo, event){
                	topo.registerScene('extended-scene', 'ExtendedScene');
                	topo.activateScene('extended-scene');
                });
                // Modify Click Node Behavior in extended-tooltip-policy.js
                topo.tooltipManager().tooltipPolicyClass('ExtendedTooltipPolicy');
                // Read topology data from variable
                topo.data(topologyData);
                // Attach it to the document
                topo.attach(this);
            }
        }
    });

    nx.define('CustomNodeTooltip', nx.ui.Component, {
        properties: {
            node: {},
            topology: {}
        },
        view: {
            content: [{
                tag: 'div',
                content: [{
                    tag: 'h5',
                    content: [{
                        tag: 'a',
                        content: '{#node.model.name}',
                        props: {"href": "{#node.model.dcimDeviceLink}"}
                    }],
                    props: {
                        "style": "border-bottom: dotted 1px; font-size:90%; word-wrap:normal; color:#003688"
                    }
                }, {
                    tag: 'p',
                    content: [
                        {
                        tag: 'label',
                        content: 'IP: ',
                    }, {
                        tag: 'label',
                       // content: '{#node.model.primaryIP}',
                        content: '{#node.model.hostname}',
                    }
                    ],
                    props: {
                        "style": "font-size:80%;"
                    }
                },{
                    tag: 'p',
                    content: [
                        {
                        tag: 'label',
                        content: 'Mod: ',
                    }, {
                        tag: 'label',
                        content: '{#node.model.model}',
                    }
                    ],
                    props: {
                        "style": "font-size:80%;"
                    }
                },{
                    tag: 'p',
                    content: [
                        {
                        tag: 'label',
                        content: 'Serial: ',
                    }, {
                        tag: 'label',
                        content: '{#node.model.serial}',
                    }
                    ],
                    props: {
                        "style": "font-size:80%;"
                    }
                },{
                    tag: 'p',
                    content: [
                        {
                        tag: 'label',
                        content: 'Tipo: ',
                    }, {
                        tag: 'label',
                        content: '{#node.model.tipo}',
                    }
                    ],
                    props: {
                        "style": "font-size:80%; padding:0"
                    }
                },{
                    tag: 'p',
                    content: [
                        {
                        tag: 'label',
                        content: 'Protocolo: ',
                    }, {
                        tag: 'label',
                        content: '{#node.model.connection}',
                    }
                    ],
                    props: {
                        "style": "font-size:80%;"
                    }
                },{
                    tag: 'p',
                    content: [
                        {
                        tag: 'label',
                        content: 'Usuario: ',
                    }, {
                        tag: 'label',
                        content: '{#node.model.username}',
                    }
                    ],
                    props: {
                        "style": "font-size:80%;"
                    }
                },{
                    tag: 'p',
                    content: [
                        {
                        tag: 'label',
                        content: 'Password: ',
                    }, {
                        tag: 'label',
                        content: '{#node.model.password}',
                    }
                    ],
                    props: {
                        "style": "font-size:80%;"
                    }
                }
            ],
            props: {
                "style": "width: 150px;"
            }
        }]
        }
    });

    nx.define('Tooltip.Node', nx.ui.Component, {
        view: function(view){
            view.content.push({
            });
            return view;
        },
        methods: {
            attach: function(args) {
                this.inherited(args);
                this.model();
            }
        }
    });

    nx.define('CustomLinkClass', nx.graphic.Topology.Link, {
        properties: {
            sourcelabel: null,
            targetlabel: null
        },
        view: function(view) {
            view.content.push({
                name: 'source',
                type: 'nx.graphic.Text',
                props: {
                    'class': 'sourcelabel',
                    'alignment-baseline': 'text-after-edge',
                    'text-anchor': 'start'
                }
            }, {
                name: 'target',
                type: 'nx.graphic.Text',
                props: {
                    'class': 'targetlabel',
                    'alignment-baseline': 'text-after-edge',
                    'text-anchor': 'end'
                }
            });

            return view;
        },
        methods: {
            update: function() {
                this.inherited()
                var el, point;
                var line = this.line();
                var angle = line.angle();
                var stageScale = this.stageScale();

                // pad line
                line = line.pad(18 * stageScale, 18 * stageScale);

                if (this.sourcelabel()) {
                    el = this.view('source');
                    point = line.start;
                    el.set('x', point.x);
                    el.set('y', point.y);
                    el.set('text', this.sourcelabel());
                    el.set('transform', 'rotate(' + angle + ' ' + point.x + ',' + point.y + ')');
                    el.setStyle('font-size', 12 * stageScale);
                }

                if (this.targetlabel()) {
                    el = this.view('target');
                    point = line.end;
                    el.set('x', point.x);
                    el.set('y', point.y);
                    el.set('text', this.targetlabel());
                    el.set('transform', 'rotate(' + angle + ' ' + point.x + ',' + point.y + ')');
                    el.setStyle('font-size', 12 * stageScale);
                }
            }
        }
    });

    var currentLayout = 'auto';
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    guardar = function(){
        var data = {'nodes': []};
        nodesLayer = topo.getLayer('nodes');
        nodesLayer.eachNode(function(node){
        data.nodes.push({
            'x': node.x(),
            'y': node.y(),
            'nodeid': node.model()._data['id'],
            'nodeName': node.model()._data['name']

            });
        });


        var NodeSet_data = {'nodeSet': []};
        nodeSetLayer = topo.getLayer('nodeSet');
        nodeSetLayer.eachNodeSet(function(nodeSet){
        NodeSet_data.nodeSet.push({
           'x': nodeSet.x(),
           'y': nodeSet.y(),
            'id': nodeSet.model()._data['id'],
            'name': nodeSet.model()._data['name'],
            'nodes': nodeSet.model()._data['nodes']
           });
       });

       var list_nodes = [data, NodeSet_data];
       console.log('lista nodes, nodeSet: ',  JSON.stringify(list_nodes));

        const options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(list_nodes)
            };

            /////// TSHOOT -> console.log(typeof topo)
            /////// Pagina web para pruebas POST (regresa lo mismo que le mandas)
            /////// fetch('https://httpbin.org/post',  options)

           fetch('http://'+ip+'/SavePosition.json',  options)
           .then(res => res.json())
           .then(data => console.log(NodeSet_data))
            };
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    marcar_NodeSet = function(){
        var NodeSet_data = {'nodeSet': []};
        nodeSetLayer = topo.getLayer('nodeSet');
        nodeSetLayer.eachNodeSet(function(nodeSet){
        NodeSet_data.nodeSet.push({
            'id': nodeSet.model()._data['id'],
            'name': nodeSet.model()._data['name'],
            'nodes': nodeSet.model()._data['nodes']
           });
       });
       nodeSet_list=[NodeSet_data]
       var list_nodes = NodeSet_data;
       console.log('nodeSet: ',  JSON.stringify(NodeSet_data));

        const options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
//            body: JSON.stringify(NodeSet_data)
            body: JSON.stringify(nodeSet_list)
            };

       fetch('http://' + ip + '/addNodeSet.json',  options) //
       .then(res => res.json())
       .then(data => console.log(NodeSet_data))
        };

//        var esqDer = screen.width-550;
//        var center = 250;
//        window.open("http://192.168.1.83:5000/addNode","node_add","menubar=1,resizable=1,width=550,height=620,top=250,"+"left="+esqDer);
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    horizontal = function() {
        if (currentLayout === 'horizontal') {
            return;
        };
        currentLayout = 'horizontal';
        var layout = topo.getLayout('hierarchicalLayout');
        layout.direction('horizontal');
        layout.levelBy(function(node, model) {
            return model.get('layerSortPreference');
        });
        topo.activateLayout('hierarchicalLayout');
    };

    vertical = function() {
        if (currentLayout === 'vertical') {
            return;
        };
        currentLayout = 'vertical';
        var layout = topo.getLayout('hierarchicalLayout');
        layout.direction('vertical');
        layout.levelBy(function(node, model) {
          return model.get('layerSortPreference');
        });
        topo.activateLayout('hierarchicalLayout');
    };

    // Create an application instance
    var shell = new Shell();
    // Run the application
    shell.start();
})(nx);
