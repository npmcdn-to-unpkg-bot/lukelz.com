d3.select("#bar").attr("align", "center");

    let margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 250
    };
    let width = 1000 - margin.left - margin.right;
    let height = 1000 - margin.top - margin.bottom;

    // Scales
    let x = d3.scale.linear()
        .range([0, width]);

    let y = d3.scale.ordinal()
        .rangeRoundBands([0, height], .1);

    // Axes
    let xAxis = d3.svg.axis()
        .scale(x)
        .orient("top")
        .ticks(20);

    let yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    // Create SVG element w/ margins and move it to the right
    let svg = d3.select('body')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    // Get json data and callback function
    d3.json("/static/data/angel.json", function(data) {
        console.log(data);
        // create list from nested dict/object
        let all_data = [];
        for (let group in data) {
            for (let cat in data[group]) {
                for (let tech in data[group][cat]) {
                    let obj = {
                        'name': tech,
                        'count': data[group][cat][tech]
                    }
                    all_data.push(obj);
                }
            }
        }

        // Sort highest to lowest by count
        all_data.sort(function(a, b) {
            return b.count - a.count;
        });
        top_all_data = all_data.slice(0, 41);

        // Get domains
        x.domain([0, d3.max(top_all_data, function(d) {
            return d.count;
        })]);
        y.domain(top_all_data.map(function(d) {
            return d.name;
        }));

        // Create x and y axes
        svg.append('g')
            .attr('class', 'x axis')
            .call(xAxis);

        svg.append('g')
            .attr('class', 'y axis')
            .call(yAxis);

        // Input data
        svg.selectAll('.bar')
            .data(top_all_data)
            .enter()
            .append("rect") // x and y describe top left corner
            .attr("class", "bar")
            .attr("x", 0)
            .attr("width", function(d) {
                return x(d.count);
            })
            .attr("y", function(d) {
                return y(d.name);
            })
            .attr("height", y.rangeBand());
    });