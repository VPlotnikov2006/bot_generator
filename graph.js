graph = {
    n: 0,
    e: [],

    nodeContainer: document.querySelector("#node-container"),
    lineContainer: document.querySelector("#line-container"),
    graphWindow: document.querySelector("#graph-window"),

    getCenter: (i) => {
        const p = document.querySelector("#node" + i);
        const x = parseInt(p.style.left) + p.clientWidth / 2;
        const y = parseInt(p.style.top) + p.clientHeight / 2;
        return [x, y];
    },


    addNode: (color, x, y) => {
        const node = document.createElement("div");
        node.className = "node";
        node.style.backgroundColor = color;
        node.id = "node" + (graph.n++);
        node.ondragstart = () => {return false;};
        node.onmousedown = (e) => {
            function move(e) {
                node.style.left = utils.clamp(
                    0,
                    e.pageX - graph.graphWindow.getClientRects()[0].left - node.offsetWidth / 2,
                    graph.graphWindow.getClientRects()[0].width - node.offsetWidth
                ) + "px";
                node.style.top = utils.clamp(
                    0,
                    e.pageY - graph.graphWindow.getClientRects()[0].top- node.offsetHeight / 2,
                    graph.graphWindow.getClientRects()[0].height - node.offsetHeight
                ) + "px";
                // updateLines();
            }

            move(e);
            // node.style.zIndex = 1000;


            document.onmousemove = (e) => {move(e); graph.updateLines();};

            document.onmouseup = () => {
                document.onmousemove = null;
                graph.updateLines();
                node.onmouseup = null;
            }
        } 
    
        node.style.left = x + "px";
        node.style.top = y + "px";
        graph.nodeContainer.appendChild(node);
    },

    addLine: (i, j) => {
        graph.e.push([i, j]);
        let line = document.createElementNS(graph.lineContainer.namespaceURI, "line");
        line.setAttribute("stroke", "black");
        line.setAttribute("stroke-width", "4");
        line.id = "line-" + i + "-" + j;
        graph.lineContainer.appendChild(line);
    },

    updateLines: () => {
        for (let [s, f] of graph.e) {
            const [x1, y1] = graph.getCenter(s);
            const [x2, y2] = graph.getCenter(f);
            let line = document.querySelector("#line-" + s + "-" + f);
            if (utils.dist(x1, y1, x2, y2) < 30)
                line.removeAttribute("marker-end");
            else
                line.setAttribute("marker-end", "url(#arrow)");
            line.setAttribute("x1", x1);
            line.setAttribute("y1", y1);
            line.setAttribute("x2", x2);
            line.setAttribute("y2", y2);
        }
    }
}
