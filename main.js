import * as graph from "./graph.js";
import * as graphList from "./graph-list.js";
import { uniformDistr, zip } from "./utils.js";


document.querySelector("#node-list span button").onclick = graphList.addNode;

test();
let k = 16;

for (let [[r, g, b], [x, y]] of zip(uniformDistr(k, 3, false, false), uniformDistr(k, 2, false, false)))
    graph.addNode(`rgb(${r * 255}, ${g * 255}, ${b * 255})`, x * 400 - 10, y * 400 - 10);


graph.addLine(0, 1);
graph.addLine(1, 2);


graph.updateLines();
