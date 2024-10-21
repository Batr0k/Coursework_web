function create_table() {
    let table = document.getElementById("table");
    if (table) return table;
    table = document.createElement("table");
    table.id = "table";
    document.body.appendChild(table);
    return table;
}
function update_occupant(id) {
    // Запрос на открытие странички для просмотра подробной информации о жильце или изменении/удалении данных
    fetch(`http://127.0.0.1:8000/komendant/occupants/${id}`)
    .then(response => response.json())
    .then(data => {


    });
};
function get_occupants() {
    const table = create_table();
    table.innerHTML = `<tr>
        <th>ФИО</th>
        <th>Фото</th>
        <th>Год рождения</th>
        <th>Телефон</th>
        <th>Комната проживания</th>
        <th>Дата заселения</th>
        </tr>`;
    fetch('http://127.0.0.1:8000/komendant/occupants')
    .then(response => response.json())
    .then(data => {
        data.forEach(element => {
            const newRow = document.createElement("tr");
            // Установка атрибута data-*
            newRow.dataset.occupantId = element.id;
            // Добавление к тегу tr класса
            newRow.classList.add("row");
            newRow.addEventListener('click', update_occupant.bind(element.id));
            newRow.innerHTML = `<td>${element.surname} ${element.name} ${element.patronymic}</td>
                <td>${element.photo}</td>
                <td>${element.birth_date}</td>
                <td>${element.phone_number}</td>
                <td>${element.number}</td>
                <td>${element.check_in_date}</td>`;
            table.appendChild(newRow);
        });

    });
}
function get_rooms() {
    const table = create_table();
    table.innerHTML = `<tr>
    <th>Номер комнаты</th>
    <th>Этаж</th>
    <th>Максимальное количество мест</th>
    <th>Площадь</th>
    </tr>`;
}
function get_furniture() {
    const table = create_table();
    table.innerHTML = `<tr>
    <th>Название</th>
    <th>Описание</th>
    <th>В какой комнате находится</th>
    </tr>`;
}

const a1 = document.getElementById("a1");
const a2 = document.getElementById("a2");
const a3 = document.getElementById("a3");
window.onload = get_occupants;
a1.addEventListener('click', get_occupants);
a2.addEventListener('click', get_rooms);
a3.addEventListener('click', get_furniture);