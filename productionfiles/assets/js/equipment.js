// console.log("Hello World Equipment");

const resetEquipmentBtn = document.getElementById('reset-equipments-btn');
resetEquipmentBtn.addEventListener('click', () => {
    document.getElementById('search-equipment-input').value = '';
});

const modalBtns = document.querySelectorAll('.modal-button');
const overlayElem = document.querySelector('.overlay');
const modalElem = document.querySelector('.modal');
const modalBody = document.querySelector('.modal-body');
const modalTitle = document.querySelector('.modal-title');
const cancelModalBtn = document.getElementById('cancel-modal');
const submitModalBtn = document.getElementById('submit-modal');

const urlOrigin = window.location.origin;

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    // console.log("Clicked");
    const closeModalBtn = document.querySelector('.btn-close');

    overlayElem.style.display = 'block';
    modalElem.classList.add('show-modal');

    const pk = modalBtn.getAttribute('data-pk');
    const serialNumber = modalBtn.getAttribute('data-serial-number');
    console.log(pk);
    console.log(serialNumber);

    modalTitle.innerHTML = `Xác nhận xóa thiết bị ${serialNumber} ?`;
    modalBody.innerHTML =  `
        <strong>Lưu ý:</strong>
        <ul>
            <li>Chỉ xóa các thiết bị chưa được kích hoạt</li>
            <li>Xóa thiết bị đã kích hoạt sẽ ảnh hưởng đến thông tin tàu, nên cần thay đổi phía thiết bị trên tàu trước khi xóa</li>
            <li>Đối với thiết bị đã kích hoạt cần thay đổi phía tàu trước khi xóa</li>
        </ul>
    `;

    closeModalBtn.addEventListener('click', () => {
        overlayElem.style.display = 'none';
        modalElem.classList.remove('show-modal');
    });

    cancelModalBtn.addEventListener('click', () => {
        overlayElem.style.display = 'none';
        modalElem.classList.remove('show-modal');
    });

    submitModalBtn.addEventListener('click', () => {
        window.location.href = urlOrigin + `/equipment/delete/${pk}/`;
    });
}));