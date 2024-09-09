import { addNode, addLine, updateLines} from "./graph.js";
import { uniformDistr, zip } from "./utils.js";

let k = 16;

for (let [[r, g, b], [x, y]] of zip(uniformDistr(k, 3, false, false), uniformDistr(k, 2, false, false)))
    addNode(`rgb(${r * 255}, ${g * 255}, ${b * 255})`, x * 400 - 12, y * 400 - 12);

addLine(0, 1);
addLine(1, 2);


updateLines();
