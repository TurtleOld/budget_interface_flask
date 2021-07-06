function removeField(btn) {
    const div = btn.closest(".field");
    if (div) {
        div.remove();
      }
}

function addField(btn) {
    const form = btn.closest("form");
    console.log(form)
    if (form) {
        const div1 = form.querySelector(".field");
        if (div1) {
            const div = document.createElement("div");
            div.className = div1.className;
            div.innerHTML = div1.innerHTML;
            form.appendChild(div);
    }
  }
}