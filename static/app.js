var parseTime = d3.timeParse("%m, %d, %Y")
d3.csv("Data/teslanew.csv", function(data) {
    teslaData.forEach(function(data) {
        data.open_price = +data.open_price;
        data.high_price = +data.high_price;
        data.low_price = +data.low_price;
        data.closing_price = +data.closing_price;
        data.adj_close = +data.adj_close;
        data.volume = +data.volume;
        data.range = +data.range;
        data.rng_perct_close = +data.rng_perct_close;
        data.real_date =  parseTime(data.real_date)
    });
    d3.select("tbody")
    .selectAll("tr")
    .data(teslaData)
    .enter()
    .append("tr")
    .html(function(d){
        return `<td>${d.real_date}</td><td>${d.open_price}</td><td>${d.high_price}</td><td>${d.low_price}</td><td>${d.closing_price}</td><td>${d.adj_close}</td>`+
        `<td>${d.volume}</td><td>${d.range}</td><td>${d.rng_perct_close}</td>`
    });
});

function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");
    
    // Use the list of zipcode names to populate the select options
    //d3.json("/allzipcodes").then((zipcodeNames) => {
      d3.json("/allzipcodes", function(error, zipcodeNames){
    
      zipcodeNames.forEach((zipcode) => {
        selector
          .append("option")
          .text(zipcode)
          .property("value", zipcode);
      });
    
      // Use the first zipcode from the list to build the initial plots
      const firstzipcode = zipcodeNames[0];
      //console.log(firstzipcode);
      buildMetadata(firstzipcode);
    });
    
    
    var factorSelector = d3.select("#selFactor")
    d3.json("/names", function(error, factors){
    
      factors.forEach((factor) => {
        factorSelector
          .append("option")
          .text(factor)
          .property("value", factor);
      });
      const firstfactor = factors[0];
      buildCharts(firstfactor);
    });
    
    }
    
    function optionChanged(newzipcode) {
    // Fetch new data each time a new sample is selected
    buildMetadata(newzipcode);
    }
    
    function factorChanged(newfactor) {
      // Fetch new data each time a new sample is selected
      buildCharts(newfactor);
      }
    
      
    // Initialize the dashboard
    init();
    