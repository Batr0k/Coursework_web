function get_residents() {
    fetch('http://127.0.0.1:8000/komendant/residents')
    .then(response => response.json())
    .then(data => {
        const newElement = document.createElement("tr");
        const oldElement = document.getElementById("table");
        const childrenTable = oldElement.children;
        for (let i = 1; i < childrenTable.length; i++) {
            oldElement.removeChild(childrenTable[i]);
        }
        newElement.innerHTML = `<td> </td><td></td><td></td><td></td><td></td><td></td>`;
         oldElement.appendChild(newElement);
    });
}
const a1 = document.getElementById("a1");
window.onload = get_residents;
a1.addEventListener('click', get_residents);
