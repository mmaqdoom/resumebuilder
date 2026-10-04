document.addEventListener("click", (event) => {
    const addButton = event.target.closest("[data-add-row]");
    if (addButton) {
        const target = document.getElementById(addButton.dataset.addRow);
        const template = document.getElementById(`${addButton.dataset.addRow.split("-")[0]}-prototype`);
        if (!target || !template) {
            return;
        }
        const indexes = Array.from(target.querySelectorAll("[data-index]"))
            .map((row) => Number(row.dataset.index))
            .filter(Number.isFinite);
        const nextIndex = indexes.length ? Math.max(...indexes) + 1 : 0;
        const markup = template.innerHTML.replaceAll("__prefix__", String(nextIndex));
        target.insertAdjacentHTML("beforeend", markup);
        const addedRow = target.lastElementChild;
        addedRow.querySelector("input, textarea")?.focus();
        return;
    }

    const removeButton = event.target.closest("[data-remove-row]");
    if (removeButton) {
        const row = removeButton.closest(".dynamic-row");
        const deleted = row?.querySelector('input[name$="-deleted"]');
        if (row && deleted) {
            deleted.value = "1";
            row.hidden = true;
        }
    }
});
