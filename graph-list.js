graphList = {
    nodeList: document.querySelector("#node-list ul"),
    nodesId: [],
    idCounter: -1,
    updateId: () => {
        let i = 0;
        for (let l of graphList.nodeList.querySelectorAll("li"))
            l.id = "node_list" + i++;
    },
    addNode: (color, x, y) => {
        graph.addNode(color, x, y, ++graphList.idCounter);
        graphList.nodesId.push(graphList.idCounter);
        let l = document.createElement("li");
        let n = document.createElement("div");
        n.className = "node"
        n.style.backgroundColor = color;
        l.appendChild(n);
        graphList.nodeList.appendChild(l);
        graphList.updateId();
    },
    deleteNode: (k) => {
        let l = document.querySelector("#node-list ul #node_list" + nodesId[k]);
        graphList.nodesId.splice(k, 1);
        if (l)
            l.remove();
        graphList.updateId();
    },
    
}