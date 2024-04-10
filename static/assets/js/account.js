// console.log("Hello World!");

const resetInputBtn = document.getElementById('reset-accout-input');
resetInputBtn.addEventListener('click', () => {
    document.getElementById('account-search-input').value = '';
});


const modalBtns = document.querySelectorAll('.modal-button');
const overlayElem = document.querySelector('.overlay');
const modalElem = document.querySelector('.modal');
const modalBody = document.getElementById('modal-body');
const modalTitle = document.getElementById('modal-title')
const cancelModalBtn = document.getElementById('cancel-modal');
const submitModalBtn = document.getElementById('submit-modal');

const urlOrigin = window.location.origin;

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const closeModalBtn = document.querySelector('.btn-close');

    overlayElem.style.display = 'block';
    modalElem.classList.add('show-modal');

    const pk = modalBtn.getAttribute('data-pk');
    const username = modalBtn.getAttribute('data-username');
    const email = modalBtn.getAttribute('data-email');
    console.log(email);

    modalTitle.innerHTML = `Xác nhận xóa thông tin user: ${username} ?`;
    modalBody.innerHTML =  `
        <strong>Lưu ý: </strong>
        <ul>
            <li>Xác nhận xóa user với username: ${username}</li>
            <li>Xác nhận xóa user với email: ${email ? email : 'Không có email'}</li>
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
        window.location.href = urlOrigin + `/account/delete/${pk}/`;
    });
}));
