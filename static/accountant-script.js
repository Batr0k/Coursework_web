const DOMEN = "http://127.0.0.1:8000/";
async function get_payments() {
const table = document.getElementById("table");
const insert_form = document.getElementById("insert_form");
insert_form.innerHTML = `<h2>Добавление новой оплаты</h2><label>Жилец</label>
             <select id = "occupant_select" required>
            </select>
            <label>Количество месяцев</label>
            <input type = "number" id = "number_month" name = "number_month" required>
            <label>Дата оплаты</label>
            <input type = "date" id = "date_paid" name = "date_paid" required>
            <input type="submit">`;
const clonedForm = insert_form.cloneNode(true);
insert_form.parentNode.replaceChild(clonedForm, insert_form);
clonedForm.addEventListener("submit", async function(event){
        event.preventDefault();
        const occupant_id = document.getElementById("occupant_select").value;
        const number_of_month_paid = document.getElementById("number_month").value;
        const date_paid = document.getElementById("date_paid").value;
        await fetch(`${DOMEN}accountant/insert_payment?id=${occupant_id}&number_of_month_paid=${number_of_month_paid}&payment_date=${date_paid}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    get_payments();
});
const response_occupants = await fetch(`${DOMEN}accountant/occupants`);
const data_occupants = await response_occupants.json();
const occupant_select = document.getElementById("occupant_select");
data_occupants.forEach(i => {
const newOption = document.createElement("option");
newOption.textContent = `${i.name} ${i.surname} ${i.patronymic}`;
newOption.value = i.id;
occupant_select.appendChild(newOption);
});
table.innerHTML =`<tr>
    <th>Фамилия плательщика</th>
    <th>Имя плательщика</th>
    <th>Отчество плательщика</th>
    <th>Дата оплаты</th>
    <th>Количество оплаченных месяцев</th>
    <th>Стоимость в месяц, руб</th>
    </tr>`;
    response = await fetch(`${DOMEN}accountant/payments`);
    const data = await response.json();
    data.forEach(element => {
        const newRow = document.createElement("tr");
            newRow.classList.add("row");
//            newRow.addEventListener('click', () => update_furniture(element.id));
            newRow.innerHTML = `<td>${element.occupant.surname}</td>
            <td>${element.occupant.name}</td>
            <td>${element.occupant.patronymic}</td>
            <td>${element.payment_date}</td>
                <td>${element.number_of_month_paid}</td>
                <td>${element.cost_per_month.price}</td>`;
            table.appendChild(newRow);
    });

}
async function get_cost_per_month() {
const insert_form = document.getElementById("insert_form");
const clonedForm = insert_form.cloneNode(true);
insert_form.parentNode.replaceChild(clonedForm, insert_form);
clonedForm.innerHTML = ` <h2>Добавление новой стоимости оплаты</h2><label>Дата установления стоимости</label>
            <input type = "date" id = "price_date" name = "price_date" required>
            <label>Стоимость</label>
            <input type = "number" id = "price" name = "price" required>
            <label>Вместимость комнаты</label>
            <select id = "room_type">
            <option value = '{"max_occupants": 1, "area": 9,"id": 1}'>1</option>
            <option value = '{"max_occupants": 2, "area": 12,"id": 2}'>2</option>
            <option value = '{"max_occupants": 3, "area": 18,"id": 3}'>3</option>
            </select>
            <input type="submit">`;
            clonedForm.addEventListener("submit", async function(event){
        event.preventDefault();
        const formData = {
        price_date: document.getElementById("price_date").value,
        price: document.getElementById("price").value,
        room_type: JSON.parse(document.getElementById("room_type").value)
        };
        await fetch(`${DOMEN}accountant/insert_cost_per_month`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
    get_cost_per_month();
});
    const table = document.getElementById("table");
    table.innerHTML =`<tr>
        <th>Дата изменения оплаты</th>
        <th>Установленная цена</th>
        <th>Для комнаты к вместимостью, человек</th>
        </tr>`;
        const response = await fetch(`${DOMEN}accountant/cost_per_month`);
    const data = await response.json();
    data.forEach(element => {
        const newRow = document.createElement("tr");
            newRow.classList.add("row");
//            newRow.addEventListener('click', () => update_furniture(element.id));
            newRow.innerHTML = `<td>${element.price_date}</td>
            <td>${element.price}</td>
            <td>${element.room_type.max_occupants}</td>`;
            table.appendChild(newRow);
    });
}
async function get_furniture() {
const insert_form = document.getElementById("insert_form");
const clonedForm = insert_form.cloneNode(true);
insert_form.parentNode.replaceChild(clonedForm, insert_form);
clonedForm.innerHTML = `<h2>Добавление новой мебели</h2><label>Название мебели</label>
        <input type = "text" id = "name" name = "name" required>
        <label>Описание</label>
        <input type = "text" id = "description" name = "description" required>
        <label>Стоимость</label>
        <input type = "number" id = "cost" name = "cost" required>
        <input type="submit">`;
        clonedForm.addEventListener("submit", async function(event){
        event.preventDefault();
        const formData = {
        description: document.getElementById("description").value,
        name: document.getElementById("name").value,
        cost: document.getElementById("cost").value
        };
        await fetch(`${DOMEN}accountant/insert_furniture`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
    get_furniture();
});
 const table = document.getElementById("table");
    table.innerHTML = `<tr>
    <th>Название</th>
    <th>Описание</th>
    <th>Стоимость, руб</th>
    <th>Удалить</th>
    </tr>`;
    const response = await fetch(`${DOMEN}accountant/furniture`);
    const data = await response.json();
    data.forEach(element => {
        const newRow = document.createElement("tr");
            newRow.classList.add("row");
            newRow.innerHTML = `<td>${element.name}</td>
                <td>${element.description}</td>
                <td>${element.cost}</td>`;
            const td = document.createElement("td");
            td.textContent = "X";
            td.addEventListener("click", async function() {
            await fetch(`${DOMEN}accountant/furniture/${element.id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });
            get_furniture();
            });
            newRow.appendChild(td);
            table.appendChild(newRow);
    });
}
const a1 = document.getElementById("a1");
const a2 = document.getElementById("a2");
const a3 = document.getElementById("a3");
a1.addEventListener('click', get_payments);
a2.addEventListener('click', get_cost_per_month);
a3.addEventListener('click', get_furniture);
get_payments();