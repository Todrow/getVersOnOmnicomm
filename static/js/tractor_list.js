// Получаем данные по тракторам из Django
const tractors_info_response = JSON.parse(document.getElementById('tractors_info_response').textContent);
// Получаем данные по компонентам из Django
const components_response = JSON.parse(document.getElementById('components_response').textContent);
// console.log(tractors_info_response)
// console.log(components_response)
// Таблица
const table = document.getElementsByClassName('tractor_list_table')[0];
const tbody = document.getElementsByClassName('tractor_list_tbody')[0];

// console.log(tractors_info_response);

for (let tractor of tractors_info_response) {
    const tr = document.createElement('tr');
    for (let i = 1; i < 3; i++) {
        let td = document.createElement('td');
        td_data = Object.values(tractor)[i];
        td.textContent = td_data
        tr.appendChild(td);
    }
    
    for (let i = 0; i < 6; i++) {
        let td = document.createElement('td');
        designation = tractor['components'][i]['designation_comp'];
        td.textContent = designation;
        tr.appendChild(td);
        td = document.createElement('td');
        version = tractor['components'][i]['version'];
        td.textContent = version;
        td.classList.add(tractor['components'][i]['status']);
        td.dataset.color = tractor['components'][i]['status'];
        tr.appendChild(td);
    }
    tbody.appendChild(tr);
}
