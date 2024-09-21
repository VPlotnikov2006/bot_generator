graphList = {
    n: 0,
    nodeList: document.querySelector("#node-list ul"),
    addNode: () => {
        let l = document.createElement("li");
        l.id = "node_list" + graphList.n++;
        l.innerHTML = "Узел" + graphList.n;
        graphList.nodeList.appendChild(l);
    },
    deleteNode: (i) => {
        let l = document.querySelector("#node-list ul #node_list" + i);
        if (l == null)
            return;
        for (let cur = l.nextElementSibling; cur; cur = cur.nextElementSibling, i++) 
            cur.id = "node_list" + i;
        graphList.n--;
        l.remove();
    }
}