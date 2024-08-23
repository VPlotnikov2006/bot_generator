const n = 3;

const nodeContainer = document.getElementById("node-container");
const lineContainer = document.getElementById("line-container");
const graphWindow = document.getElementById("graph-window");

const e = [
    [0, 2],
    [1, 2],
    // [1, 2],
    // [2, 3],
    // [5, 6]
];

const clamp = (mn, val, mx) => {return Math.max(mn, Math.min(mx, val));}

const getCenter = (i) => {
    const p = document.getElementById("node" + i);
    const x = p.getClientRects()[0].left - graphWindow.getClientRects()[0].left + p.offsetWidth / 2;
    const y = p.getClientRects()[0].top - graphWindow.getClientRects()[0].top + p.offsetHeight / 2;
    return [x, y];
}

const dist = (x1, y1, x2, y2) => {
    return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
}

const addNode = (i, color) => {
    const node = document.createElement("div");
    node.className = "node";
    node.style.backgroundColor = color;
    node.id = "node" + i;
    node.ondragstart = () => {return false;};
    node.onmousedown = (e) => {
        function move(e) {
            node.style.left = clamp(
                0,
                e.pageX - graphWindow.getClientRects()[0].left - node.offsetWidth / 2,
                graphWindow.getClientRects()[0].width - node.offsetWidth
            ) + "px";
            node.style.top = clamp(
                0,
                e.pageY -graphWindow.getClientRects()[0].top- node.offsetHeight / 2,
                graphWindow.getClientRects()[0].height - node.offsetHeight
             ) + "px";
            // updateLines();
        }

        move(e);
        // node.style.zIndex = 1000;


        document.onmousemove = (e) => {move(e); updateLines();};

        node.onmouseup = () => {
            document.onmousemove = null;
            updateLines();
            node.onmouseup = null;
        }
    } 

    nodeContainer.appendChild(node);

    node.style.top = Math.random() * (graphWindow.getClientRects()[0].height - node.offsetHeight) + "px";
    node.style.left = Math.random() * (graphWindow.getClientRects()[0].width - node.offsetWidth) + "px";

}

const addLine = (i, j) => {
    let line = document.createElementNS(lineContainer.namespaceURI, "line");
    line.setAttribute("stroke", "black");
    line.setAttribute("stroke-width", "4");
    line.id = "line-" + i + "-" + j;
    lineContainer.appendChild(line);
}

const updateLines = () => {
    for (let i in e) {
        const [s, f] = e[i];
        const [x1, y1] = getCenter(s);
        const [x2, y2] = getCenter(f);
        let line = document.getElementById("line-" + s + "-" + f);
        if (dist(x1, y1, x2, y2) < 30)
            line.removeAttribute("marker-end");
        else
            line.setAttribute("marker-end", "url(#arrow)");
        line.setAttribute("x1", x1);
        line.setAttribute("y1", y1);
        line.setAttribute("x2", x2);
        line.setAttribute("y2", y2);
    }
}

for (let i = 0; i < n; i++) {
    addNode(i, ["red", "blue", "green"][i]);
}

for (let i in e) {
    addLine(...e[i]);
}

updateLines();
