function Init(arg) {
	//Initialise Map
    var mymap = L.map('mapid').setView([29.338788, 48.022319], 12);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery ? <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap);
    //locate User
    function onLocationFound(e) {
        var radius = e.accuracy / 2;
        var redIcon = new L.Icon({
            iconUrl: 'static/img/marker-icon-2x-red.png',
            shadowUrl: 'static/img/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
            watch: true
        });
        L.marker(e.latlng, {icon: redIcon}).addTo(mymap).bindPopup("You are within " + radius + " meters from this point").openPopup();
    	L.circle(e.latlng, radius).addTo(mymap);
    }

    function onLocationError(e) {
        alert(e.message);
    }
    mymap.on('locationfound', onLocationFound);
    mymap.on('locationerror', onLocationError);
    mymap.locate({
        setView: true,
        maxZoom: 13
    });
    //displaying all Libraries near user
    let a = arg;
    console.log(a)
    var locations=[];
    for (var i = a.length - 1; i >= 0; i--) {
        let str = a[i]['fields']['location'];
        var substr = str.substring(
            str.lastIndexOf("(") + 1,
            str.lastIndexOf(")")
        );
        longt = parseFloat(substr.split(' ')[0])
        latt = parseFloat(substr.split(' ')[1])
        var marker = L.marker([latt, longt]).addTo(mymap);
        marker.bindPopup("<b>" + (a[i]['fields']['name']) + '</b><br>'+ (a[i]['fields']['city'])+'<br><input type="submit" value="choose this one" onclick="choosethis(this.parentElement)">').openPopup();
        locations.push(marker)
    }
    console.log(locations)
    var latlngs = Array();
    latlngs.push(locations[0].getLatLng());
    latlngs.push(ulatlong);
    var polyline = L.polyline(latlngs, {color: 'red'}).addTo(mymap);
    mymap.fitBounds(polyline.getBounds());
}

function choosethis(thiss){
    console.log(thiss.children[0].innerHTML);
}
