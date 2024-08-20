const n = 3;

const nodeContainer = document.getElementById("node-container");
const lineContainer = document.getElementById("line-container");

const e = [
    [0, 2],
    // [4, 2],
    // [1, 2],
    // [2, 3],
    // [5, 6]
];

const getCenter = (i) => {
    const p = document.getElementById("node" + i);
    const x = parseFloat(p.style.left) + p.offsetWidth / 2;
    const y = parseFloat(p.style.top) + p.offsetHeight / 2;
    return [x, y];
}

const updateLines = () => {
    for (let i in e) {
        const [s, f] = e[i];
        const [sX, sY] = getCenter(s)
        const [fX, fY] = getCenter(f)
        const len = Math.sqrt((sX - fX) * (sX - fX) + (sY - fY) * (sY - fY));
        const ang = Math.atan2(fY - sY, fX - sX);
        let line = document.getElementById("line-" + s + "-" + f);
        line.style.width = len + "px";
        line.style.transform = "rotate(" + ang + "rad)";
        line.style.left = sX + "px";
        line.style.top = sY - line.offsetHeight / 2 + "px";
    }
}

for (let i = 0; i < n; i++) {
    const node = document.createElement("div");
    node.className = "node";
    node.style.top = Math.random() * 100 + "px";
    node.style.left = Math.random() * 100 + "px";
    node.style.backgroundColor = "red";
    node.id = "node" + i;
    node.textContent = i + 1;
    nodeContainer.appendChild(node);
}

for (let i in e) {
    let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    let defs = document.createElementNS(svg.namespaceURI, "defs");
    let marker = document.createElementNS(defs.namespaceURI, "marker");
    let path = document.createElementNS(marker.namespaceURI, "path");
    svg.style.position = "absolute";
    svg.style.left = "0px";
    svg.style.top = "0px";
    svg.setAttribute("width", "500");
    svg.setAttribute("height", "500");

    marker.setAttribute("id", "arrow");
    marker.setAttribute("viewBox", "0 -5 20 20");
    marker.setAttribute("refX", "13");
    marker.setAttribute("refY", "0");
    marker.setAttribute("markerWidth", "16");
    marker.setAttribute("orient", "auto");
    
    path.setAttribute("fill", "teal");
    path.setAttribute("stroke", "teal");
    path.setAttribute("d", "M0,-5L20,0L0,5");
    
    marker.appendChild(path);
    defs.appendChild(marker);

    let line = document.createElementNS(svg.namespaceURI, "line");
    line.setAttribute("stroke", "teal");
    line.setAttribute("stroke", "teal");
    line.setAttribute("stroke-width", "4");
    line.setAttribute("marker-end", "url(#arrow)");

    const [x1, y1] = getCenter(e[i][0]);
    const [x2, y2] = getCenter(e[i][1]);
    line.setAttribute("x1", x1);
    line.setAttribute("y1", y1);
    line.setAttribute("x2", x2);
    line.setAttribute("y2", y2);

    svg.appendChild(defs);
    svg.appendChild(line);

    lineContainer.appendChild(svg);
}

// updateLines();
// 'url(data:image/svg+xml;utf8,<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow" viewBox="0 -5 10 10" refX="5" refY="0" markerWidth="4" markerHeight="4" orient="auto"><path class="cool" d="M0,-5L10,0L0,5"></path></marker></defs><line fill="teal" x1="100" y1="150" x2="130" y2="350" stroke="teal" stroke-width="4" marker-end="url(#arrow)"></line></svg>)'
// data:image/svg+xml;utf8,<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow" viewBox="0 -5 10 10" refX="5" refY="0" markerWidth="4" markerHeight="4" orient="auto"><path class="cool" d="M0,-5L10,0L0,5"></path></marker></defs><line fill="teal" x1="100" y1="150" x2="130" y2="350" stroke="teal" stroke-width="4" marker-end="url(#arrow)"></line></svg>