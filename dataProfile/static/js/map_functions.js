// global variables
var map = L.map('map').setView([37.8, -96], 5);
var legend = L.control({position: 'bottomright'});
var info = L.control();

// parameters
var color_low = "#3f79a6";
var color_high = "#e91129";
var opacity_low = 0.7;
var opacity_high = 0.9;

function run_map(map_data){

    // clears the map of anything
    map.eachLayer(function (layer) {
        map.removeLayer(layer);
    });

    legend.remove();
    info.remove();    


    var selected_region = '';

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.light'
    }).addTo(map);


    // control that shows state info on hover
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    };

    info.update = function (props) {
        this._div.innerHTML = (props ? '<h4>Sales by BEA</h4><b>BEA Name: ' + props.name + '<br/><b>Volume: ' + props.density + ' MT':
            '<h4>Sales by BEA</h4><b>BEA Name:   </br><b>Volume:');
    };

    info.addTo(map);


    mv = 0;
    lv = 100000;
    for (var i = 0; i < map_data["features"].length; i++) {
        if (map_data["features"][i]["properties"]["density"] > mv) {
            mv = map_data["features"][i]["properties"]["density"];
        };
        if (map_data["features"][i]["properties"]["density"] != '' && map_data["features"][i]["properties"]["density"] < lv) {
            lv = map_data["features"][i]["properties"]["density"];
        };

    };



    color_scale = d3.scaleLog()
        .domain([lv, mv])
        .range([color_low, color_high]);

    // color_scale = d3.scaleLinear()
    //     .domain([lv, mv])
    //     .range([color_low, color_high]);

    function density_check(density){
        if(density == 0){
            return(0);
        } else{
            return(opacity_low);
        };
    };

    function style(feature) {
        return {
            weight: 1,
            opacity: density_check(feature.properties.density),
            color: color_scale(feature.properties.density),
            // dashArray: '3',
            fillOpacity: density_check(feature.properties.density),
            fillColor: color_scale(feature.properties.density)
        };
    }


    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 1,
            dashArray: '',
            fillOpacity: opacity_high
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

    geojson = L.geoJson(map_data, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);

    map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [mv, lv + 3 * (mv - lv)/5, lv + 2 * (mv - lv)/5, lv + (mv - lv)/5,  lv],
            labels = [],
            from, to;

        for (var i = 0; i < grades.length; i++) {
            from = parseInt(grades[i]);
            to = grades[i + 1];

            labels.push(
                '<i style="background:' + color_scale(from + 1) + '"></i> ' + from);

            // labels.push(
            //     '<i style="background:' + color_scale(from + 1) + '"></i> ' +
            //     from + (to ? '&ndash;' + to : '+'));
        }

        div.innerHTML = labels.join('<br>');
        return div;
    };

    legend.addTo(map);

};

    // function for toggeling the areas on and off
    function flip(what_button){
        var position = document.getElementById(what_button).checked;
        if (position) {
            var opacity_level = opacity_low;
        } else {
            var opacity_level = 0.0;
        };

        map.eachLayer(function(layer) {
            try {
                if (layer.feature.properties.type == what_button){
                    layer.setStyle({fillOpacity: opacity_level});
                    if (opacity_level == opacity_low){
                        layer.setStyle({weight: opacity_level + opacity_low});
                    } else {
                        layer.setStyle({weight: opacity_level});
                    }
                };
            } catch (err) {}
        });
    };