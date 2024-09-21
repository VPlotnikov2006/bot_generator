let n = 0;

let nodeList = document.querySelector("#node-list ul");

export const addNode = () => {
    let l = document.createElement("li");
    l.innerHTML = "Узел" + n++;
    nodeList.appendChild(l);
}