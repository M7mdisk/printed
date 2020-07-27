function Init(arg) {

    //Initialise Map
    var mymap = L.map('mapid').setView([29.338788, 48.022319], 12);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors' +
            '',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap);
    //locate User
    var uexits = false
    var umarker;
    var redIcon = new L.Icon({
        iconUrl: 'static/img/marker-icon-2x-red.png',
        shadowUrl: 'static/img/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
        watch: true
    });
    var greenIcon = new L.Icon({
      iconUrl: 'static/img/marker-icon-2x-green.png',
      shadowUrl: 'static/img//marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });

    mymap.locate({
        setView: true,
        maxZoom: 120,
        watch: true,
        enableHighAccuracy: true
    }).on("locationfound", e => {
        if (!umarker) {
            umarker = new L.marker(e.latlng, {
                icon: redIcon,
            });
            uexits = true;
            umarker.addTo(mymap);
        } else {
            umarker.setLatLng(e.latlng);
        }
    }).on("locationerror", error => {
        if (umarker) {
            mymap.removeLayer(umarker);
            umarker = undefined;
        }
    });
    //displaying all Libraries near user
    let a = arg;
    console.log(a)
    var locations = [];
    var blueIcon = new L.Icon({
        iconUrl: '/static/img/marker-icon-2x-blue.png',
        shadowUrl: '/static/img/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    for (var i = a.length - 1; i >= 0; i--) {
        let str = a[i]['fields']['location'];
        var substr = str.substring(
            str.lastIndexOf("(") + 1,
            str.lastIndexOf(")")
        );

        longt = parseFloat(substr.split(' ')[0])
        latt = parseFloat(substr.split(' ')[1])
        var marker = L.marker([latt, longt],{icon: blueIcon}).addTo(mymap);
        marker.bindPopup(" <div style='text-align:center; font-size: 1.1em;'> <b>" + (a[i]['fields']['name']) + '</b><br>' + (a[i]['fields']['city']) + '<br> <button class="btn-sm btn-primary" style="font-size:0.99em !important ;" name="shop" type="submit" value="'+ a[i]['fields']['name'] +'">Select Shop</button></div>')
        locations.push(marker);
    }
    function checkFlag() {
        if (uexits == false) {
            window.setTimeout(checkFlag, 10); /* this checks the flag every 100 milliseconds*/
        } else {
            umarker.bindPopup('Your Location').openPopup();
            var nearest;
            var sdistance = Infinity;
            for (var i = locations.length - 1; i >= 0; i--) {
                if(mymap.distance(locations[i].getLatLng(), umarker.getLatLng()) < sdistance)
                {
                    sdistance = mymap.distance(locations[i].getLatLng(), umarker.getLatLng());
                    nearest=locations[i];

                }
            }
            nearest.setIcon(greenIcon);
            nearest.openPopup();
            console.log(locations[0].getPopup().getContent())
            var latlngs = Array();
            latlngs.push(nearest.getLatLng());
            latlngs.push(umarker.getLatLng());
            //var polyline = L.polyline(latlngs, {color: 'green'}).addTo(mymap);
        }
    }
    checkFlag();
}

function choosethis(thiss) {
    console.log(thiss.children[0].innerHTML);
}