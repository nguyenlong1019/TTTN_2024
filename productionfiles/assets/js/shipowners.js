// console.log("Hello Shipowners!!");
const urlOrigin = window.location.origin;

const resetSearchInputBtn = document.getElementById('reset-search-shipowners');
resetSearchInputBtn.addEventListener('click', () => {
    document.getElementById('input-search-shipowners').value = '';
});

const editShipownerBtns = document.querySelectorAll('.edit-shipowner-btn');
editShipownerBtns.forEach(editShipownerBtn => {
    editShipownerBtn.addEventListener('click', () => {
        const pk = editShipownerBtn.getAttribute('data-pk');
        const userType = editShipownerBtn.getAttribute('data-user-type');
        window.location.href = urlOrigin + `/shipowners/edit-shipowner/${pk}&${userType}/`;
    });
});

const modalBtns = [...document.querySelectorAll('.modal-button')];
const overlayElem = document.querySelector('.overlay');
const modalElem = document.querySelector('.modal');
const modalBody = document.getElementById('modal-body');
const modalTitle = document.getElementById('modal-title')
const cancelModalBtn = document.getElementById('cancel-modal');
const submitModalBtn = document.getElementById('submit-modal');

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const closeModalBtn = document.querySelector('.btn-close');
    overlayElem.style.display = 'block';
    modalElem.classList.add('show-modal');

    const pk = modalBtn.getAttribute('data-pk');
    const userType = modalBtn.getAttribute('data-user-type');
    const fullName = modalBtn.getAttribute('data-fullname');
    const identification = modalBtn.getAttribute('data-identification');
    if (userType == 'captain') {
        modalTitle.innerHTML = `Xác nhận xóa thông tin thuyền trưởng ${fullName} - CMND (CCCD): ${identification}?`;
    } else if (userType == 'shipowner') {
        modalTitle.innerHTML = `Xác nhận xóa thông tin chủ tàu ${fullName} - CMND (CCCD): ${identification}?`;
    } else {
        console.log("Error: user type không hợp lệ!");
    }

    modalBody.innerHTML = `
        <strong>Lưu ý</strong>:
        <ul>
            <li>Xóa thông tin người dùng cũng sẽ không ảnh hưởng thông tin liên quan đến tàu do thuyền trưởng hoặc chủ tàu có liên quan</li>
            <li>Nếu muốn xóa thông tin tàu liên quan vui lòng đến trang quản lý tàu</li>
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
        overlayElem.style.display = 'none';
        modalElem.classList.remove('show-modal');

        // xử lý logic xóa thông tin ở đây

        // kiểm tra xem chủ tàu hoặc thuyền trưởng có liên kết đến tàu hay không?
        // nếu có set tại tàu là null
        // sau đó thực hiện xóa
    });
}));