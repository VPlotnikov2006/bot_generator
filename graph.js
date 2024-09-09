import { clamp, dist } from "./utils.js";

let n = 0;
let e = [];

let nodeContainer = document.querySelector("#node-container");
let lineContainer = document.querySelector("#line-container");
let graphWindow = document.querySelector("#graph-window");

const getCenter = (i) => {
    const p = document.querySelector("#node" + i);
    const x = p.getClientRects()[0].left - graphWindow.getClientRects()[0].left + p.offsetWidth / 2;
    const y = p.getClientRects()[0].top - graphWindow.getClientRects()[0].top + p.offsetHeight / 2;
    return [x, y];
}


export const addNode = (color, x, y) => {
    const node = document.createElement("div");
    node.className = "node";
    node.style.backgroundColor = color;
    node.id = "node" + (n++);
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

        document.onmouseup = () => {
            document.onmousemove = null;
            updateLines();
            node.onmouseup = null;
        }
    } 
   
    node.style.left = x + "px";
    node.style.top = y + "px";

    nodeContainer.appendChild(node);


}

export const addLine = (i, j) => {
    e.push([i, j]);
    let line = document.createElementNS(lineContainer.namespaceURI, "line");
    line.setAttribute("stroke", "black");
    line.setAttribute("stroke-width", "4");
    line.id = "line-" + i + "-" + j;
    lineContainer.appendChild(line);
}

export const updateLines = () => {
    for (let [s, f] of e) {
        const [x1, y1] = getCenter(s);
        const [x2, y2] = getCenter(f);
        let line = document.querySelector("#line-" + s + "-" + f);
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