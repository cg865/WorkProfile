/**
 * @param {HTMLDivElement} div
 * @param {number} id 
 */
function handlePersonClick(div, id) {
    const cssClass = div.className;
    if (cssClass === "person-disabled") { return; }
    fetch(`/delete/${id}`, { method: "DELETE" })
        .then(res => {
            if (res.status === 200) {
                const parent = div.parentElement;
                parent.removeChild(div);
                if (parent.children.length === 0) {
                    const grandparent = parent.parentElement;
                    grandparent.removeChild(parent);
                }
            } else {
                alert("Something went wrong");
            }
        })
        .catch(err => console.log(err));
}

function handleClick() {
    document.getElementById('personModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('personModal').style.display = 'none';
}

/**
 * @param {Event} event 
 */
window.onclick = function (event) {
    let modal = document.getElementById('personModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Handle form submission
document.getElementById('addPersonForm').addEventListener('submit', function (event) {
    event.preventDefault();
    // Collect form data
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const age = document.getElementById('age').value;
    const workplace = document.getElementById('workplace').value;
    const address = document.getElementById('address').value;

    // send put request with person object in body
    fetch("/add", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            firstName,
            lastName,
            age,
            workplace,
            address
        })
    }).then(res => {
        if (res.status === 200) {
            // Add new person to the DOM
            res.json().then(id => {
                // Create new person div
                const newPerson = document.createElement('div');
                newPerson.className = "person";
                newPerson.onclick = function () {
                    handlePersonClick(this, id);
                };

                // Create new person name h3
                const newPersonName = document.createElement('h3');
                newPersonName.innerHTML = `${firstName} ${lastName}`;

                // Create new person age p
                const newPersonAge = document.createElement('p');
                newPersonAge.innerHTML = `Age: ${age}`;

                // Create new person address p
                const newPersonAddress = document.createElement('p');
                newPersonAddress.innerHTML = `Address: ${workplace}`;

                // Create new person workplace div
                const newPersonWorkplace = document.createElement('p');
                newPersonWorkplace.innerHTML = `Workplace: ${address}`;

                // Append all new divs to the new person div
                newPerson.appendChild(newPersonName);
                newPerson.appendChild(newPersonAge);
                newPerson.appendChild(newPersonAddress);
                newPerson.appendChild(newPersonWorkplace);

                // Get the tableContainer div
                const people = document.getElementById('tableContainer');

                // get the last child of the tableContainer div
                let parent = people.children[people.children.length - 1];

                // check if parent has 3 children. If it does, create a new one, otherwise use the existing one
                if (parent.childElementCount === 3) {
                    parent = document.createElement('div');
                    parent.className = "container";
                    people.appendChild(parent);
                }

                // Append new person div to the parent div
                parent.appendChild(newPerson);
            });
        } else {
            alert("Something went wrong");
        }
    })
        .catch(err => console.log(err));

    closeModal();
});