const DOMEN = "http://127.0.0.1:8000/";
async function insert_worker() {
const worker_form = document.getElementById("worker_form");
worker_form.innerHTML = `
    <h2 id ="worker_h2">Добавить нового работника</h2>
            <label>Фамилия</label>
            <input type = "text" id = "surname" name = "surname" required>
            <label>Имя</label>
            <input type = "text" name = "name" id = "name" required>
            <label>Отчество</label>
            <input type = "text" name = "patronymic" id = "patronymic" required>
            <label>Телефон</label>
            <input type="text" name = "phone_number" id = "phone_number" required>
            <label>Должность</label>
            <select id = "position_at_work_select" required>
            </select>
            <input type="submit">`;
const position_at_work_select = document.getElementById("position_at_work_select");
const response_position = await fetch(`${DOMEN}director/position_at_work`);
position_data = await response_position.json();
position_data.forEach(element => {
    const option = document.createElement("option");
    option.value = JSON.stringify(element);
    option.textContent = element.position;
    position_at_work_select.appendChild(option);
});
     const clonedForm = worker_form.cloneNode(true);
     worker_form.parentNode.replaceChild(clonedForm, worker_form);
clonedForm.addEventListener("submit", async function(event) {
    const formData = {
        surname: document.getElementById("surname").value,
        name: document.getElementById("name").value,
        patronymic: document.getElementById("patronymic").value,
        phone_number: document.getElementById("phone_number").value,
        position_at_work: JSON.parse(document.getElementById("position_at_work_select").value)
    }
    await fetch(`${DOMEN}director/workers`, {
     method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
});
};
async function update_workers(id) {
const worker_form = document.getElementById("worker_form");
const response_workers = await fetch(`${DOMEN}director/workers/${id}`);
const data_workers = await response_workers.json();
document.getElementById("surname").value = data_workers.surname;
document.getElementById("name").value = data_workers.name;
document.getElementById("patronymic").value = data_workers.patronymic;
document.getElementById("phone_number").value = data_workers.phone_number;
const clonedForm = worker_form.cloneNode(true);
worker_form.parentNode.replaceChild(clonedForm, worker_form);
clonedForm.addEventListener("submit", async function(event) {
const formData = {
        surname: document.getElementById("surname").value,
        name: document.getElementById("name").value,
        patronymic: document.getElementById("patronymic").value,
        phone_number: document.getElementById("phone_number").value,
        position_at_work: JSON.parse(document.getElementById("position_at_work_select").value)
    }
    await fetch(`${DOMEN}director/workers/{id}`, {
     method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
 });

}
async function get_workers() {
insert_worker();
const table = document.getElementById("table");
table.innerHTML =`<tr>
    <th>Фамилия работника</th>
    <th>Имя работника</th>
    <th>Отчество работника</th>
    <th>Номер телефона</th>
    <th>Должность</th>
    <th>Удалить</th>
    </tr>`;
const response_workers = await fetch(`${DOMEN}director/workers`);
const data_workers = await response_workers.json();
data_workers.forEach(element => {
            const newRow = document.createElement("tr");
            newRow.dataset.Id = element.id;
            newRow.classList.add("row");
            const td1 = document.createElement("td");
            const td2 = document.createElement("td");
            const td3 = document.createElement("td");
            const td4 = document.createElement("td");
            const td5 = document.createElement("td");
            const td6 = document.createElement("td");
            td1.textContent = `${element.surname}`;
            td1.addEventListener('click', () => update_workers(element.id));
            newRow.appendChild(td1);
            td2.textContent = `${element.name}`;
            td2.addEventListener('click', () => update_workers(element.id));
            newRow.appendChild(td2);
            td3.textContent = `${element.patronymic}`;
            td3.addEventListener('click', () => update_workers(element.id));
            newRow.appendChild(td3);
            td4.textContent = `${element.phone_number}`;
            td4.addEventListener('click', () => update_workers(element.id));
            newRow.appendChild(td4);
            td5.textContent = `${element.position_at_work.position}`;
            td5.addEventListener('click', () => update_workers(element.id));
            newRow.appendChild(td5);
            td6.textContent = `X`;
            td6.addEventListener('click', async function() {
            await fetch(`${DOMEN}director/workers/${element.id}`,{
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json'
            }
            });
            get_workers();
            });
            newRow.appendChild(td6);
            table.appendChild(newRow);
        });
}
get_workers();
const a1 = document.getElementById("a1");
a1.addEventListener("click", get_workers);