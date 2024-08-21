const n = 3;

const nodeContainer = document.getElementById("node-container");
const lineContainer = document.getElementById("line-container");
const graphWindow = document.getElementById("graph-window");

const e = [
    [0, 2],
    // [4, 2],
    // [1, 2],
    // [2, 3],
    // [5, 6]
];

const clamp = (mn, val, mx) => {return Math.max(mn, Math.min(mx, val));}

const getCenter = (i) => {
    const p = document.getElementById("node" + i);
    const x = parseFloat(p.style.left) + p.offsetWidth / 2;
    const y = parseFloat(p.style.top) + p.offsetHeight / 2;
    return [x, y];
}

const updateLines = () => {
    for (let i in e) {
        const [s, f] = e[i];
        const [x1, y1] = getCenter(s);
        const [x2, y2] = getCenter(f);
        let line = document.getElementById("line-" + s + "-" + f);
        line.setAttribute("x1", x1);
        line.setAttribute("y1", y1);
        line.setAttribute("x2", x2);
        line.setAttribute("y2", y2);
    }
}

for (let i = 0; i < n; i++) {
    const node = document.createElement("div");
    node.className = "node";
    node.style.top = Math.random() * 100 + "px";
    node.style.left = Math.random() * 100 + "px";
    node.style.backgroundColor = "red";
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
}

for (let i in e) {
    let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    let defs = document.createElementNS(svg.namespaceURI, "defs");
    let marker = document.createElementNS(defs.namespaceURI, "marker");
    let polygon = document.createElementNS(marker.namespaceURI, "polygon");
    svg.style.position = "absolute";
    svg.style.left = "0px";
    svg.style.top = "0px";
    svg.setAttribute("width", "500");
    svg.setAttribute("height", "500");
    svg.setAttribute("viewBox", "0 0 500 500");

    marker.setAttribute("id", "arrow");
    marker.setAttribute("refX", "7");
    marker.setAttribute("refY", "3.5");
    marker.setAttribute("markerWidth", "10");
    marker.setAttribute("markerWidth", "7");
    marker.setAttribute("orient", "auto");
    
    polygon.setAttribute("points", "0 0, 10 3.5, 0 7");
    
    marker.appendChild(polygon);
    defs.appendChild(marker);

    let line = document.createElementNS(svg.namespaceURI, "line");
    line.setAttribute("stroke", "teal");
    line.setAttribute("stroke-width", "8");
    line.setAttribute("marker-end", "url(#arrow)");
    line.id = "line-" + e[i][0] + "-" + e[i][1];

    svg.appendChild(defs);
    svg.appendChild(line);

    lineContainer.appendChild(svg);
}

updateLines();
// 'url(data:image/svg+xml;utf8,<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow" viewBox="0 -5 10 10" refX="5" refY="0" markerWidth="4" markerHeight="4" orient="auto"><path class="cool" d="M0,-5L10,0L0,5"></path></marker></defs><line fill="teal" x1="100" y1="150" x2="130" y2="350" stroke="teal" stroke-width="4" marker-end="url(#arrow)"></line></svg>)'
// data:image/svg+xml;utf8,<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow" viewBox="0 -5 10 10" refX="5" refY="0" markerWidth="4" markerHeight="4" orient="auto"><path class="cool" d="M0,-5L10,0L0,5"></path></marker></defs><line fill="teal" x1="100" y1="150" x2="130" y2="350" stroke="teal" stroke-width="4" marker-end="url(#arrow)"></line></svg>