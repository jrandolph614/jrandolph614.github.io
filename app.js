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



