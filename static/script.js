const get_residents = document.querySelector("table");
get_residents.addEventListener("load", () => {
    fetch("http://127.0.0.1:8000/komendant/residents")
    .then(data => console.log(data));
});

