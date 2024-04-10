// console.log("Hello world!");

const modalBtns = [...document.querySelectorAll('.modal-button')];
const overlayElem = document.querySelector('.overlay');
const modalElem = document.querySelector('.modal');
const modalBody = document.getElementById('modal-body');
const modalTitle = document.getElementById('modal-title')
const cancelModalBtn = document.getElementById('cancel-modal');
const submitModalBtn = document.getElementById('submit-modal');

const resetSearchBtn = document.getElementById('reset-search-device');

const urlOrigin = window.location.origin;
// console.log(urlOrigin);

overlayElem.addEventListener('click', () => {
    overlayElem.style.display = 'none';
    modalElem.classList.remove('show-modal');
});

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const closeModalBtn = document.querySelector('.btn-close');

    overlayElem.style.display = 'block';
    modalElem.classList.add('show-modal');

    const pk = modalBtn.getAttribute('data-pk');
    const command = modalBtn.getAttribute('data-command');
    const title = modalBtn.getAttribute('data-comfirm'); // xác nhận xóa tàu hoặc xem vị trí tàu nào?
    if (command === 'location') {
        modalBody.style.display = 'block';
        cancelModalBtn.style.display = 'none';
        submitModalBtn.innerHTML = 'Xong'

        let locationUrlApi = urlOrigin + `/api/device-location/${pk}/`;
        fetch(locationUrlApi)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok!');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            let isSuccess = data.success;
            // console.log(isSuccess);
            if (isSuccess) {
                modalTitle.innerHTML = `Thông tin vị trí tàu ${title}`;
                const bundle = data.bundle;
                modalBody.innerHTML = `
                    <p class="fs-6">Chủ tàu: <b>${bundle.shipowner}</b></p>
                    <p class="fs-6">Thuyền thưởng: <b>${bundle.captain}</b></p>
                    <p class="fs-6">Vĩ độ: <b>${bundle.lat}</b></p>
                    <p class="fs-6">Kinh độ: <b>${bundle.lng}</b></p>
                    <p class="fs-6">Thời gian cập nhật: <b>${bundle.date}</b> </p>
                `;
            } else {
                modalTitle.innerHTML = `Chưa có thông tin vị trí tàu ${title}`;
                modalBody.innerHTML = `
                    <p class="fs-6">Đảm bảo rằng thiết bị giám sát đang hoạt động trên tàu</p>
                `;
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
        submitModalBtn.setAttribute('data-command', 'location');
    } else if (command === 'trash') {
        modalTitle.innerHTML = `Xác nhận xóa thông tin tàu ${title}?`;
        modalBody.style.display = 'none';
        cancelModalBtn.style.display = 'initial';
        submitModalBtn.innerHTML = 'Xác nhận'
        submitModalBtn.setAttribute('data-command', 'trash');
    }
    
    closeModalBtn.addEventListener('click', () => {
        overlayElem.style.display = 'none';
        modalElem.classList.remove('show-modal');
    });

    cancelModalBtn.addEventListener('click', () => {
        overlayElem.style.display = 'none';
        modalElem.classList.remove('show-modal');
    });

    submitModalBtn.addEventListener('click', () => {
        let commandSubmit = submitModalBtn.getAttribute('data-command');
        if (commandSubmit === 'trash') {
            window.location.href = urlOrigin + `/device/delete-device/${pk}/`;
        } else {
            overlayElem.style.display = 'none';
            modalElem.classList.remove('show-modal');
        }
    });
}));

resetSearchBtn.addEventListener('click', () => {
    document.getElementById('input-search-device').value = '';
});

const selectQtyRecordElem = document.getElementById('select-record-number');
selectQtyRecordElem.addEventListener('change', () => {
    let selectedIndex = selectQtyRecordElem.selectedIndex;
    let selectedOption = selectQtyRecordElem.options[selectedIndex];
    let selectedValue = selectedOption.value;
    // console.log(selectedValue);

    let newUrl = "{% url 'download-device-data' 0 %}".replace('0', selectedValue);
    document.getElementById('download-excel-data').href = newUrl;
});
