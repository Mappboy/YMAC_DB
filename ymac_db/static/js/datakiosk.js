var token = "91e61ba3c8b7101ddf7a6ee8a0ddc935acd77089";
var server = "ymac-dc3-app1:8080";
var formFields = [];
var outputOptions = [];
var tableData = {};
var currentRepo = {};
var outputRequest = "";
var layer, map;
var download = false;
var googleEarthData = "";
var infowindow;

//TODO Include token string and custom request or write XMLHTTPRequester
//TODO we need to get OUTPUT OR OUTPUTFORMAT and hide it unless. OUTPUT=DOWNLOAD
function processForm() {
    var repository = document.getElementById("repository-name").value;
    var workspace = document.getElementById("workspace-name").value;

    // Get the workspace parameters from FME Server
    FMEServer.getWorkspaceParameters(repository, workspace, generateForm);
}

function showTableResults(json) {
    // The following is to write out the full return object
    // for visualization of the example
    //We don't care for this stuff
    json.forEach(function (el, i) {
        delete el.json_featuretype;
        delete el.json_geometry;
        delete el.json_ogc_wkt_crs;
    });
    var headers = {};
    data = JSON.stringify(json, undefined, 4);
    tableData = data;
    console.log(data);
    //TODO Update the table and add info for hover
    //Create results table
    $('#results').html('<div class="row"><table id="results_table" class="table table-striped hover"><thead><tr id="result_head"></tr></thead><tbody></tbody></table></div>');
    for (var heading in json[0]) {
        $("#result_head").append('<th>' + heading + '</th>');
    }
    /*$('#results').html("<table class=\"table\" id=\"tentable\"> \
     <thead> \
     <th data-dynatable-column=\"tenementid\">Tenement ID</th> \
     <th data-dynatable-column=\"all_holder\">Tenement Holder</th> \
     <th data-dynatable-column=\"tenstatus\">Status</th> \
     <th data-dynatable-column=\"name\" >Full Claim name</th> \
     <th data-dynatable-column=\"ymacregion\">Region</th> \
     <th data-dynatable-column=\"claimgroup\">Claim Group</th> \
     <th data-dynatable-column=\"anthro\">Anthropologist</th> \
     <th data-dynatable-column=\"hs_officer\">Heritage Survey Officer</th> \
     <th data-dynatable-column=\"lawyer\">Lawyer</th> \
     </thead> \
     <tbody> \
     </tbody> \
     </table>");*/

    $('#results_table').dynatable({
        dataset: {
            records: json
        },
        table: {
            defaultColumnIdStyle: 'lowercase'
        }
    });
}
function showMapResults(json) {
    // The following is to write out the full return object
    // for visualization of the example
    data = json; //JSON.stringify(json, undefined, 4);
    console.log(data);
}

/**
 * Process each point in a Geometry, regardless of how deep the points may lie.
 * @param {google.maps.Data.Geometry} geometry The structure to process
 * @param {function(google.maps.LatLng)} callback A function to call on each
 *     LatLng point encountered (e.g. Array.push)
 * @param {Object} thisArg The value of 'this' as provided to 'callback' (e.g.
 *     myArray)
 */
function processPoints(geometry, callback, thisArg) {
    if (geometry instanceof google.maps.LatLng) {
        callback.call(thisArg, geometry);
    } else if (geometry instanceof google.maps.Data.Point) {
        callback.call(thisArg, geometry.get());
    } else {
        geometry.getArray().forEach(function (g) {
            processPoints(g, callback, thisArg);
        });
    }
}

/**
 * Update a map's viewport to fit each geometry in a dataset
 * @param {google.maps.Map} map The map to adjust
 */
function zoom(procmap) {
    var bounds = new google.maps.LatLngBounds();
    procmap.data.forEach(function (feature) {
        processPoints(feature.getGeometry(), bounds.extend, bounds);
    });
    procmap.fitBounds(bounds);
}

function showGoogleMapResults(ogckml) {
    // The following is to write out the full return object
    // for visualization of the example
    //NOTE: This is currently not working because it is local
    googleEarthData = ogckml;
    var props = [];
    var add_props = true;
    for (var geojson in ogckml) {
        map.data.addGeoJson(ogckml[geojson]);
        if (add_props) {
            for (var varprop in ogckml[geojson].features[0].properties) {
                props.push(prop);
            }
            add_props = false;
        }
    }
    zoom(map);
    map.data.setStyle({
        fillColor: 'green',
        clickable: true,
    });
    // Set event listener for each feature.
    map.data.addListener('click', function (event) {
        var contentstring = "<h1>" + event.feature.getProperty("tenementid") + "</h1>";
        for (var prop in props) {
            contentstring += "<h5>" + props[prop] + ": </h5>" + event.feature.getProperty(props[prop]);
        }
        infowindow.setContent(contentstring);
        infowindow.setPosition(event.latLng);
        infowindow.setOptions({
            pixelOffset: new google.maps.Size(0, -34)
        });
        infowindow.open(map);
    });
}

