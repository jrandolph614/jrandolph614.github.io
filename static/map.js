function createMap(factorPoints, factor) {

    // Create the tile layer that will be the background of our map
    var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.light",
      accessToken: API_KEY
    });
  
    var outdoormap = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.outdoor",
      accessToken: API_KEY
    });
  
    var satellitemap = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.satellite",
      accessToken: API_KEY
    });
  
    // Create a baseMaps object to hold the lightmap layer
    var baseMaps = {
      "Satellite" : satellitemap,
      "Grayscale": lightmap,
      "Outdoors" : outdoormap
    };
      map = L.map("map", {
        center: [40.7282, -73.7949],
        zoom: 11,
        layers: [outdoormap, factorPoints]
      });
  
      var overlayMaps = {};
      overlayMaps[factor] = factorPoints;
      
      // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
      L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
      }).addTo(map);
  
  }
  
  // Perform an API call to the Citi Bike API to get earthquake information. 
  var factorSelector = d3.select("#selmapFactor")
  var map;
  d3.json("/names", function(error, factors){
  
    factors.forEach((factor) => {
      factorSelector
        .append("option")
        .text(factor)
        .property("value", factor);
    });
    const factor = factors[0];
    buildMap(factor);
  });
  
  function buildMap(factor){
  
  
    var passedfactor = factor;
    d3.json('/alldata', function(error, response){
  
    if (factor == "Sales Price"){
      factor = "saleprice";
      rad = 3000;
      col = "blue";
    }
    if (factor == "Total Crime"){
      factor = "totalcrime";
      rad = 1/5;
      col = "red";
    }
    if (factor == "School Rating"){
      factor = "rankStars";
      rad = 1/150;
      col = "#4A235A";
    }
    if (factor == "Rent"){
      factor = "rent";
      rad = 5;
      col = "#900C3F";
    }
    if(factor == "Market Health Index"){
      factor = "marketindex";
      rad = 1/100;
      col = "green";
    }
    if (factor == "Total Income"){
      factor = "totalincome";
      rad = 9000;
      col = "teal";
    }
  
    // Pull the "marketFactors" property off of response.data
    var marketFactors = response;
  
    // Initialize an array to hold marketFactors markers
    var marketFactorsMarkers = [];
  
    console.log(factor);
    // Loop through the marketFactors array
    for (var index = 0; index < marketFactors.length; index++) {
      var marketdata = marketFactors[index];
      
      // For each earthquake, create a marker and bind a popup with the earthquake's name
      var marketFactorsMarker = L.circle([marketdata.latitude, marketdata.longitude], {
        fillOpacity: 0.75,
        color: "black",
        fillColor: col,
        radius: marketdata[factor]/rad,
        weight: .25
      })
        .bindPopup("<h3>" + marketdata.zipcode  + "</h3>"
        + "<h5>Number of Crimes: " + marketdata.totalcrime + "</h5>" 
        + "<h5>Median Home Value: " + marketdata.saleprice + "</h5>" 
        + "<h5>Median Rent: " + marketdata.rent + "</h5>" 
        + "<h5>Total Income: " + marketdata.totalincome + "</h5>" 
        + "<h5>Market Index: " + marketdata.marketindex + "</h5>"
        + "<h5>School Rating: " + marketdata.rankStars + "</h5>");
  
      // Add the marker to the marketFactorsMarkers array
      marketFactorsMarkers.push(marketFactorsMarker);
    }
  
    // Create a layer group made from the bike markers array, pass it into the createMap function
    createMap(L.layerGroup(marketFactorsMarkers), passedfactor);
  
  });
  }
  
  function mapfactorChanged(newfactor) {
    // Fetch new data each time a new sample is selected
    map.off();
    map.remove();
    buildMap(newfactor);
  }
  
  