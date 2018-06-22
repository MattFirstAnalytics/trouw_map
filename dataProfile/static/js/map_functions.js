var map = L.map('map').setView([37.8, -96], 4);
var selected_region = '';

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.light'
}).addTo(map);


// control that shows state info on hover
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function (props) {
    this._div.innerHTML = (props ? '<h4>Sales Purchased by BEA</h4><b>BEA Name: ' + props.name + '<br/><b>Volume: ' + props.density :
        '<h4>Sales Purched by BEA</h4><b>BEA Name:   </br><b>Volume:');
};

info.addTo(map);


mv = 0;
lv = 100000;
for (var i = 0; i < statesData["features"].length; i++) {
    if (statesData["features"][i]["properties"]["density"] > mv) {
        mv = statesData["features"][i]["properties"]["density"];
    };
    if (statesData["features"][i]["properties"]["density"] != '' && statesData["features"][i]["properties"]["density"] < lv) {
        lv = statesData["features"][i]["properties"]["density"];
    };

};


console.log(mv);
console.log(lv);
color_scale = d3.scaleLog()
    .domain([lv, mv])
    .range(["#055faa", "#c1182b"]);


function style(feature) {
    return {
        weight: 1,
        opacity: 0.5,
        color: color_scale(feature.properties.density),
        // dashArray: '3',
        fillOpacity: 0.5,
        fillColor: color_scale(feature.properties.density)
    };
}


function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 1,
        // color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }

    info.update(layer.feature.properties);
}

var geojson;

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function clickEvent(e) {
    // map.fitBounds(e.target.getBounds());
    selected_region = e.target.feature.properties.name;
}

function update_base(e) {

}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: clickEvent
    });
}

geojson = L.geoJson(statesData, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);

map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');


var legend = L.control({
    position: 'bottomright'
});

// legend.onAdd = function (map) {

//     var div = L.DomUtil.create('div', 'info legend'),
//         grades = [0, 10, 20, 50, 100, 200, 500, 1000],
//         labels = [],
//         from, to;

//     for (var i = 0; i < grades.length; i++) {
//         from = grades[i];
//         to = grades[i + 1];

//         labels.push(
//             '<i style="background:' + getColor(from + 1) + '"></i> ' +
//             from + (to ? '&ndash;' + to : '+'));
//     }

//     div.innerHTML = labels.join('<br>');
//     return div;
// };

legend.addTo(map);


// function for toggeling the areas on and off
function flip(what_button){
    console.log(what_button);
    var position = document.getElementById(what_button).checked;
    console.log(position);
    if (position) {
        var opacity_level = 0.5;
    } else {
        var opacity_level = 0.0;
    };

    map.eachLayer(function(layer) {
        try {
            if (layer.feature.properties.type == what_button){
                layer.setStyle({fillOpacity: opacity_level});
                if (opacity_level == 0.5){
                    layer.setStyle({weight: opacity_level + 0.5});
                } else {
                    layer.setStyle({weight: opacity_level});
                }
            };
        } catch (err) {}
    });
};