const list_a = document.querySelectorAll("a");
list_a.forEach( (a)=> {
    a.addEventListener("mouseover", () => {
        a.style.backgroundColor = "#2db82a";
    });
});

