document.querySelector("#node-list span button").onclick = graphList.addNode;

let k = 16;

for (let [[r, g, b], [x, y]] of utils.zip(utils.uniformDistr(k, 3, false, false), utils.uniformDistr(k, 2, false, false)))
    graph.addNode(`rgb(${r * 255}, ${g * 255}, ${b * 255})`, x * 400 - 10, y * 400 - 10);


graph.addLine(0, 1);
graph.addLine(1, 2);


graph.updateLines();
