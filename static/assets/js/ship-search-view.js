// let markers = [
//     { position: {lat: 13.884421, lng: 110.028847}, title: 'Tàu 1', content: 'Tàu 1' },
//     { position: {lat: 12.605872, lng: 111.199578}, title: 'Tàu 2', content: 'Tàu 2' }, 
// ]

const selectShip = document.getElementById('select-ship');
const focusInput = document.getElementsByName('flexRadioDefault');
const shipInfoBox = document.getElementById('search-info');

function initMap() {
    let map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 13.678354, lng: 111.400118}, // tọa độ trung tâm
        zoom: 15, // zoom max là 22
    });

    // thêm polyline
    let flightPlanCoordinates = [
        {lat: 21.532618, lng: 108.056009},
        {lat: 20.4017, lng: 108.3792},
        {lat: 19.9583, lng: 107.93},
        {lat: 19.6583, lng: 107.5283},
        {lat: 19.4233, lng: 107.35},
        {lat: 19.4233, lng: 107.2117},
        {lat: 19.2683, lng: 107.19},
        {lat: 19.215, lng: 107.16},
        {lat: 18.715, lng: 107.16},
        {lat: 18.23, lng: 107.5667},
        {lat: 18.1183, lng: 107.6267},
        {lat: 18.07, lng: 107.6517},
        {lat: 17.7833, lng: 107.9667},
        {lat: 17.3317, lng: 108.5572},
        {lat: 16.7817, lng: 109.4958},
        {lat: 16.4481, lng: 110.9795},
        {lat: 17.4598, lng: 111.2896},
        {lat: 17.5515, lng: 111.3583},
        {lat: 17.6065, lng: 111.4434},
        {lat: 17.6274, lng: 111.5286},
        {lat: 17.6274, lng: 111.6192},
        {lat: 17.5515, lng: 112.1438},
        {lat: 17.5017, lng: 112.4322},
        {lat: 17.3524, lng: 112.7453},
        {lat: 17.2212, lng: 112.9486},
        {lat: 17.1517, lng: 112.9843},
        {lat: 17.0822, lng: 112.9815},
        {lat: 17.4329, lng: 113.5533},
        {lat: 18.5129, lng: 114.6131},
        {lat: 18.9288, lng: 116.1876},
        {lat: 19.743, lng: 117.6259},
        {lat: 18.6421, lng: 117.4442},
        {lat: 17.8225, lng: 116.99},
        {lat: 16.2592, lng: 116.5207},
        {lat: 13.8618, lng: 116.8083},
        {lat: 13.8471, lng: 116.8235},
        {lat: 12.6799, lng: 116.4964},
        {lat: 11.93, lng: 115.7554},
        {lat: 12.1166, lng: 116.7854},
        {lat: 11.118, lng: 117.8153},
        {lat: 10.3488, lng: 117.9698},
        {lat: 9.0, lng: 115.9814},
        {lat: 7.66, lng: 115.7554},
        {lat: 6.74, lng: 113.6954},
        {lat: 7.6634, lng: 112.5625},
        {lat: 6.262, lng: 111.0175},
        {lat: 6.8375, lng: 109.2869},
        {lat: 6.35, lng: 106.6605},
        {lat: 6.25, lng: 106.3169},
        {lat: 6.25, lng: 106.2},
        {lat: 6.0967, lng: 105.82},
        {lat: 7.05, lng: 103.8667},
        {lat: 7.3052, lng: 103.5953},
        {lat: 7.5667, lng: 103.3167},
        {lat: 7.7, lng: 102.9667},
        {lat: 7.7122, lng: 102.9512},
        {lat: 7.8167, lng: 103.0417},
        {lat: 8.7819, lng: 102.2032},
        {lat: 9.5834, lng: 103.1711},
        {lat: 9.9167, lng: 102.8917},
        {lat: 9.9033, lng: 102.92},
        {lat: 9.9083, lng: 102.95},
        {lat: 10.4017, lng: 103.8},
        {lat: 10.4267, lng: 103.82},
        {lat: 10.5, lng: 103.79},
        {lat: 10.54, lng: 103.8033},
    ];

    let flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true, // đường nét liền
        strokeColor: '#0B60B0',
        strokeOpacity: 1.0,
        strokeWeight: 2,
    });

    flightPath.setMap(map);

    let pk = selectShip.getAttribute('data-pk');
    let startDate = document.getElementById('start-date').value;
    let endDate = document.getElementById('end-date').value;
    let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const requestData = {
        'pk': pk,
        'startDate': startDate,
        'endDate': endDate,
    }
    // console.log("Start");
    fetch(`/api/get-marine-log/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Có lỗi khi lấy dữ liệu!!');
        }
        return response.json();
    })
    .then(data => {
        let info = data.info;
        shipInfoBox.innerHTML = `
            <p>Thông tin tìm được</p>
            <div>
                <p>Tàu cá: <strong>${info.SoDangKy}</strong><br></p>
                <p>Lat: <strong>${info.ViDo}</strong></p>
                <p>Lng: <strong>${info.KinhDo}</strong></p>
                <p>Date: <strong>${info.Ngay}</strong></p>
            </div>
        `;

        map.setCenter({lat: parseFloat(info.ViDo), lng: parseFloat(info.KinhDo)});

        let marineLogCoordinates = [];
        let locationData = data.location;

        for (let i = 0; i < locationData.length; i++)
        {
            let position = {lat: parseFloat(locationData[i].ViDo), lng: parseFloat(locationData[i].KinhDo)};
            marineLogCoordinates.push(position);
        }

        let marineLogLine = new google.maps.Polyline({
            path: marineLogCoordinates,
            geodesic: true, // đường nét liền
            strokeColor: '#ffffff',
            strokeOpacity: 1.0,
            strokeWeight: 4,
        });

        marineLogLine.setMap(map);

        let markers = [];

        if (marineLogCoordinates.length > 0) {
            let lastPosition = marineLogCoordinates[marineLogCoordinates.length - 1];
            let lastMarker = new google.maps.Marker({
                position: lastPosition,
                map: map,
                title: `Vị trí tàu ${info.SoDangKy} ngày ${info.Ngay}`,
                icon: {
                    url: '/static/assets/imgs/fishing-boat-resize.png',  // sau nên trả url về từ server
                },
            });

            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <div class="p-3">
                        <h3 class="fs-5">Vị trí tàu cá ${info.SoDangKy}</h3>
                        <p class="fs-6"><strong>Thông tin:</strong> </p>
                        <p class="fs-6">Tàu cá: ${info.SoDangKy}</p>
                        <p class="fs-6">Chủ tàu: ${info.ChuTau}</p>
                        <p class="fs-6">Thuyền trưởng: ${info.ThuyenTruong}</p>
                        <p class="fs-6">Kinh độ: ${info.KinhDo}</p>
                        <p class="fs-6">Vĩ độ: ${info.ViDo}</p>
                        <p class="fs-6">Ngày cập nhật: ${info.Ngay}</p>
                    </div>
                `
            });

            lastMarker.addListener('click', () => {
                infoWindow.open(map, lastMarker);
            });
        }


        if (marineLogCoordinates.length >= 2) {
            let firstPosition = marineLogCoordinates[0];
            let firstMarker = new google.maps.Marker({
                position: firstPosition,
                map: map,
                title: `Vị trí tàu ${info.SoDangKy} ngày ${locationData[0].Ngay}`,
            });
            markers.push(firstMarker);
        }

        if (marineLogCoordinates.length >= 3)
        {
            for (let i = 1; i < marineLogCoordinates.length - 1; i++) {
                let marker = new google.maps.Marker({
                    position: marineLogCoordinates[i],
                    map: map,
                    title: `Vị trì tàu ${info.SoDangKy} ngày ${locationData[i].Ngay}`,
                    icon: {
                        url: '/static/assets/imgs/dot.png',
                        scaledSize: new google.maps.Size(5, 5),
                    }
                });
                markers.push(marker);
            }
        }

        


    })
    .catch(error => {
        console.error('There was a problem  with your fetch  operation: ', error);
    });
}