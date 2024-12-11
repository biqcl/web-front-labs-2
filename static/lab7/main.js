function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;
                
            let titleElement = document.createElement('i');
            titleElement.style.color = '#e0b8c2';
            titleElement.innerText = films[i].title;
            tdTitle.appendChild(titleElement);

            tdYear.innerText = films [i].year;

            let editButton = document.createElement('button');
            editButton.innerText = "редактировать";
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = "удалить"; 
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru); 
            };

            tdActions.append(editButton); 
            tdActions.append(delButton); 

            tr.append(tdTitleRus);
            tr.append(tdTitle);            
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'}) 
        .then(function () {
            fillFilmList();
        })   
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block'; 
    document.getElementById('title_ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';        
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';   
}
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;

    const film = {
        title_ru: document.getElementById('title_ru').value,
        title: document.getElementById('title').value || "",        
        year: parseInt(document.getElementById('year').value),
        description: document.getElementById('description').value 
    }

    const url = `/lab7/rest-api/films/${id}/`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return{};
        }        
        return resp.json();
    })
    .then(function(errors) {
        for (const key in errors) {
            const errorElement = document.getElementById(`${key}-error`);
            if (errorElement) {
                errorElement.innerText = errors[key];
            }
        }
    })
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    })
}
 