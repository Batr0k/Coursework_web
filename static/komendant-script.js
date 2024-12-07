
async function update_occupant(id) {
    // Запрос на открытие странички для просмотра подробной информации о жильце или изменении/удалении данных
     response = await fetch(`http://127.0.0.1:8000/komendant/occupants/${id}`);
     data = await response.json();
     const form = document.getElementById("update_form");
     const clonedForm = form.cloneNode(true);
     form.parentNode.replaceChild(clonedForm, form);
     document.getElementById("surname").value = data.surname;
     document.getElementById("name").value = data.name;
     document.getElementById("patronymic").value = data.patronymic;
     document.getElementById("phone_number").value = data.phone_number;
     document.getElementById("birth_date").value = data.birth_date;
     document.getElementById("check_in_date").value = data.check_in_date;
     clonedForm.addEventListener("submit", async function(event){
        event.preventDefault();
        const formData = {
            surname: document.getElementById("surname").value,
            name: document.getElementById("name").value,
            patronymic: document.getElementById("patronymic").value,
            phone_number: document.getElementById("phone_number").value,
            birth_date: document.getElementById("birth_date").value,
            check_in_date: document.getElementById("check_in_date").value,
            payments: null,
            room: { number: document.getElementById("room_select").value }
        };
        await fetch(`http://127.0.0.1:8000/komendant/occupants/update/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
    get_occupants();
});
};
// Вывод списка жильцов
async function get_occupants() {
    const div_instruments = document.getElementById("instruments_div");
    div_instruments.innerHTML = "";
    const add_occupant_button = document.createElement("button");
    add_occupant_button.textContent = "Добавить нового жильца";
    add_occupant_button.id = "add-occupant-button";
    add_occupant_button.classList.add("add-occupant");
    add_occupant_button.addEventListener('click', insert_occupant);
    div_instruments.appendChild(add_occupant_button);
    const table = document.getElementById("table");
    const work_area = document.getElementById("work_area");
    const update_form = document.getElementById("update_form");
    update_form.innerHTML = `
            <label>Фамилия</label>
            <input type = "text" id = "surname" name = "surname" required>
            <label>Имя</label>
            <input type = "text" name = "name" id = "name" required>
            <label>Отчество</label>
            <input type = "text" name = "patronymic" id = "patronymic" required>
            <label>Год рождения</label>
            <input type="date" name = "birth_date" id = "birth_date" required>
            <label>Телефон</label>
            <input type="text" name = "phone_number" id = "phone_number" required>
            <label>Комната проживания</label>
             <select id = "room_select" required>
            </select>
            <label>Дата заселения</label>
            <input type="date" name = "check_in_date" id = "check_in_date" required>
            <input type="submit">`;
    table.innerHTML = `<tr>
        <th>ФИО</th>
        <th>Год рождения</th>
        <th>Телефон</th>
        <th>Комната проживания</th>
        <th>Дата заселения</th>
        </tr>`;
    const response = await fetch('http://127.0.0.1:8000/komendant/free_rooms');
    const data = await response.json();
    const room_select = document.getElementById("room_select");
    data.forEach(element => {
        const newOption = document.createElement("option");
        newOption.value = element[0];
        newOption.text = element[1];
        room_select.add(newOption);
    });
    fetch('http://127.0.0.1:8000/komendant/occupants')
    .then(response => response.json())
    .then(data => {
        data.forEach(element => {
            const newRow = document.createElement("tr");
            // Установка атрибута data-*
            newRow.dataset.occupantId = element.id;
            // Добавление к тегу tr класса
            newRow.classList.add("row");
            newRow.addEventListener('click', () => update_occupant(element.id));
            newRow.innerHTML = `<td>${element.surname} ${element.name} ${element.patronymic}</td>
                <td>${element.birth_date}</td>
                <td>${element.phone_number}</td>
                <td>${element.room?.number}</td>
                <td>${element.check_in_date}</td>`;
            table.appendChild(newRow);
        });

    });
}
async function insert_occupant() {
     const form = document.getElementById("update_form");
     const clonedForm = form.cloneNode(true);
     form.parentNode.replaceChild(clonedForm, form);
     clonedForm.reset();
clonedForm.addEventListener("submit", async function(event){
    event.preventDefault();
    const formData = {
        surname: document.getElementById("surname").value,
        name: document.getElementById("name").value,
        patronymic: document.getElementById("patronymic").value,
        phone_number: document.getElementById("phone_number").value,
        birth_date: document.getElementById("birth_date").value,
        check_in_date: document.getElementById("check_in_date").value,
        payments: null,
        room:  { number: document.getElementById("room_select").value }
    };
     await fetch("http://127.0.0.1:8000/komendant/occupants", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
    get_occupants();
});
}
async function get_rooms() {
    const div_instruments = document.getElementById("instruments_div");
    div_instruments.innerHTML = "";
    const table = document.getElementById("table");
    table.innerHTML = `<tr>
    <th>Номер комнаты</th>
    <th>Этаж</th>
    <th>Максимальное количество мест</th>
    <th>Площадь</th>
    </tr>`;
    const update_form = document.getElementById("update_form");
    update_form.innerHTML = "";
    const response = await fetch('http://127.0.0.1:8000/komendant/rooms');
    const data = await response.json();
    data.forEach(element => {
        const newRow = document.createElement("tr");
            newRow.classList.add("row");
            newRow.innerHTML = `<td>${element.number}</td>
                <td>${element.floor.number}</td>
                <td>${element.room_type.max_occupants}</td>
                <td>${element.room_type.area}</td>`;
            table.appendChild(newRow);
    });
}
async function update_furniture(id) {
// Запрос на открытие странички для просмотра подробной информации о жильце или изменении/удалении данных
     response = await fetch(`http://127.0.0.1:8000/komendant/furniture/${id}`);
     data = await response.json();
     const form = document.getElementById("update_form");
     const clonedForm = form.cloneNode(true);
     form.parentNode.replaceChild(clonedForm, form);
     document.getElementById("description").value = data.description;
     clonedForm.addEventListener("submit", async function(event){
        event.preventDefault();
        const formData = {
            name: "",
            cost: 0,
            description: document.getElementById("description").value,
            room: { number: document.getElementById("room_furniture_select").value }
        };
        await fetch(`http://127.0.0.1:8000/komendant/furniture/update/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
    get_furniture();
});
}
async function get_furniture() {
    const div_instruments = document.getElementById("instruments_div");
    div_instruments.innerHTML = "";
    const table = document.getElementById("table");
    table.innerHTML = `<tr>
    <th>Название</th>
    <th>Описание</th>
    <th>Стоимость, руб</th>
    <th>В какой комнате находится</th>
    </tr>`;
    const update_form = document.getElementById("update_form");
    update_form.innerHTML = `
            <label>Описание</label>
            <input type = "text" id = "description" name = "description" >
            <label>Комната</label>
             <select id = "room_furniture_select">
            </select>
            <input type="submit">`;
    const room_furniture_select = document.getElementById("room_furniture_select");
    for (let i = 1; i < 161; i++) {
        const newOption = document.createElement("option");
        newOption.value = i;
        newOption.text = i;
        room_furniture_select.appendChild(newOption);
    }
    const response = await fetch('http://127.0.0.1:8000/komendant/furniture');
    const data = await response.json();
    data.forEach(element => {
        const newRow = document.createElement("tr");
            newRow.classList.add("row");
            newRow.addEventListener('click', () => update_furniture(element.id));
            newRow.innerHTML = `<td>${element.name}</td>
                <td>${element.description}</td>
                <td>${element.cost}</td>
                <td>${element.room.number}</td>`;
            table.appendChild(newRow);
    });
}

const a1 = document.getElementById("a1");
const a2 = document.getElementById("a2");
const a3 = document.getElementById("a3");
get_occupants();
insert_occupant();
add_occupant_button = document.getElementById("add-occupant-button");
a1.addEventListener('click', get_occupants);
a2.addEventListener('click', get_rooms);
a3.addEventListener('click', get_furniture);
add_occupant_button.addEventListener('click', insert_occupant);
// Добавление обработчика событий в форму