function downloadFile(json) {
    // The following is to write out the full return object
    // for visualization of the example
    window.location.href = json.serviceResponse.url; //JSON.stringify(json, undefined, 4);
}

function runDataDownload() {
    var repository = document.getElementById("repo_selector").value;
    var workspace = $("#repository").text();
    var form = $("#output_form");
    var inputs = $(".form-control");
    var checks = $(".checkbox");
    //var params = { "publishedParameters" : [] };
    //var publishedParameters = params.publishedParameters;
    var params = "";
    inputs.each(function (i, el) {
        if (el.id != "repo_selector") {
            //If type = select then add first and iterate over array
            if (el.type == "select-multiple") {
                var name = el.id;
                $('#' + el.id).val().forEach(function (el, i) {
                    params += name + "=" + el + "&";
                });
            } else {
                params += el.id + "=" + el.value + "&";
            }
            // Remove trailing & from string
        }
    });
    checks.each(function (i, c) {
        var checkbox = $(c).find('input');
        if (checkbox.prop("checked")) {
            params += checkbox[0].id + "=True";
        }
    });
    params = params.substr(0, params.length - 1);
    FMEServer.runDataDownload(workspace, repository, params, downloadFile);
}

function runStreamingMap() {
    //IF STREAMING WE SHOULD EITHER SHOW TABLE OF DATA USING JSON
    //OR STREAM TO A GOOGLE MAP OR LEAFLET
    var workspace = document.getElementById("repo_selector").value;
    var repository = $("#repository").text();
    var form = $("#output-form");
    var inputs = $(".form-control");
    var checks = $(".checkbox");
    var params = "";
    inputs.each(function (i, el) {
        if (el.id != "repo_selector") {
            //If type = select then add first and iterate over array
            if (el.type == "select-multiple") {
                alert("Haven't figured out multiples yet.");
            } else if (el.id == "OUTPUT") {
                params += el.id + "=" + outputRequest + "&";
            } else {
                params += el.id + "=" + el.value + "&";
            }
            // Remove trailing & from string
        }
    });
    checks.each(function (i, c) {
        var checkbox = $(c).find('input');
        if (checkbox.prop("checked")) {
            params += checkbox[0].id + "=True";
        }
    });
    params = params.substr(0, params.length - 1);
    if (outputRequest == "GEOJSON") {
        $('#results').html('<div id="map-canvas"></div>');
        var mapStyles = [{
            featureType: "all",
            elementType: "labels",
            stylers: [{
                visibility: "on"
            }
            ]
        }
        ];

        //Zoom to LAYERS
        var mapOptions = {
            zoom: 9,
            center: new google.maps.LatLng(-24.050681, 118.458115),
            mapTypeId: google.maps.MapTypeId.SATELLITE
        };
        map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
        google.maps.event.addListenerOnce(map, 'idle', function () {
            map.setOptions({
                styles: mapStyles
            });
        });
        google.maps.event.addListener(map, 'click', function () {
            infowindow.close();
        });
        infowindow = new google.maps.InfoWindow();
        FMEServer.runDataStreaming(repository, workspace, params, showGoogleMapResults);
        //showGoogleMapResults("http://" + server + "/fmedatastreaming/" + encodeURI( repository + "/" +  workspace+ "?" + params + "&token=" + token))
    }
    //Todo add leaflet geojson
}
function runStreamingTab() {
    //IF STREAMING WE SHOULD EITHER SHOW TABLE OF DATA USING JSON
    //OR STREAM TO A GOOGLE MAP OR LEAFLET
    var repository = document.getElementById("repo_selector").value;
    var workspace = $("#repository").text();
    var form = $("#output-form");
    var inputs = $(".form-control");
    var checks = $(".checkbox");
    var params = "";
    inputs.each(function (i, el) {
        if (el.id != "repo_selector") {
            //If type = select then add first and iterate over array
            if (el.type == "select-multiple") {
                alert("Haven't figured out multiples yet.");
            } else if (el.id == "OUTPUT") {
                params += el.id + "=" + outputRequest + "&";
            } else {
                params += el.id + "=" + el.value + "&";
            }
            // Remove trailing & from string
        }
    });
    //Inlcude checkboxes
    checks.each(function (i, c) {
        var checkbox = $(c).find('input');
        if (checkbox.prop("checked")) {
            params += checkbox[0].id + "=True";
        }
    });
    params = params.substr(0, params.length - 1);
    FMEServer.runDataStreaming(workspace, repository, params, showTableResults);
}

