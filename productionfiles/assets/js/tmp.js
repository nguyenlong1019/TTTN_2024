if (marineLogCoordinates.length == 1) {
    // Chỉ có 1 vị trí
    let singleMarker = new google.maps.Marker({
        position: marineLogCoordinates[0],
        map: map,
        title: `Vị trí tàu ${info.SoDangKy} ngày ${locationData[0].Ngay}`,
        icon: {
            url: '/static/assets/imgs/fishing-boat-resize.png',
        },
    });
} else if (marineLogCoordinates.length == 2) {
    // Có 2 vị trí
    // Vị trí đầu
    new google.maps.Marker({
        position: marineLogCoordinates[0],
        map: map,
        title: `Vị trí ban đầu của tàu ${info.SoDangKy}`,
        icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
    });
    // Vị trí cuối
    new google.maps.Marker({
        position: marineLogCoordinates[1],
        map: map,
        title: `Vị trí cuối của tàu ${info.SoDangKy}`,
        icon: {
            url: '/static/assets/imgs/fishing-boat-resize.png',
        },
    });
} else if (marineLogCoordinates.length > 2) {
    // Có nhiều hơn 2 vị trí
    // Vị trí đầu
    new google.maps.Marker({
        position: marineLogCoordinates[0],
        map: map,
        title: `Vị trí ban đầu của tàu ${info.SoDangKy}`,
        icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
    });

    // Các vị trí giữa
    for (let i = 1; i < marineLogCoordinates.length - 1; i++) {
        new google.maps.Marker({
            position: marineLogCoordinates[i],
            map: map,
            title: `Vị trí trung gian của tàu ${info.SoDangKy}`,
            icon: {
                url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png', // Sử dụng dấu chấm màu khác cho các điểm trung gian
                scaledSize: new google.maps.Size(4, 4),
            },
        });
    }

    // Vị trí cuối
    new google.maps.Marker({
        position: marineLogCoordinates[marineLogCoordinates.length - 1],
        map: map,
        title: `Vị trí cuối cùng của tàu ${info.SoDangKy}`,
        icon: {
            url: '/static/assets/imgs/fishing-boat-resize.png',
        },
    });
}