function generateForm(json) {
    var returnstring = "";
    // list of defaults to set
    var procdefaults = [];
    $('#output_req').show();
    json.forEach(function (param) {

        //We need to check the type of param
        var type = param.type;
        console.log(type);
        //LOOKUP_CHOICE = Select
        //DIRNAME = Textbox
        switch (type) {
            case "LOOKUP_LISTBOX":
            case "LOOKUP_CHOICE":
                returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
                returnstring += '<select type="select" id="' + param.name + '" class="form-control">';
                param.listOptions.forEach(function (options) {
                    returnstring += '<option value="' + options.value + '">' + options.caption + '</option>';
                });
                returnstring += '</select>';
                break;
            case "LISTBOX":
                returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
                returnstring += '<select multiple type="select" size="10" id="' + param.name + '" class="form-control">';
                param.listOptions.forEach(function (options) {
                    returnstring += '<option value="' + options.value + '">' + options.caption + '</option>';
                });
                returnstring += '</select>';
                break;
            case "CHOICE":
                returnstring += '<div class="checkbox">';
                returnstring += '<label><input type="checkbox" id="' + param.name + '" value="' + param.defaultValue + '">' + param.description + '</input></label>';
                break;
            default:
                returnstring += '<div class="form-group"><label class="control-label" for="' + param.name + '">' + param.description + '</label>';
                returnstring += '<input id="' + param.name + '" class="form-control" type="text"\>';
                procdefaults.push([param.name, param.defaultValue]);
        }
        returnstring += '</div>';
    });
    returnstring += '<input class="btn btn-default" value="Submit" onclick="runRequest();" />';
    $("#output-form").html(returnstring);
    procdefaults.forEach(function (defaults) {
        console.log(defaults[0]);
        $("#" + defaults[0]).val(defaults[1]);
    });
}

function runRequest() {
    var outputType = $('#output_request').val();
    var outputRequest = outputType;
    if (outputType == "table") {
        //Should set output type in here to json
        runStreamingTab();
    } else if (outputType == "googleEarth") {
        //Setoutput == OGCKML
        runStreamingMap();
    } else if (outputType == "customizableMap") {
        //Set output == Geojson
        runStreamingMap();
    } else {
        runDataDownload();
    }
}
function generateRepos(json) {
    console.log(json);
    formFields.push(json);
    json.forEach(function (param) {
        if (Boolean(param.title.trim()) && Boolean(param.name.trim())) {
            $("#repo_selector").append($('<option></option>').attr("value", param.name).text(param.title));
        }
    });
}

$(document).ready(function () {

    FMEServer.init(server, token);

    // Test if get repositories else pop up alert
    FMEServer.getRepositoryItems($("#repository").text(), 0, generateRepos);
    //Next step is on change of update output form
    $('#repo_selector').change(function () {
        FMEServer.getWorkspaceParameters($("#repository").text(), $("#repo_selector").val(), generateForm);
        //$('#description').remove('p');
        //TODO GET repo description out.
        var selected = formFields[0].filter(function (obj) {
            if ('name' in obj && obj.name == $("#repo_selector").val()) {
                return true;
            } else {
                return false;
            }
        });
        $('#description').html(selected[0].description);
    });
    //Set output type if downloading
    $("#OUTPUT").change(function () {
        outputRequest = $('#OUTPUT').val();
    });
    //ADD Listener for output format
    $('#output_request').change(function () {
        if ($(this).val() == "Download") {
            $($('#OUTPUT').parent()).show();
            download = true;
        } else {
            $($('#OUTPUT').parent()).hide();
            download = false;
            switch ($(this).val()) {
                case "table":
                    outputRequest = "JSON";
                    break;
                case "googleEarth":
                    outputRequest = "GEOJSON";
                    break;
                case "customizableMap":
                    outputRequest = "GEOJSON";
                    break;
            }
            /*depends upon output */
        }
    });

    $('#repo_selector').focus(function () {
        FMEServer.getWorkspaceParameters($("#repository").text(), $("#repo_selector").val(), generateForm);
    });
});
